import requests
import json
from io import StringIO

def authenticate_user(email, password):
    #url = "http://localhost:4000/api/v1/session"
    url = "https://gargantuan-unwritten-carp.gigalixirapp.com/api/v1/session"
    headers = {"Content-Type": "application/json"}
    data = {
        "user": {
            "email": email,
            "password": password
        }
    }

    print(url)
    response = requests.post(url, json=data, headers=headers)
    return response

def show_device(deviceId):
    api_url = f'https://gargantuan-unwritten-carp.gigalixirapp.com/api/v1/devices/{deviceId}'
    headers = {'Authorization': f'{token}', 'Content-Type': 'application/json'}

    print(api_url)    

    response = requests.get(api_url, headers=headers)

    if response.status_code >= 200 and response.status_code < 300:
        return response
    else:
        print(f"Error: {response.status_code}, Message: ") # {response.text}")
        return None

email = "fake@email.com"
password = "password"
result = authenticate_user(email, password)

token = result.json().get('data').get('access_token')
renewal_token = result.json().get('data').get('renewal_token')

# Example usage
deviceId = "15b417c2-574e-4c07-a78d-58e6d86e8530"

device_data = show_device(deviceId)

if device_data:
    #res = json.loads( device_data.json())
    #print("data: ", res)
    #print("data: ", res['content_filters'])
    print("data: ", device_data.json())
    print("\n")
    print("headers: ",device_data.headers)
    print("content: ",device_data.content)

