import requests

def sign_in(email, password):
    url = "http://localhost:4000/api/v1/session"
    data = {
        'user[email]': email,
        'user[password]': password
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("Sign in successful!")
        # You can process the response further here
        # For example, extracting and returning a session token or cookie
        return response
    else:
        print("Sign in failed. Status code:", response.status_code)
        return None

# Example usage
email = "fake@email.com"
password = "password"
response = sign_in(email, password)

print(response)
print("text",response.text)
print("headers",response.headers)
print("json",response.json())
