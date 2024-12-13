import asyncio
import logging
import re
from datetime import date, datetime, timedelta
from typing import Any

import aiohttp
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client import ClientResponse

from pysuez.const import (
    API_CONSUMPTION_INDEX,
    API_ENDPOINT_ALERT,
    API_ENDPOINT_DAILY_DATA,
    API_ENDPOINT_LOGIN,
    API_ENDPOINT_MONTH_DATA,
    API_HISTORY_CONSUMPTION,
    ATTRIBUTION,
    BASE_URI,
    INFORMATION_ENDPOINT_INTERVENTION,
    INFORMATION_ENDPOINT_LIMESTONE,
    INFORMATION_ENDPOINT_PRICE,
    INFORMATION_ENDPOINT_QUALITY,
    MAX_REQUEST_ATTEMPT,
    TOKEN_HEADERS,
)
from pysuez.exception import (
    PySuezConnexionError,
    PySuezConnexionNeededException,
    PySuezDataError,
    PySuezError,
)
from pysuez.models import (
    AggregatedData,
    AlertQueryResult,
    AlertResult,
    ConsumptionIndexResult,
    ContractResult,
    DayDataResult,
    InterventionResult,
    LimestoneResult,
    PriceResult,
    QualityResult,
)
from pysuez.utils import cubic_meters_to_liters, extract_token

_LOGGER = logging.getLogger(__name__)


