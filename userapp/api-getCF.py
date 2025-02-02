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


def show_device(deviceId, token):
    headers = {'Authorization': f'{token}', 'Content-Type': 'application/json'}

    api_url = f'https://gargantuan-unwritten-carp.gigalixirapp.com/api/v1/getContentFilters'
    print(api_url)    

    response = requests.get(api_url, headers=headers)

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
deviceId = 2

device_data = show_device(deviceId, token)

if device_data:
    #res = json.loads( device_data.json())
    #print("data: ", res)
    #print("data: ", res['content_filters'])
    print("\n")
    #print("data: ", device_data.json()['content_filters'])
    print("headers: ",device_data.headers)
#    print("content: ",device_data.content) # just json in bytes
    print("data: ", device_data.json())

