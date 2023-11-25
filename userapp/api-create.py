import requests

def create_device_and_sign_in(api_url, email, password, device_name):
    data = {
#        'sub': "auth0|655331b127a4232eddd25768",
        'email': email,
        'password': password,
        'device': {'name': device_name}
    }
    response = requests.post(api_url, json=data)

    if response.status_code >= 200 and response.status_code < 300:
        return response
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return None

# Example usage
api_url = 'http://localhost:3000/api/v1/devices'  # Replace with your actual API endpoint
username = 'fake@email.com'  # Replace with the actual username
password = 'Passw0rd'       # Replace with the actual password
device_name = 'New Device'      # Replace with the desired device name

device_data = create_device_and_sign_in(api_url, username, password, device_name)

if device_data:
    print(device_data.json())
    print("headers: ",device_data.headers)
    print("content: ",device_data.content)

