# api_handler.py
import requests
import os
import logging

BASE_URL = "https://evaluate-api.vijil.ai/v1"

SUPPORTED_HUBS = {
    "openai": "OpenAI",
    "together": "Together",
    "octo": "OctoAI",
    "mistral": "Mistral",
    "fireworks": "Fireworks",
    "nvidia": "NVIDIA",
    "vertex": "Vertex",
    "bedrock_custom": "Bedrock",
    "azure": "Azure",
    "custom": "Custom",
    "digitalocean": "DigitalOcean",
}

# Set up logging
HIDDEN_DIR_NAME = ".vijil"
LOG_FILE_NAME = "vijil.log"
LOG_FILE_PATH = os.path.join(os.path.expanduser('~'), HIDDEN_DIR_NAME, LOG_FILE_NAME)
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
logging.basicConfig(level=logging.ERROR, filename=LOG_FILE_PATH, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def make_api_request(base_url, endpoint, method="get", token=None, params=None, data=None):
    url = f"{base_url}/{endpoint}"
    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = {}
            
    try:
        if method.lower() == "get":
            response = requests.get(url, params=params, headers=headers)
            # print("GET request made") # code to test if the request is being made
        elif method.lower()=='put':
            response = requests.put(url, json=data, params=params, headers=headers)
        elif method.lower() == "delete":
            response = requests.delete(url, params=params, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url, json=data, params=params, headers=headers)
            # print(f"POST request made to {url} with payload {data}") # code to test if the request is being made
        else:
            raise ValueError("Invalid HTTP method. Use 'get', 'put', 'delete', or 'post'.")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e} based on response: {response.text}")
    except ValueError as e:
        print(f"Error: {e}")

def get_api_proxy_dict(base_url, token=None):

    response = make_api_request(base_url=base_url, endpoint="api-keys", token=token)
    
    unique_hubs = set([r['hub'] for r in response])
    hubs_dict = {hub: {} for hub in unique_hubs}
    for hub in unique_hubs:
        for r in response:
            if r['hub'] == hub:
                hubs_dict[hub][r['name']] = r['id']
                
    return hubs_dict
