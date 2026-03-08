#!/bin/bash
set -e

echo "============================================"
echo "  HexaDynamics Lab — Container Starting"
echo "============================================"

# Start SSH daemon
service ssh start

# --- WordPress file setup ---
cd /var/www/html

# Only copy WP files if neither root nor /intranet has them yet
if [ ! -f /var/www/html/wp-includes/version.php ] && [ ! -f /var/www/html/intranet/wp-includes/version.php ]; then
    echo "[*] Copying WordPress files to /var/www/html..."
    tar cf - --directory=/usr/src/wordpress --owner=www-data --group=www-data . | tar xf -
    echo "[+] WordPress files copied."
else
    echo "[+] WordPress files already present, skipping copy."
fi

# Generate wp-config.php if missing in both locations
if [ ! -s /var/www/html/wp-config.php ] && [ ! -s /var/www/html/intranet/wp-config.php ]; then
    echo "[*] Generating wp-config.php..."
    for wpConfigDocker in \
        /var/www/html/wp-config-docker.php \
        /usr/src/wordpress/wp-config-docker.php \
    ; do
        if [ -s "$wpConfigDocker" ]; then
            awk '
                /put your unique phrase here/ {
                    cmd = "head -c1m /dev/urandom | sha1sum | cut -d\\  -f1"
                    cmd | getline str
                    close(cmd)
                    gsub("put your unique phrase here", str)
                }
                { print }
            ' "$wpConfigDocker" > /var/www/html/wp-config.php
            chown www-data:www-data /var/www/html/wp-config.php || true
            break
        fi
    done
    echo "[+] wp-config.php generated."
fi

# Run lab setup (idempotent)
echo "[*] Running lab setup..."
/01_setup.sh

echo "============================================"
echo "  HexaDynamics Lab — Ready!"
echo "  Web:  http://localhost:8080"
echo "  WP:   http://localhost:8080/intranet"
echo "  SSH:  ssh marketing@localhost -p 2222"
echo "============================================"

# Start Apache in the foreground
exec "$@"
