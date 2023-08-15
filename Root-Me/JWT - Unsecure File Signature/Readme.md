[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=8a00a4&width=435&lines=JWT-1)](https://git.io/typing-svg)

</br>

![banner](https://github.com/ACHUX21/Writeups/assets/130113878/e12382f1-a20c-4601-aad4-a9f311356fc9)

### Statement

```
A previous Root Me administrator is trying to replicate the website after being banned for sharing
challenge solutions.

Try to find out if he is hiding any other flags on his new website.
```

### Web-View
![web-view](https://github.com/ACHUX21/Writeups/assets/130113878/3da1e468-7b0c-409c-bc63-14eb8e139752)
</br>

I'm having difficulty deciphering the location of Buttons on this website.

Upon inspecting the page's source code, I discovered certain endpoints that seem intriguing.

```
/admin
static/challs/htmllecture.html
static/challs/irc.html
static/challs/obfu6.html
static/https://www.youtube.com/watch?v=ZYrmrflWBmY
static/challs/samboxv5.html
```
### /admin

Upon accessing the 'admin' endpoint at `http://challenge01.root-me.org:59081/admin`, I encountered an 'Unauthorized' error.

```json
{"Unauthorized":"You are not admin !"}
```

### burp

I attempted to intercept the request using Burp in order to uncover more information.

![Burp-request](https://github.com/ACHUX21/Writeups/assets/130113878/fde8ca6d-e02e-4e97-9c17-895ae42727cf)

It appears that the situation involves JWT (JSON Web Tokens).


To gain a clearer understanding, I searched for information on jwt.io to access helpful visualizations and explanations.

### [JWT.IO](https://jwt.io/)


![jwt-io](https://github.com/ACHUX21/Writeups/assets/130113878/91d1b72b-d9db-49f6-951e-2509b73de49f)

While encoding the JWT, I observed that it utilizes the HS256 (HMAC_SHA256) algorithm along with a "kid" (Key ID) parameter.

The "kid" (key ID) claim is a string that signifies the key responsible for digitally signing the JWT.

If you're interested in delving deeper into attacks involving the "kid" parameter in JWTs, you can find more information here: [kid-parameter](https://portswigger.net/web-security/jwt#injecting-self-signed-jwts-via-the-kid-parameter)



Afterwards, I proceeded to modify the JWT by signing it with a particular secret key and conducting attacks on the JWT "kid" header,
 such as SQL injection and OS injection. 
Eventually, I identified a path traversal vulnerability in the "kid" header. 
I attempted to alter the "kid" header to "/dev/null" and sign the JWT with an empty secret key.

![empty-sign](https://github.com/ACHUX21/Writeups/assets/130113878/32fba5ca-a326-4f55-b5cc-bf6b626ac6bf)

</br>

![path-traversal](https://github.com/ACHUX21/Writeups/assets/130113878/a2a39c96-618b-4f2f-828e-0ccf479d7be4)


However, a complication arose: there seems to be a replace function or a similar mechanism in place that eliminates our "../" sequences.

Yet, we can overcome this by using the pattern `....//....//....//` to bypass the restriction and continue with our intended manipulation.

![final_sol](https://github.com/ACHUX21/Writeups/assets/130113878/b92fdb13-7af9-454a-b882-1c0c9c92071a)



As a result of these efforts, we successfully obtained the flag! 


![flag](https://github.com/ACHUX21/Writeups/assets/130113878/8c75a20d-8d09-4360-b427-60f1d8c9198c)



have Fun 💜
