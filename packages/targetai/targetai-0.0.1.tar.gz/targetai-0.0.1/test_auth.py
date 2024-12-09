import asyncio
from targetai import Auth

async def main():
    # Initialize authentication
    auth = Auth(
        email="g.dementev@targetai.ai",  # Replace with your email
        password="gleb",                  # Replace with your password
        base_url="http://127.0.0.1:8000"  # Replace with your API URL if different
    )

    try:
        # 1. Login and get tokens
        response = await auth.login()
        print("\n1. Login successful!")
        print(f"Access token: {response.access_token[:20]}...")
        print(f"Refresh token: {response.refresh_token[:20]}...")

        # 2. Check authentication status
        status = await auth.get_status()
        print("\n2. Auth status:")
        print(f"Is authenticated: {status['isAuthenticated']}")
        print(f"User info: {status['user']}")

        # 3. Refresh tokens
        refresh_response = await auth.refresh()
        print("\n3. Token refresh successful!")
        print(f"New access token: {refresh_response.access_token[:20]}...")
        print(f"New refresh token: {refresh_response.refresh_token[:20]}...")

        # 4. Logout
        await auth.logout()
        print("\n4. Logged out successfully!")

        # 5. Verify logged out status
        final_status = await auth.get_status()
        print("\n5. Final status:")
        print(f"Is authenticated: {final_status['isAuthenticated']}")
    
    except Exception as e:
        print(f"\nError: {str(e)}")
    
    finally:
        await auth.close()

if __name__ == "__main__":
    asyncio.run(main()) 