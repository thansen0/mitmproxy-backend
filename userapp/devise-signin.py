import requests

#url = 'https://your-rails-app.com/authenticate'  # Replace with your authentication endpoint URL
#url = 'http://127.0.0.1:3000/api/auth/login'
url = 'http://127.0.0.1:3000/user/sign_in'
#url = 'http://127.0.0.1:3000/login'
# url = "http://localhost:3000/api/v1/sign_in"
data = {
    'user': {
        'email': 'fake@email.com',
        'password': 'password'
    }
}

#data = {
#    'email': 'fake@email.com',
#    'password': 'password'
#}

response = requests.post(url, json=data)
#response = requests.get(url, auth=('fake@email.com', 'password'))
print(response)

if response.status_code == 200:
    # Authentication successful
    #auth_token = response.json()#['auth_token']
    # Store the token for future requests
    #print(auth_token)
    print("Successful login")
    print(response.json())
else:
    # Authentication failed
    print('Authentication failed. Check credentials or handle the error.')
    print(response.json())
    print(response.json()['error'])



exit(1)


data = {
    'user': {
        'email': 'wrong@email.com',
        'password': 'passwwword'
    }
}

response = requests.post(url, json=data)
#response = requests.get(url, auth=('wrong@email.com', 'passwword'))
print(response)

if response.status_code == 200:
    # Authentication successful
    #auth_token = response.json()#['auth_token']
    # Store the token for future requests
    #print(auth_token)
    print("Successful login")
else:
    # Authentication failed
    print('Authentication failed. Check credentials or handle the error.')
    print(response)

    print(url)
    #print(data)
