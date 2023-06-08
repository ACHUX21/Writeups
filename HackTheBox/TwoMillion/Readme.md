 </br>[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=6A0DAD&width=435&lines=TwoMillion)](https://git.io/typing-svg)
</br>
<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic1.png" alt="Alt Text">
</a>
</br>
</br>
</br>
## Nmap-scan
</br>

First, let's initiate a quick scan utilizing nmap.


<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic2.png" alt="Alt Text">
</a>
</br>

It appears that we need to include "2million.htb" in our hosts file

```bash
echo "10.10.11.221 2million.htb" >> /etc/hosts
```
</br>

## Trying to have access

Upon visiting the website, I discovered it's an outdated version of the HackTheBox platform. To gain access, I attempted to log in using the default credentials, but unfortunately, I received an error message indicating that the user not found.
<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic3.png" alt="Alt Text">
</a>
</br>
While exploring the website, I discovered that I can join the platform by obtaining an invite code.
</br>

`http://2million.htb/invite`

</br>
I came across a JavaScript code that contains some intriguing elements. 
</br>

`/js/inviteapi.min.js`

<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic4.png" alt="Alt Text">
</a>

</br>
I am interested in generating my own invite code as well.
</br>
I will examine the endpoint "/api/v1/invite/how/to/generate" to gather more information.
</br>


<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic6.png" alt="Alt Text">
</a>
</br>

After decoding the ROT13 cipher, we discovered the method to generate our own invite code.


</br>
<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic7.png" alt="Alt Text">
</a>

Let's proceed with generating our invite code using the discovered method

</br>
<a href="https://app.hackthebox.com/machines/TwoMillion">
  <img src="pic5.png" alt="Alt Text">
</a>
</br>
Since the invite is encoded using base64, it should be easy to obtain one.

</br>

```bash
curl -s -X POST http://2million.htb/api/v1/invite/generate | jq .data.code -r |base64 -d
```

## Gain administrative

</br>

After logging in with the provided invite code, I will attempt to brute force certain endpoints to obtain more valuable information and enhance our capabilities.





















