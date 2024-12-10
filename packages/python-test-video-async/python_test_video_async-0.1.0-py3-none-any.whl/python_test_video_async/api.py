import aiohttp
import json
from .exceptions import APIError

BASE_URL = "https://v1.fastpix.io"

async def make_request(method, endpoint, headers=None, data=None, params=None):
    """
    Generic async request method to handle different HTTP methods.
    
    Args:
        method (str): HTTP method (GET, POST, PATCH, DELETE, etc.)
        endpoint (str): API endpoint
        headers (dict, optional): Request headers
        data (dict, optional): Request payload
        params (dict, optional): Query parameters
    
    Returns:
        dict: JSON response from the API
    
    Raises:
        APIError: For API-related errors
    """
    url = f"{BASE_URL}{endpoint}"
    headers = headers or {}

    try:
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url, headers=headers, params=params) as response:

                    if response.status == 200:
                        return await response.json()
                    else:
                        raise APIError(f"Request failed with status {response.status}: {await response.text()}")

            elif method == "POST":
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise APIError(f"Request failed with status {response.status}: {await response.text()}")

            elif method == "PATCH":
                async with session.patch(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise APIError(f"Request failed with status {response.status}: {await response.text()}")

            elif method == "PUT":
                async with session.put(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise APIError(f"Request failed with status {response.status}: {await response.text()}")

            elif method == "DELETE":
                async with session.delete(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise APIError(f"Request failed with status {response.status}: {await response.text()}")

            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

    except aiohttp.ClientError as e:
        raise APIError(f"Request failed: {str(e)}")