class SuezClient:
    """Client used to interact with suez website."""

    _token: str | None = None
    _headers: dict | None = None
    _session: ClientSession | None = None

    def __init__(
        self,
        username: str,
        password: str,
        counter_id: int | None,
        timeout: ClientTimeout | None = None,
        url: str = BASE_URI,
    ) -> None:
        """Initialize the client object."""

        self._username = username
        self._password = password
        self._counter_id = counter_id
        self._hostname = url
        if timeout is None:
            self._timeout = ClientTimeout(total=60)
        else:
            self._timeout = timeout

    async def check_credentials(self) -> bool:
        try:
            await self._connect()
            return True
        except Exception:
            return False
        finally:
            await self.close_session()

    async def find_counter(self) -> int:
        _LOGGER.debug("Try finding counter")
        page_url = API_HISTORY_CONSUMPTION
        text = await self._get(page_url, read="text")
        match = re.search(
            r"'\/mon-compte-en-ligne\/statMData'\s\+\s'/(\d+)'",
            text,
            re.MULTILINE,
        )
        if match is None:
            raise PySuezError("Counter id not found")
        self._counter_id = int(match.group(1))
        _LOGGER.debug("Found counter {}".format(self._counter_id))
        return self._counter_id

    async def close_session(self) -> None:
        """Close current session."""
        if self._session is not None:
            _LOGGER.debug("Closing suez session")
            await self._logout()
            await self._session.close()
            _LOGGER.debug("Successfully closed suez session")
        self._session = None

    async def fetch_day_data(self, date: datetime | date) -> DayDataResult | None:
        """Retrieve requested day consumption if available or none if not.

        ! This method will retrieve all month data"""
        year = date.year
        month = date.month

        result_by_day = await self.fetch_month_data(year, month)
        if len(result_by_day) == 0:
            return None
        return result_by_day[len(result_by_day) - 1]

    async def fetch_yesterday_data(self) -> DayDataResult | None:
        """Retrieve yesterday consumption if available or none if not.

        ! This method will retrieve all month data"""
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        return await self.fetch_day_data(yesterday)

    async def fetch_month_data(self, year, month) -> list[DayDataResult]:
        now = datetime.now()

        result_by_day = await self._get(
            API_ENDPOINT_DAILY_DATA,
            year,
            month,
            with_counter_id=True,
            params={"_=": now.timestamp()},
        )
        if result_by_day[0] == "ERR":
            _LOGGER.debug(
                "Error while requesting data for {}/{}: {}".format(
                    year, month, result_by_day[1]
                )
            )
            return []

        result = []
        for day in result_by_day:
            date = datetime.strptime(day[0], "%d/%m/%Y")
            try:
                total = float(day[2])
                if total > 0:
                    result.append(
                        DayDataResult(
                            date.date(),
                            cubic_meters_to_liters(float(day[1])),
                            total,
                        )
                    )
            except ValueError:
                _LOGGER.debug(f"Failed to parse consumption value:{day[1]} / {day[0]} ")
                return result
        return result

    async def fetch_all_daily_data(
        self, since: date | None = None, timeout: int | None = 60
    ) -> list[DayDataResult]:
        async with asyncio.timeout(timeout):
            current = datetime.now().date()
            _LOGGER.debug(
                "Getting all available data from suez since %s to %s",
                str(since),
                str(current),
            )
            result = []
            while since is None or current >= since:
                try:
                    _LOGGER.debug("Fetch data of " + str(current))
                    current = current.replace(day=1)
                    month = await self.fetch_month_data(current.year, current.month)
                    if len(month) == 0:
                        return result
                    next_result = []
                    next_result.extend(month)
                    next_result.extend(result)
                    result = next_result
                    current = current - timedelta(days=1)
                except PySuezDataError:
                    return result
            return result

    async def fetch_aggregated_data(self) -> AggregatedData:
        """Fetch latest data from Suez."""
        now = datetime.now()
        today_year = now.strftime("%Y")
        today_month = now.strftime("%m")

        yesterday_data = await self.fetch_yesterday_data()
        if yesterday_data is not None:
            state = yesterday_data.day_consumption
        else:
            state = None

        month_data = await self.fetch_month_data(today_year, today_month)
        current_month = {}
        for item in month_data:
            current_month[item.date] = item.day_consumption

        if int(today_month) == 1:
            last_month = 12
            last_month_year = int(today_year) - 1
        else:
            last_month = int(today_month) - 1
            last_month_year = today_year

        previous_month_data = await self.fetch_month_data(last_month_year, last_month)
        previous_month = {}
        for item in previous_month_data:
            previous_month[item.date] = item.day_consumption

        (
            highest_monthly_consumption,
            last_year,
            current_year,
            history,
        ) = await self._fetch_aggregated_statistics()

        return AggregatedData(
            value=state,
            current_month=current_month,
            previous_month=previous_month,
            highest_monthly_consumption=highest_monthly_consumption,
            previous_year=last_year,
            current_year=current_year,
            history=history,
            attribution=ATTRIBUTION,
        )

    async def get_consumption_index(self) -> ConsumptionIndexResult:
        """Fetch consumption index."""
        json = await self._get(API_CONSUMPTION_INDEX)
        return ConsumptionIndexResult(**json)

    async def get_alerts(self) -> AlertResult:
        """Fetch alert data from Suez."""
        json = await self._get(API_ENDPOINT_ALERT)
        alert_response = AlertQueryResult(**json)
        return AlertResult(
            alert_response.content.leak.status != "NO_ALERT",
            alert_response.content.overconsumption.status != "NO_ALERT",
        )

    async def get_price(self) -> PriceResult:
        """Fetch water price in e/m3"""
        contract = await self.contract_data()
        json = await self._get(INFORMATION_ENDPOINT_PRICE, contract.inseeCode)
        return PriceResult(**json)

    async def get_water_quality(self) -> QualityResult:
        """Fetch water quality"""
        contract = await self.contract_data()
        json = await self._get(INFORMATION_ENDPOINT_QUALITY, contract.inseeCode)
        return QualityResult(**json)

    async def get_interventions(self) -> InterventionResult:
        """Fetch water interventions"""
        contract = await self.contract_data()
        json = await self._get(
            INFORMATION_ENDPOINT_INTERVENTION,
            contract.inseeCode,
        )
        return InterventionResult(**json)

    async def get_limestone(self) -> LimestoneResult:
        """Fetch water limestone values"""
        contract = await self.contract_data()
        json = await self._get(INFORMATION_ENDPOINT_LIMESTONE, contract.inseeCode)
        return LimestoneResult(**json)

    async def contract_data(self) -> ContractResult:
        url = "/public-api/user/donnees-contrats"
        json = await self._get(url)
        return ContractResult(json[0])

    async def _fetch_aggregated_statistics(
        self,
    ) -> tuple[int, int, int, dict[date, float]]:
        try:
            statistics_url = API_ENDPOINT_MONTH_DATA
            fetched_data: list = await self._get(statistics_url, with_counter_id=True)
            highest_monthly_consumption = int(
                cubic_meters_to_liters(float(fetched_data[-1]))
            )
            fetched_data.pop()
            last_year = int(cubic_meters_to_liters(float(fetched_data[-1])))
            fetched_data.pop()
            current_year = int(cubic_meters_to_liters(float(fetched_data[-1])))
            fetched_data.pop()
            history = {}
            for item in fetched_data:
                history[item[3]] = int(cubic_meters_to_liters(float(item[1])))
        except ValueError:
            raise PySuezError("Issue with history data")
        return highest_monthly_consumption, last_year, current_year, history

    async def _get_token(self) -> None:
        """Get the token"""
        headers = {**TOKEN_HEADERS}
        url = self._hostname + API_ENDPOINT_LOGIN

        session = self._get_session()
        async with session.get(url, headers=headers, timeout=self._timeout) as response:
            headers["Cookie"] = ""
            cookies = response.cookies
            for key in cookies.keys():
                if headers["Cookie"]:
                    headers["Cookie"] += "; "
                headers["Cookie"] += key + "=" + cookies.get(key).value

            page = await response.text("utf-8")
            self._token = extract_token(page)
            self._headers = headers

    async def _connect(self) -> bool:
        """Connect and get the cookie"""
        data, url = await self._get_credential_query()
        try:
            session = self._get_session()
            async with session.post(
                url,
                headers=self._headers,
                data=data,
                allow_redirects=True,
                timeout=self._timeout,
            ) as response:
                if response.status >= 400:
                    raise PySuezConnexionError(f"Login error: status={response.status}")
                cookies = session.cookie_jar.filter_cookies(response.url.origin())
                session_cookie = cookies.get("eZSESSID")
                if session_cookie is None:
                    raise PySuezConnexionError(
                        "Login error: Please check your username/password."
                    )
                # Get the URL after possible redirection
                self._hostname = response.url.origin().__str__()
                _LOGGER.debug(
                    f"Login successful, redirected from {url} to {self._hostname}"
                )

                self._headers["Cookie"] = ""
                session_id = session_cookie.value
                self._headers["Cookie"] = "eZSESSID=" + session_id
                return True
        except Exception:
            raise PySuezConnexionError("Can not submit login form.")

    async def _get(
        self, *url: str, with_counter_id=False, params=None, read: str | None = "json"
    ) -> Any:
        url = self._get_url(self._hostname, *url, with_counter_id=with_counter_id)
        _LOGGER.debug(f"Try requesting {url}")

        remaing_attempt = MAX_REQUEST_ATTEMPT
        while remaing_attempt > 0:
            remaing_attempt -= 1
            try:
                async with self._get_session().get(
                    url,
                    headers=self._headers,
                    params=params,
                    timeout=self._timeout,
                    allow_redirects=not read,
                ) as response:
                    self._check_request_status(response, url)
                    if not read:
                        return
                    if read == "json":
                        return await response.json()
                    return await response.text()
            except PySuezConnexionNeededException as err:
                if remaing_attempt > 0:
                    await self._connect()
                else:
                    raise err
            except Exception as ex:
                await self.close_session()
                if remaing_attempt == 0:
                    raise PySuezError(f"Error during get query to {url}") from ex
                else:
                    _LOGGER.warning(f"Discarded error during query to {url}", ex)

    def _get_session(self) -> ClientSession:
        if self._session is not None:
            return self._session
        self._session = aiohttp.ClientSession()
        return self._session

    async def _get_credential_query(self):
        await self._get_token()
        data = {
            "_csrf_token": self._token,
            "tsme_user_login[_username]": self._username,
            "tsme_user_login[_password]": self._password,
        }
        url = self._get_url(self._hostname, API_ENDPOINT_LOGIN, with_counter_id=False)
        return data, url

    async def _logout(self) -> None:
        if self._session is not None:
            await self._get("/mon-compte-en-ligne/deconnexion", read=False)
            _LOGGER.debug("Successfully logged out from suez")

    def _get_url(self, *url: str, with_counter_id: bool) -> str:
        res = ""
        first = True
        for part in url:
            next = str(part)
            if not first and not res.endswith("/") and not next.startswith("/"):
                res += "/"
            res += next
            first = False

        if with_counter_id:
            if not res.endswith("/"):
                res += "/"
            res += str(self._counter_id)
        return res

    def _check_request_status(self, response: ClientResponse, url: str) -> bool:
        _LOGGER.debug(f"{url} responded with {response.status}")
        if response.status >= 200 and response.status < 300:
            return True
        if response.status >= 300 and response.status < 400:
            redirection_target = response.headers.get("Location")
            if redirection_target and API_ENDPOINT_LOGIN in redirection_target:
                raise PySuezConnexionNeededException(
                    f"Redirected to {redirection_target}, should log again"
                )
            else:
                _LOGGER.debug(f"Ignored redirection to {redirection_target}")
                return True
        raise PySuezError(f"Unexpected response status {response.status} for {url}")
