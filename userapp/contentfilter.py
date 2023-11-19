# This is an example of calling the content filter function
# in ruby on rails. This returns the content filters for a given
# user, however the user credentials portion hasn't been implemented
# in python yet bc I don't know how
import requests

def get_article(auth0_id):
    # url = f"http://localhost:3000/api/v1/auth0s/" # {auth0_id}"
    url = f"http://localhost:3000/api/v1/auth0s/{auth0_id}/content_filters/" # {auth0_id}"
    print("url: ",url)
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching content filter: {response.status_code}")
        return None

# Example usage
#auth0_id = "1"  # Replace with the ID of the article you want to retrieve
auth0_id = "auth0|655331b127a4232eddd25768"
#auth0_id = "655331b127a4232eddd25768"
article_data = get_article(auth0_id)

if article_data:
    print(article_data)

