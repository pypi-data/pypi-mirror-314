import os
import ngiri

API_BASE_URLS = {
    "console": "https://console.ngao.pro",
    "dashboard": "https://dashboard.ngao.pro",
    "vpn": "https://vpn.ngao.pro",
}

def get_auth_token():
    token = os.getenv("NGAO_AUTH_TOKEN")
    if not token:
        raise EnvironmentError("NGAO_AUTH_TOKEN environment variable is not set.")
    return token

def make_request(service, endpoint, method="GET", data=None, params=None):
    url = f"{API_BASE_URLS[service]}{endpoint}"
    headers = {"Authorization": f"Bearer {get_auth_token()}"}

    try:
        if method == "GET":
            response = ngiri.get(url, params=params, headers=headers)
        elif method == "POST":
            response = ngiri.post(url, data=data, params=params, headers=headers)
        elif method == "PUT":
            response = ngiri.put(url, data=data, params=params, headers=headers)
        elif method == "DELETE":
            response = ngiri.delete(url, params=params, headers=headers)
        elif method == "HEAD":
            response = ngiri.head(url, params=params, headers=headers)
        elif method == "OPTIONS":
            response = ngiri.options(url, params=params, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()
    except ngiri.HTTPError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise
