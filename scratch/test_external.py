import asyncio
import httpx
import json
import sys

# Simulation of ExternalProvider logic
async def test_server(name, url, api_key, server_type, extra_id=None):
    print(f"\n--- Testing {name} ---")
    url = url.rstrip('/') + '/'
    action = "country_info" if server_type == "lion" else "getCountrys"
    
    if server_type == "lion":
        params = {"action": action, "apiKey": api_key, "YourID": extra_id}
    else:
        params = {"action": action, "apiKay": api_key}
    
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=15.0)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print("RAW RESPONSE (Truncated):")
                print(json.dumps(data, indent=2)[:1000])
                return data
            else:
                print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Exception: {e}")
    return None

async def main():
    # You can fill these with your actual keys to test locally
    # Or I will just provide the script for you to run and tell me the output
    print("This script will test your API servers and show the RAW response.")
    print("Please edit the values below or run it if they are already in DB.")
    
    # We will try to read from DB if possible
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine("sqlite:///database.db")
        with engine.connect() as conn:
            res = conn.execute(text("SELECT name, url, api_key, server_type, extra_id FROM api_servers WHERE is_active=1"))
            servers = res.fetchall()
            for s in servers:
                await test_server(s[0], s[1], s[2], s[3], s[4])
    except Exception as e:
        print(f"Could not read from DB: {e}")

if __name__ == "__main__":
    asyncio.run(main())
