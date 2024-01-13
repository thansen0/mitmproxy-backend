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
    return response #response.json()

# CREATE
def show_device(token):
    headers = {'Authorization': f'{token}', 'Content-Type': 'application/json'}
    #data = {"device": {"name": "API Device 1"}}
    data = {}

    #api_url = f'http://localhost:4000/api/v1/session/renew'  # Replace with your actual API endpoint
    api_url = f'https://gargantuan-unwritten-carp.gigalixirapp.com/api/v1/session/renew'
    print(api_url)

    print("\nheaders:", headers, "\ndata:", data)
    response = requests.post(api_url, headers=headers )

    if response.status_code >= 200 and response.status_code < 300:
        return response
    else:
        print(f"Error: {response.status_code}, Message: ") # {response.text}")
        return None


# Example usage
email = "fake@email.com"
password = "password"
result = authenticate_user(email, password)

print(result)
print(result.json())
#print(result.headers)

token = result.json().get('data').get('access_token')
renewal_token = result.json().get('data').get('renewal_token')

# Example usage
device_data = show_device(renewal_token)

if device_data:
    print("\n")
    print(device_data)
    print("headers: ",device_data.headers, "\n")
#    print("content: ",device_data.content) # just json in bytes
    print("data: ", device_data.json())

