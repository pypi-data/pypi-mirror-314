import aiohttp
from typing import Optional
from pydantic import BaseModel

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str

class Auth:
    def __init__(self, email: str, password: str, base_url: str = "http://localhost:8000"):
        self.email = email
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def login(self) -> AuthResponse:
        """Authenticate with the API and get access and refresh tokens"""
        await self._ensure_session()
        
        login_data = {
            "email": self.email,
            "password": self.password
        }
        
        async with self._session.post(f"{self.base_url}/api/login", json=login_data) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Authentication failed: {error_text}")
            
            data = await response.json()
            auth_response = AuthResponse(
                access_token=data["access_token"],
                refresh_token=data["refresh_token"]
            )
            self.access_token = auth_response.access_token
            self.refresh_token = auth_response.refresh_token
            return auth_response

    async def refresh(self) -> AuthResponse:
        """Refresh the access token using the refresh token"""
        if not self.refresh_token:
            raise Exception("No refresh token available. Please login first.")

        await self._ensure_session()
        cookies = {"refresh_token_cookie": self.refresh_token}
        
        async with self._session.post(f"{self.base_url}/api/refresh", cookies=cookies) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Token refresh failed: {error_text}")
            
            data = await response.json()
            auth_response = AuthResponse(
                access_token=data["access_token"],
                refresh_token=data["refresh_token"]
            )
            self.access_token = auth_response.access_token
            self.refresh_token = auth_response.refresh_token
            return auth_response

    async def logout(self) -> None:
        """Logout and invalidate tokens"""
        await self._ensure_session()
        
        async with self._session.post(f"{self.base_url}/api/logout") as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Logout failed: {error_text}")

        self.access_token = None
        self.refresh_token = None

    async def get_status(self) -> dict:
        """Get current authentication status"""
        if not self.access_token:
            return {"isAuthenticated": False, "user": None}

        await self._ensure_session()
        headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
        
        async with self._session.get(f"{self.base_url}/api/status", headers=headers) as response:
            if response.status != 200:
                return {"isAuthenticated": False, "user": None}
            
            return await response.json()

    async def close(self):
        """Close the underlying HTTP session"""
        if self._session:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    def __del__(self):
        """Ensure resources are cleaned up"""
        if self._session and not self._session.closed:
            import asyncio
            try:
                asyncio.get_event_loop().run_until_complete(self.close())
            except:
                pass  # Event loop might be closed