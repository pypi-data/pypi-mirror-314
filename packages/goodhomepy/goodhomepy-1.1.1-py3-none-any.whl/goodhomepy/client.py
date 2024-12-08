import aiohttp

from goodhomepy.models import *


class GoodHomeClient:
    BASE_URL = "https://shkf02.goodhome.com"

    def __init__(self, token: str = None, ssl_verify=False):
        self.token = token
        self.ssl_verify = ssl_verify

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def __get_session(self):
        if not self.ssl_verify:
            return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        return aiohttp.ClientSession()

    async def login(self, email: str, password: str) -> AuthResponse:
        async with self.__get_session() as session:
            async with session.post(f"{self.BASE_URL}/v1/auth/login", headers=self._get_headers(),
                                    json={"email": email, "password": password}) as response:
                json_data = await response.json()
                auth_response = AuthResponse(**json_data)
                return auth_response

    async def refresh_token(self, refresh_token: str) -> str:
        async with self.__get_session() as session:
            async with session.get(f"{self.BASE_URL}/v1/auth/token", headers=self._get_headers(),
                                   params={"refresh_token": refresh_token}) as response:
                json_data = await response.json()
                refresh_token_response = RefreshTokenResponse(**json_data)
                self.token = refresh_token_response.token
                return self.token

    async def verify_token(self, token: str) -> bool:
        async with self.__get_session() as session:
            async with session.get(f"{self.BASE_URL}/v1/auth/verify", headers=self._get_headers(),
                                   params={"token": token}) as response:
                json_data = await response.json()
                verify_token_response = VerifyTokenResponse(**json_data)
                return verify_token_response.expire > 0

    async def get_devices(self, user_id: str) -> List[Device]:
        async with self.__get_session() as session:
            async with session.get(f"{self.BASE_URL}/v1/users/{user_id}/devices",
                                   headers=self._get_headers()) as response:
                json_data = await response.json()
                devices = json_data.get("devices", [])
                return [Device(**item) for item in devices]

    async def get_user(self, user_id: str) -> User:
        async with self.__get_session() as session:
            async with session.get(f"{self.BASE_URL}/v1/users/{user_id}", headers=self._get_headers()) as response:
                json_data = await response.json()
                return User(**json_data)

    async def get_homes(self, user_id: str) -> List[Home]:
        async with self.__get_session() as session:
            async with session.get(f"{self.BASE_URL}/v1/users/{user_id}/homes",
                                   headers=self._get_headers()) as response:
                json_data = await response.json()
                homes = json_data.get("homes", [])
                return [Home(**item) for item in homes]
