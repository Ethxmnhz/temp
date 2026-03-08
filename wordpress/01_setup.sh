#!/bin/bash
set -e

echo "[*] Starting HexaDynamics lab setup..."

# ── Detect if WordPress is already moved to /intranet (idempotent restarts) ──
if [ -f /var/www/html/intranet/wp-includes/version.php ]; then
    WP_PATH="/var/www/html/intranet"
    ALREADY_MOVED=true
    echo "[+] WordPress already at /intranet (restart detected)."
else
    WP_PATH="/var/www/html"
    ALREADY_MOVED=false
fi

cd "$WP_PATH"

# ── Wait for MySQL ──
echo "[*] Waiting for MySQL..."
RETRIES=0
MAX_RETRIES=60
until php -r "
  \$c = @new mysqli(
    getenv('WORDPRESS_DB_HOST'),
    getenv('WORDPRESS_DB_USER'),
    getenv('WORDPRESS_DB_PASSWORD'),
    getenv('WORDPRESS_DB_NAME')
  );
  if (\$c->connect_error) exit(1);
  \$c->close();
" 2>/dev/null; do
    RETRIES=$((RETRIES+1))
    if [ $RETRIES -ge $MAX_RETRIES ]; then
        echo "[!] MySQL not ready after ${MAX_RETRIES} attempts. Aborting."
        exit 1
    fi
    echo "    Waiting for database... (${RETRIES}/${MAX_RETRIES})"
    sleep 3
done
echo "[+] MySQL is ready."

# ── Install WordPress via WP-CLI ──
echo "[*] Installing WordPress..."
if ! wp core is-installed --path="$WP_PATH" --allow-root 2>/dev/null; then
    wp core install \
        --path="$WP_PATH" \
        --url="http://localhost:8080/intranet" \
        --title="HexaDynamics Intranet" \
        --admin_user=admin \
        --admin_password='SuperSecret@2026' \
        --admin_email=admin@hexadynamics.local \
        --skip-email \
        --allow-root
    echo "[+] WordPress installed."
else
    echo "[+] WordPress already installed."
fi

# ── Create marketing_user (idempotent) ──
echo "[*] Creating marketing_user..."
if ! wp user get marketing_user --path="$WP_PATH" --allow-root >/dev/null 2>&1; then
    wp user create marketing_user marketing@hexadynamics.local \
        --user_pass='Marketing@2026' \
        --role=editor \
        --path="$WP_PATH" \
        --allow-root
    echo "[+] marketing_user created."
else
    echo "[+] marketing_user already exists."
fi

