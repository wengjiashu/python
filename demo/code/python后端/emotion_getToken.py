
import requests
import json


def main():
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=z8vuaHHgDfuOgJLRgaSLsrts&client_secret=obhWKLJtO7E5PpOXca3BYNeVlUIXVC72"
#   Token 25.3aa94fd7e89179b95a9efe058446279b.315360000.2053761411.282335-117214922
#   expires_in:2592000

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()