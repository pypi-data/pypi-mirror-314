# TargetAI Python SDK

A Python SDK for interacting with the TargetAI API.

## Installation

```bash
pip install targetai
```

## Quick Start

Here's a complete example showing how to use the SDK:

```python
import asyncio
from targetai import Auth

async def main():
    # Initialize authentication with custom base URL (default is http://localhost:8000)
    auth = Auth(
        email="your_email@example.com",
        password="your_password",
        base_url="http://localhost:8000"  # Change this to your API URL
    )

    try:
        # Login and get tokens
        response = await auth.login()
        print(f"Access token: {response.access_token}")
        print(f"Refresh token: {response.refresh_token}")

        # Check authentication status
        status = await auth.get_status()
        print(f"Is authenticated: {status['isAuthenticated']}")
        print(f"User info: {status['user']}")

        # Refresh tokens when needed
        new_tokens = await auth.refresh()
        
        # Logout when done
        await auth.logout()
    
    finally:
        # Always close the session
        await auth.close()

# Run the async example
if __name__ == "__main__":
    asyncio.run(main())
```

You can also use the context manager pattern:

```python
async def main():
    async with Auth(
        email="your_email@example.com",
        password="your_password",
        base_url="http://localhost:8000"
    ) as auth:
        response = await auth.login()
        print(f"Successfully logged in!")
```

## Features

- Simple authentication with email and password
- Token refresh support
- Session management with logout
- Authentication status checking
- Async support for all operations
- Type hints for better IDE support
- Configurable base URL for API endpoints

## Requirements

- Python 3.7+
- aiohttp
- pydantic

## License

MIT 