# ── Move WordPress into /intranet subdirectory (first run only) ──
if [ "$ALREADY_MOVED" = false ]; then
    echo "[*] Moving WordPress to /intranet..."
    cd /var/www/html
    mkdir -p /tmp/wp-hold
    cp -a /var/www/html/. /tmp/wp-hold/
    rm -rf /var/www/html/*
    mkdir -p /var/www/html/intranet
    cp -a /tmp/wp-hold/. /var/www/html/intranet/
    rm -rf /tmp/wp-hold
    WP_PATH="/var/www/html/intranet"

    wp option update siteurl 'http://localhost:8080/intranet' --path="$WP_PATH" --allow-root
    wp option update home 'http://localhost:8080/intranet' --path="$WP_PATH" --allow-root
    echo "[+] WordPress moved to /intranet."
else
    echo "[+] Skipping /intranet move (already done)."
fi

# ── Deploy corporate landing page ──
echo "[*] Deploying corporate landing page..."
cp /corporate-site/index.html /var/www/html/index.html
mkdir -p /var/www/html/assets

# ── Initialize Git repo with leaked credentials (exposed .git) ──
echo "[*] Initializing exposed .git repository..."
cd /var/www/html
set +e
if [ ! -d /var/www/html/.git ]; then
    # Configure git globally to avoid safe.directory issues
    git config --global init.defaultBranch main
    git config --global user.email "devops@hexadynamics.local"
    git config --global user.name "DevOps Team"
    git config --global --add safe.directory /var/www/html

    git init /var/www/html

    # First commit: migration notes with leaked creds
    cat > /var/www/html/migration_notes.txt << 'GITEOF'
HexaDynamics Infrastructure Migration Notes
============================================
Date: 2025-11-15
Author: Vikram Singh (DevOps Lead)

Temporary WP admin creds for testing:
YWRtaW46U3VwZXJTZWNyZXRAMjAyNg==

FLAG{GIT_HISTORY_EXPOSED_creds_leaked}

TODO: Remove these creds before production deployment.
GITEOF

    git -C /var/www/html add migration_notes.txt
    git -C /var/www/html commit -m "Added migration notes during infrastructure migration"

    # Second commit: remove from working tree but keep in git history
    rm -f /var/www/html/migration_notes.txt
    git -C /var/www/html add migration_notes.txt
    git -C /var/www/html commit -m "Cleaned up migration artifacts — removed temp creds"

    # Verify commits exist
    COMMIT_COUNT=$(git -C /var/www/html rev-list --count HEAD 2>/dev/null || echo 0)
    if [ "$COMMIT_COUNT" -ge 2 ]; then
        echo "[+] Git repository initialized with $COMMIT_COUNT commits (credential history intact)."
    else
        echo "[!] WARNING: Git repo has only $COMMIT_COUNT commits — history may be incomplete!"
    fi
else
    echo "[+] Git repository already exists."
fi
set -e

# ── Rewrite wp-config.php with hardcoded credentials (visible during post-exploitation) ──
echo "[*] Rewriting wp-config.php with hardcoded credentials..."
if [ -f "$WP_PATH/wp-config.php" ]; then
    cat > "$WP_PATH/wp-config.php" << 'WPCONFIGEOF'
<?php
/**
 * The base configuration for WordPress (HexaDynamics Intranet)
 * Generated during Docker migration — Nov 2025
 */

// ** Database settings ** //
define( 'DB_NAME', 'wordpress' );
define( 'DB_USER', 'wp_user' );
define( 'DB_PASSWORD', 'WpDb@2026!' );
define( 'DB_HOST', 'db' );
define( 'DB_CHARSET', 'utf8' );
define( 'DB_COLLATE', '' );

/**
 * Authentication unique keys and salts.
 */
define( 'AUTH_KEY',         'hexa-auth-key-2026-rAnDoM' );
define( 'SECURE_AUTH_KEY',  'hexa-secure-auth-key-2026-XyZ' );
define( 'LOGGED_IN_KEY',    'hexa-logged-in-key-2026-AbC' );
define( 'NONCE_KEY',        'hexa-nonce-key-2026-DeF' );
define( 'AUTH_SALT',        'hexa-auth-salt-2026-GhI' );
define( 'SECURE_AUTH_SALT', 'hexa-secure-salt-2026-JkL' );
define( 'LOGGED_IN_SALT',   'hexa-logged-salt-2026-MnO' );
define( 'NONCE_SALT',       'hexa-nonce-salt-2026-PqR' );

$table_prefix = 'wp_';

define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */
if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}
require_once ABSPATH . 'wp-settings.php';

/* FLAG{WP_CONFIG_DB_CREDS_EXPOSED} */
WPCONFIGEOF
    chown www-data:www-data "$WP_PATH/wp-config.php"
    echo "[+] wp-config.php rewritten with hardcoded credentials and flag."
fi

# ── Plant flag accessible via RCE (webshell/file manager exploitation) ──
mkdir -p "$WP_PATH/wp-content/uploads"
echo "FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}" > "$WP_PATH/wp-content/uploads/.flag.txt"

# ── Plant flag in database via WP option (DB enumeration phase) ──
if ! wp option get hexa_flag --path="$WP_PATH" --allow-root >/dev/null 2>&1; then
    wp option add hexa_flag 'FLAG{DATABASE_ENUMERATION_wp_options}' --path="$WP_PATH" --allow-root 2>/dev/null || true
fi

# ── Fix permissions ──
chown -R www-data:www-data /var/www/html

