import requests


class LoginHelper:

    def __init__(self):
        self.url = 'http://127.0.0.1:3000/users/sign_in'

    def isLoggedIn(self):
        return False

    def login(self, username, password):
        print(username)
        print(password)
        response = requests.get(self.url, auth=(username, password))

        print(response)

        if response.status_code == 200:
            print("Successful login")
            #auth_token = response.json()['auth_token']
            #print(auth_token)
            return True
        else:
            print("Error logging in")

            return False

    def close(self):
        print("Closing login helper")