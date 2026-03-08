FROM wordpress:6.4-apache

ENV DEBIAN_FRONTEND=noninteractive

# Install system tools (python3 is already in the base image — do NOT reinstall it)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    sudo \
    unzip \
    wget \
    curl \
    openssh-server \
    iputils-ping \
    net-tools \
    libcap2-bin \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install pip via get-pip.py and then install reportlab
RUN wget -q https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py \
    && python3 /tmp/get-pip.py --break-system-packages \
    && rm /tmp/get-pip.py \
    && python3 -m pip install --break-system-packages reportlab

# Install WP-CLI for automated WordPress setup
RUN wget -q https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -O /usr/local/bin/wp \
    && chmod +x /usr/local/bin/wp

# Install WP File Manager plugin from local ZIP (reproducible/offline build)
COPY assets/wp-file-manager-6.0.zip /tmp/wp-file-manager-local.zip
RUN set -e; \
    mkdir -p /usr/src/wordpress/wp-content/plugins; \
    if [ ! -s /tmp/wp-file-manager-local.zip ]; then \
        echo "ERROR: wp-file-manager-6.0.zip not found in wordpress/assets/"; \
        exit 1; \
    fi; \
    echo "[*] Installing WP File Manager from local ZIP..."; \
    unzip -o /tmp/wp-file-manager-local.zip -d /tmp/wp-fm-extract; \
    rm -f /tmp/wp-file-manager-local.zip; \
    echo "[*] Outer ZIP contents:"; \
    find /tmp/wp-fm-extract -type f | head -20; \
    # Keep extracting any nested zips until we find the plugin PHP or run out of zips
    for attempt in 1 2 3; do \
        MAIN_PHP=$(find /tmp/wp-fm-extract -name 'wp-file-manager.php' -type f | head -1); \
        if [ -n "$MAIN_PHP" ]; then break; fi; \
        INNER_ZIP=$(find /tmp/wp-fm-extract -name '*.zip' -type f | head -1); \
        if [ -z "$INNER_ZIP" ]; then break; fi; \
        echo "[*] Attempt $attempt: Found inner zip: $INNER_ZIP — extracting..."; \
        unzip -o "$INNER_ZIP" -d /tmp/wp-fm-inner; \
        rm -f "$INNER_ZIP"; \
        cp -a /tmp/wp-fm-inner/. /tmp/wp-fm-extract/ 2>/dev/null || true; \
        rm -rf /tmp/wp-fm-inner; \
        echo "[*] Contents after extraction:"; \
        find /tmp/wp-fm-extract -type f -name '*.php' | head -10; \
    done; \
    MAIN_PHP=$(find /tmp/wp-fm-extract -name 'wp-file-manager.php' -type f | head -1); \
    if [ -z "$MAIN_PHP" ]; then \
        echo "ERROR: Could not find wp-file-manager.php after extracting all ZIPs"; \
        echo "Full directory listing:"; \
        find /tmp/wp-fm-extract -type f | sort; \
        exit 1; \
    fi; \
    PLUGIN_SRC=$(dirname "$MAIN_PHP"); \
    echo "[+] Found plugin at: $PLUGIN_SRC"; \
    rm -rf /usr/src/wordpress/wp-content/plugins/wp-file-manager; \
    cp -a "$PLUGIN_SRC" /usr/src/wordpress/wp-content/plugins/wp-file-manager; \
    rm -rf /tmp/wp-fm-extract; \
    chown -R www-data:www-data /usr/src/wordpress/wp-content/plugins/wp-file-manager; \
    echo "[+] WP File Manager installed successfully"; \
    echo "[+] Plugin files:"; \
    ls /usr/src/wordpress/wp-content/plugins/wp-file-manager/wp-file-manager.php; \
    find /usr/src/wordpress/wp-content/plugins/wp-file-manager -name 'connector.minimal.php' -type f | head -1

# Create marketing user with flag in home directory
RUN useradd -m -s /bin/bash marketing \
    && echo "marketing:Marketing@2026" | chpasswd \
    && mkdir -p /home/marketing/Documents \
    && echo "FLAG{SSH_CREDENTIAL_REUSE_marketing_2026}" > /home/marketing/flag.txt \
    && chown -R marketing:marketing /home/marketing

# Create devops user (for /etc/passwd enumeration)
RUN useradd -m -s /bin/bash devops \
    && echo "devops:D3v0ps@Hexa!" | chpasswd \
    && mkdir -p /home/devops \
    && echo "FLAG{ENUMERATION_devops_user_found}" > /home/devops/flag.txt \
    && chown -R devops:devops /home/devops

# Enable SSH
RUN mkdir -p /var/run/sshd
RUN echo 'root:rootpass' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Privilege Escalation Setup — find actual python3 binary
RUN PYTHON3_BIN=$(readlink -f $(which python3)) && setcap cap_setuid+ep "$PYTHON3_BIN"

# Place root flag
RUN echo "FLAG{ROOT_PRIVESC_python3_cap_setuid}" > /root/flag.txt \
    && chmod 600 /root/flag.txt

# Copy corporate site, PDF generator, and setup scripts
COPY corporate-site/ /corporate-site/
COPY generate_pdfs.py /generate_pdfs.py

# Copy setup script and fix Windows line endings
COPY 01_setup.sh /01_setup.sh
RUN sed -i 's/\r$//' /01_setup.sh && chmod +x /01_setup.sh \
    && sed -i 's/\r$//' /generate_pdfs.py

# Copy custom entrypoint and fix Windows line endings
COPY custom-entrypoint.sh /custom-entrypoint.sh
RUN sed -i 's/\r$//' /custom-entrypoint.sh && chmod +x /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["apache2-foreground"]

EXPOSE 80 22
