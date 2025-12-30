import aiohttp
import logging
from typing import Optional, Dict, Any, List
from config import settings

logger = logging.getLogger(__name__)

class TTCApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = settings.TTC_BASE_URL

    async def _make_request(self, action: str, params: Optional[Dict[str, Any]] = None) -> str:
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        params['action'] = action
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.base_url, params=params) as response:
                    text = await response.text()
                    logger.debug(f"API Request: {action}, Params: {params}, Response: {text}")
                    return text
            except Exception as e:
                logger.error(f"API Request Error: {e}")
                return f"ERROR:{e}"

    async def get_balance(self) -> float:
        """Returns the current balance."""
        result = await self._make_request("getBalance")
        if result.startswith("ACCESS_BALANCE:"):
            return float(result.split(":")[1])
        return 0.0

    async def get_countries(self) -> List[Dict[str, Any]]:
        """Returns a list of countries."""
        async with aiohttp.ClientSession() as session:
            params = {'api_key': self.api_key, 'action': 'getCountries'}
            async with session.get(self.base_url, params=params) as response:
                try:
                    return await response.json()
                except:
                    return []

    async def get_services(self, country_id: int) -> List[Dict[str, Any]]:
        """Returns a list of services for a country."""
        async with aiohttp.ClientSession() as session:
            params = {'api_key': self.api_key, 'action': 'getServicesList', 'country': country_id}
            async with session.get(self.base_url, params=params) as response:
                try:
                    data = await response.json()
                    return data.get("services", [])
                except:
                    return []

    async def get_prices(self, service: str, country_id: int) -> List[Dict[str, Any]]:
        """Returns prices for a service in a country."""
        async with aiohttp.ClientSession() as session:
            params = {'api_key': self.api_key, 'action': 'getPrices', 'service': service, 'country': country_id}
            async with session.get(self.base_url, params=params) as response:
                try:
                    return await response.json()
                except:
                    return []

    async def get_number(self, service: str, country_id: int) -> Optional[Dict[str, str]]:
        """Requests a phone number."""
        result = await self._make_request("getNumber", {"service": service, "country": country_id})
        # Format: ACCESS_NUMBER:<activation_id>:<number>
        if result.startswith("ACCESS_NUMBER:"):
            parts = result.split(":")
            return {
                "id": parts[1],
                "number": parts[2]
            }
        return None

    async def set_status(self, activation_id: str, status: int) -> str:
        """
        1 - SMS sent (ready)
        3 - request resend
        6 - complete
        8 - cancel
        """
        return await self._make_request("setStatus", {"id": activation_id, "status": status})

    async def get_status(self, activation_id: str) -> str:
        """Returns status: STATUS_WAIT_CODE, STATUS_WAIT_RETRY, STATUS_OK:code, STATUS_CANCEL"""
        return await self._make_request("getStatus", {"id": activation_id})