# ── Generate corporate PDF documents ──
echo "[*] Generating corporate PDF documents..."
python3 /generate_pdfs.py /var/www/html
echo "[+] PDF documents generated."

# ── Fix permissions after PDF generation ──
chown -R www-data:www-data /var/www/html
chown -R marketing:marketing /home/marketing

# ── Configure Apache (expose .git, enable directory listing) ──
echo "[*] Configuring Apache..."
cat > /etc/apache2/conf-available/hexadynamics.conf << 'APACHEEOF'
<Directory /var/www/html>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

<Directory /var/www/html/.git>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>

<Directory /var/www/html/assets>
    Options Indexes FollowSymLinks
    Require all granted
</Directory>
APACHEEOF
a2enconf hexadynamics 2>/dev/null || true
a2enmod rewrite 2>/dev/null || true

# ── Normalize and activate WP File Manager plugin ──
echo "[*] Setting up WP File Manager plugin..."
PLUGIN_DIR="$WP_PATH/wp-content/plugins/wp-file-manager"

# If plugin directory doesn't exist, copy from source
if [ ! -d "$PLUGIN_DIR" ]; then
    if [ -d /usr/src/wordpress/wp-content/plugins/wp-file-manager ]; then
        echo "[*] Copying plugin from image source..."
        cp -a /usr/src/wordpress/wp-content/plugins/wp-file-manager "$PLUGIN_DIR"
    fi
fi

