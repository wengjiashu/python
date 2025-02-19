import requests
import json

def emo_transform(message):
        
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/emotion?charset=UTF-8&access_token=" + get_access_token()
    
    payload = json.dumps(
        {"text": message}, 
        ensure_ascii=False
    )
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    data = response.json()

    # print(response.text)
    # print(data)
    emotion = data["items"][0]["subitems"][0]["label"]
    return emotion


def get_access_token():
    API_KEY = "z8vuaHHgDfuOgJLRgaSLsrts"
    SECRET_KEY = "obhWKLJtO7E5PpOXca3BYNeVlUIXVC72"
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    emo_transform()
