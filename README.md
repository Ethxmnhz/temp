# HexaExam — HexaDynamics Vulnerable WordPress Lab

A self-contained, production-ready vulnerable WordPress lab for security training. Runs automatically on any machine with Docker — no manual configuration required.

## Quick Start (Any PC)

```bash
# 1. Build and start (fully automatic)
docker-compose up --build -d

# 2. Wait ~60 seconds, then verify
docker-compose ps
docker logs hs_wp_web --tail 50

# 3. Access the lab
#    Corporate site: http://localhost:8080
#    WordPress:      http://localhost:8080/intranet
#    SSH:            ssh marketing@localhost -p 2222
```

Everything sets up automatically:
- MySQL database with flags
- WordPress with admin user
- WP File Manager 6.0 (vulnerable) plugin installed & activated
- Git repo with leaked credentials in history
- SSH with password auth
- Python3 privilege escalation capability
- 8 flags planted across the attack chain

## What Gets Set Up Automatically

| Component | Details |
|-----------|---------|
| WordPress 6.4 | Auto-installed at `/intranet/` with admin account |
| WP File Manager 6.0 | Vulnerable plugin (CVE-2020-25213) auto-installed |
| Exposed .git | Leaked base64 credentials in commit history |
| MySQL 5.7 | WordPress DB + hidden `hexa_internal_notes` table |
| SSH Server | Port 2222, password auth enabled |
| System Users | `marketing`, `devops` with flags in home dirs |
| Python3 Capability | `cap_setuid=ep` for privilege escalation |
| Corporate PDFs | Auto-generated brochures and internal docs |

## Flags (8 Total)

| # | Phase | Flag |
|---|-------|------|
| 1 | Git History | `FLAG{GIT_HISTORY_EXPOSED_creds_leaked}` |
| 2 | RCE (File Manager) | `FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}` |
| 3 | wp-config.php | `FLAG{WP_CONFIG_DB_CREDS_EXPOSED}` |
| 4 | DB (wp_options) | `FLAG{DATABASE_ENUMERATION_wp_options}` |
| 5 | DB (hidden table) | `FLAG{DATABASE_DIRECT_ACCESS_hexa_internal}` |
| 6 | SSH Pivot | `FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}` |
| 7 | User Enum | `FLAG{ENUMERATION_devops_user_found}` |
| 8 | Root Privesc | `FLAG{ROOT_PRIVESC_python3_cap_setuid}` |

## Attack Chain

```
Recon → .git exposure → Base64 decode → WP admin login
→ CVE-2020-25213 RCE → wp-config.php → DB creds
→ MySQL enum → Password crack → SSH pivot
→ Python3 cap_setuid → Root
```

## Full Walkthrough

See [walkthrough.md](walkthrough.md) for complete step-by-step exploitation guide with exact commands for every phase.

## Credentials Reference (Instructor Only)

| Service | Username | Password |
|---------|----------|----------|
| WordPress Admin | admin | SuperSecret@2026 |
| WordPress Editor | marketing_user | Marketing@2026 |
| MySQL | wp_user | WpDb@2026! |
| SSH (marketing) | marketing | Marketing@2026 |
| SSH (devops) | devops | D3v0ps@Hexa! |

## Distribution

```bash
# Save portable image (no Docker Hub needed)
make save
# Produces: hexaexam-wordpress.tar

# On target machine:
docker load -i hexaexam-wordpress.tar
docker-compose up -d
```

## Cleanup

```bash
docker-compose down -v
docker rmi hexaexam/wordpress:latest
```

## Requirements

- Docker Engine / Docker Desktop
- ~2GB disk space
- Ports 8080 and 2222 available

