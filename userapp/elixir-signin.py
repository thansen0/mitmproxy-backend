import requests

def authenticate_user(email, password):
    url = "http://localhost:4000/api/v1/session"
    # url = "http://localhost:4000/api/api_devices"
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

# Example usage
email = "fake@email.com"
password = "password"
result = authenticate_user(email, password)
print(result)
