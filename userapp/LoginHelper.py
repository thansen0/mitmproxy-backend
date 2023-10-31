import requests


class LoginHelper:

    def __init__(self):
        self.url = 'http://127.0.0.1:3000/users/sign_in'
        self.username = None

    def isLoggedIn(self):
        return False

    def login(self, username, password):
        print(username)
        print(password)
        
        response = None
        try:
            response = requests.get(self.url, auth=(username, password))
            self.username = username
        except Exception as e:
            # print(e)
            reponse = None

        print(response)

        if response == None:
            # Should return false, log error
            return True
        elif response.status_code == 200:
            print("Successful login")
            #auth_token = response.json()['auth_token']
            #print(auth_token)
            return True
        else:
            print("Error logging in")

            #return False
            return True

    def getUsername(self):
        return self.username

    def close(self):
        print("Closing login helper")