if [ -d "$PLUGIN_DIR" ]; then
    # Flatten any nested wp-file-manager directory
    if [ -d "$PLUGIN_DIR/wp-file-manager" ]; then
        echo "[*] Flattening nested wp-file-manager directory..."
        cp -a "$PLUGIN_DIR"/wp-file-manager/* "$PLUGIN_DIR"/ 2>/dev/null || true
        cp -a "$PLUGIN_DIR"/wp-file-manager/.* "$PLUGIN_DIR"/ 2>/dev/null || true
        rm -rf "$PLUGIN_DIR"/wp-file-manager
    fi

    # Unpack any nested zip files
    for z in "$PLUGIN_DIR"/*.zip; do
        if [ -f "$z" ]; then
            echo "[*] Unpacking nested zip: $z"
            unzip -o "$z" -d "$PLUGIN_DIR" && rm -f "$z" || true
        fi
    done

    # Fix double-nesting after zip extraction
    if [ -d "$PLUGIN_DIR/wp-file-manager" ]; then
        echo "[*] Flattening post-unzip nested directory..."
        cp -a "$PLUGIN_DIR"/wp-file-manager/* "$PLUGIN_DIR"/ 2>/dev/null || true
        cp -a "$PLUGIN_DIR"/wp-file-manager/.* "$PLUGIN_DIR"/ 2>/dev/null || true
        rm -rf "$PLUGIN_DIR"/wp-file-manager
    fi

    chown -R www-data:www-data "$PLUGIN_DIR"

    # Verify plugin main file exists (this version uses file_folder_manager.php)
    if [ -f "$PLUGIN_DIR/file_folder_manager.php" ]; then
        echo "[+] Plugin main file found: file_folder_manager.php"
    elif [ -f "$PLUGIN_DIR/wp-file-manager.php" ]; then
        echo "[+] Plugin main file found: wp-file-manager.php"
    else
        echo "[!] WARNING: Plugin main PHP file NOT found!"
        echo "    Contents of $PLUGIN_DIR:"
        ls -la "$PLUGIN_DIR"/ 2>/dev/null || true
    fi

    # Ensure connector.minimal.php exists (CVE-2020-25213 endpoint)
    if [ -f "$PLUGIN_DIR/lib/php/connector.minimal.php" ]; then
        echo "[+] connector.minimal.php found — exploit endpoint ready."
    else
        echo "[!] WARNING: connector.minimal.php NOT found at $PLUGIN_DIR/lib/php/"
        echo "    Searching for it..."
        CONNECTOR=$(find "$PLUGIN_DIR" -name 'connector.minimal.php' -type f 2>/dev/null | head -1)
        if [ -n "$CONNECTOR" ]; then
            echo "[+] Found at: $CONNECTOR"
            mkdir -p "$PLUGIN_DIR/lib/php"
            cp "$CONNECTOR" "$PLUGIN_DIR/lib/php/connector.minimal.php"
        else
            echo "[!] CRITICAL: connector.minimal.php not found anywhere in plugin!"
        fi
    fi

    # Ensure lib/files directory exists and is writable (upload destination for exploit)
    mkdir -p "$PLUGIN_DIR/lib/files"
    chown -R www-data:www-data "$PLUGIN_DIR/lib/files"
    chmod 777 "$PLUGIN_DIR/lib/files"
    echo "[+] lib/files directory ready for uploads."
else
    echo "[!] Plugin directory not found at $PLUGIN_DIR"
fi

# ── Activate WP File Manager plugin ──
echo "[*] Activating WP File Manager plugin..."
ACTIVATION_RETRIES=0
while [ $ACTIVATION_RETRIES -lt 3 ]; do
    if wp plugin is-installed wp-file-manager --path="$WP_PATH" --allow-root 2>/dev/null; then
        wp plugin activate wp-file-manager --path="$WP_PATH" --allow-root 2>/dev/null || true
        echo "[+] wp-file-manager activated."
        break
    else
        ACTIVATION_RETRIES=$((ACTIVATION_RETRIES+1))
        echo "[*] Plugin not detected by WP-CLI, retry ${ACTIVATION_RETRIES}/3..."
        sleep 2
    fi
done

if [ $ACTIVATION_RETRIES -ge 3 ]; then
    echo "[!] wp-file-manager could not be activated via WP-CLI."
    echo "    Attempting direct database activation..."
    # Force-activate via database as fallback
    wp option get active_plugins --path="$WP_PATH" --allow-root 2>/dev/null || true
    php -r "
        define('ABSPATH', '${WP_PATH}/');
        require_once('${WP_PATH}/wp-config.php');
        require_once('${WP_PATH}/wp-load.php');
        \$active = get_option('active_plugins', array());
        # Check both possible main file names
        \$found = false;
        foreach (['wp-file-manager/file_folder_manager.php', 'wp-file-manager/wp-file-manager.php'] as \$p) {
            if (in_array(\$p, \$active)) { \$found = true; break; }
        }
        if (!\$found) {
            \$main = file_exists('${WP_PATH}/wp-content/plugins/wp-file-manager/file_folder_manager.php')
                ? 'wp-file-manager/file_folder_manager.php'
                : 'wp-file-manager/wp-file-manager.php';
            \$active[] = \$main;
            update_option('active_plugins', \$active);
            echo '[+] Plugin force-activated via database.';
        } else {
            echo '[+] Plugin already active.';
        }
    " 2>/dev/null || echo "[!] Database activation also failed. Check plugin files."
fi

# ── Verify final plugin status ──
echo "[*] Plugin verification:"
wp plugin list --path="$WP_PATH" --allow-root 2>/dev/null | grep -i file-manager || echo "    wp-file-manager not in plugin list"

# ── Final permission fix ──
chown -R www-data:www-data /var/www/html

echo ""
echo "============================================"
echo "  HexaDynamics Lab Setup Complete!"
echo "============================================"
echo ""
echo "  Flags planted at:"
echo "    1. Git history    - FLAG{GIT_HISTORY_EXPOSED_creds_leaked}"
echo "    2. RCE upload dir - FLAG{RCE_WP_FILE_MANAGER_6_CVE_2020_25213}"
echo "    3. wp-config.php  - FLAG{WP_CONFIG_DB_CREDS_EXPOSED}"
echo "    4. DB wp_options  - FLAG{DATABASE_ENUMERATION_wp_options}"
echo "    5. SSH marketing  - FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}"
echo "    6. Privesc root   - FLAG{ROOT_PRIVESC_python3_cap_setuid}"
echo "    7. devops home    - FLAG{ENUMERATION_devops_user_found}"
echo ""
echo "[+] Setup complete."
