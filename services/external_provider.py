import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

class ExternalProvider:
    def __init__(self, name, url, api_key, profit_margin, server_type="standard", extra_id=None):
        self.name = name
        self.url = url.rstrip('/') + '/'
        self.api_key = api_key
        self.profit_margin = profit_margin
        self.server_type = server_type
        self.extra_id = extra_id

    def get_base_params(self, action):
        """Prepare base parameters for API calls."""
        if self.server_type == "lion":
            params = {
                "action": action,
                "apiKey": self.api_key,
                "YourID": self.extra_id
            }
        else:
            # Standard (Spider/Max-TG)
            params = {
                "action": action,
                "apiKey": self.api_key,
                "apiKay": self.api_key  # Some panels have this typo
            }
        return params

    async def get_countries(self):
        """Fetch available countries and prices from the provider."""
        try:
            async with httpx.AsyncClient() as client:
                action = "country_info" if self.server_type == "lion" else "getCountrys"
                params = self.get_base_params(action)
                
                logger.info(f"Fetching countries from {self.name}: {self.url} with {params}")
                resp = await client.get(self.url, params=params, timeout=15.0)
                if resp.status_code == 200:
                    data = resp.json()
                    logger.info(f"Response from {self.name}: {data}")
                    return data
                else:
                    logger.warning(f"Failed to fetch countries from {self.name}: {resp.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching countries from {self.name}: {e}")
            return []

    async def get_balance(self):
        """Fetch the current balance from the provider."""
        try:
            async with httpx.AsyncClient() as client:
                # 1. Determine the correct action
                if self.server_type == "lion":
                    action = "balance" # Lion typically uses 'balance' or 'get_balance'
                else:
                    action = "getBalance"
                    
                params = self.get_base_params(action)
                
                logger.info(f"Fetching balance from {self.name}: {self.url} (Action: {action})")
                resp = await client.get(self.url, params=params, timeout=15.0)
                
                if resp.status_code == 200:
                    text = resp.text.strip()
                    logger.info(f"Raw balance response from {self.name}: {text}")
                    
                    # 1. Try parsing as JSON
                    try:
                        data = resp.json()
                        if isinstance(data, dict):
                            # Common field names for balance
                            balance_keys = ["balance", "Balance", "money", "credit", "amount", "balans", "sum", "user_balance", "available_balance", "credits"]
                            
                            # A. Direct search
                            for key in balance_keys:
                                if key in data and data[key] is not None:
                                    try: return {"status": "success", "balance": float(data[key])}
                                    except: continue
                            
                            # B. Nested search (Common for Standard panels like Max-TG/Spider)
                            for sub in ['result', 'user', 'info', 'data']:
                                if sub in data:
                                    # If result is a dict
                                    if isinstance(data[sub], dict):
                                        for key in balance_keys:
                                            v = data[sub].get(key)
                                            if v is not None:
                                                try: return {"status": "success", "balance": float(v)}
                                                except: continue
                                    # If result is a raw value (some panels)
                                    elif sub == 'result':
                                        try: return {"status": "success", "balance": float(data[sub])}
                                        except: continue

                            # C. Handle specific status/ok flags
                            msg = data.get("message") or data.get("msg") or data.get("error") or data.get("status")
                            if msg and msg != "success":
                                keys_found = ", ".join(data.keys())
                                return {"status": "error", "message": f"{msg} (Keys: {keys_found})"}
                            
                            keys_found = ", ".join(data.keys())
                            return {"status": "error", "message": f"Balance missing. Keys: {keys_found}"}
                    except:
                        # 2. Try parsing as raw number
                        try:
                            return {"status": "success", "balance": float(text)}
                        except:
                            pass
                            
                    return {"status": "error", "message": f"Format Error. Text: {text[:50]}"}
                else:
                    return {"status": "error", "message": f"HTTP {resp.status_code}"}
        except Exception as e:
            logger.error(f"Error fetching balance from {self.name}: {e}")
            return {"status": "error", "message": str(e)}


    async def buy_number(self, country_code):
        """Order a new number from the provider."""
        try:
            async with httpx.AsyncClient() as client:
                params = self.get_base_params("getNumber")
                if self.server_type == "lion":
                    params["country_code"] = country_code
                else:
                    params["country"] = country_code
                
                resp = await client.get(self.url, params=params, timeout=20.0)
                if resp.status_code == 200:
                    data = resp.json()
                    return data
                return {"status": "error", "message": f"HTTP {resp.status_code}"}
        except Exception as e:
            logger.error(f"Error buying number from {self.name}: {e}")
            return {"status": "error", "message": str(e)}

    async def get_code(self, hash_code, number=None):
        """Fetch the activation code for a purchased number."""
        try:
            async with httpx.AsyncClient() as client:
                params = self.get_base_params("getCode")
                if self.server_type == "lion":
                    params["number"] = number
                else:
                    params["hash_code"] = hash_code
                
                resp = await client.get(self.url, params=params, timeout=15.0)
                if resp.status_code == 200:
                    data = resp.json()
                    return data
                return {"status": "error", "message": f"HTTP {resp.status_code}"}
        except Exception as e:
            logger.error(f"Error getting code from {self.name}: {e}")
            return {"status": "error", "message": str(e)}

    def calculate_price(self, provider_price):
        """Calculate selling price based on profit margin."""
        return float(provider_price) * (1 + self.profit_margin / 100.0)
