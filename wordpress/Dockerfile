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
    # Keep extracting any nested ZIPs until no more remain
    for attempt in 1 2 3; do \
        INNER_ZIP=$(find /tmp/wp-fm-extract -name '*.zip' -type f | head -1); \
        if [ -z "$INNER_ZIP" ]; then break; fi; \
        echo "[*] Attempt $attempt: extracting inner zip: $INNER_ZIP"; \
        unzip -o "$INNER_ZIP" -d "$(dirname "$INNER_ZIP")"; \
        rm -f "$INNER_ZIP"; \
    done; \
    # The plugin main file is file_folder_manager.php (not wp-file-manager.php)
    MAIN_PHP=$(find /tmp/wp-fm-extract -name 'file_folder_manager.php' -type f | head -1); \
    if [ -z "$MAIN_PHP" ]; then \
        MAIN_PHP=$(find /tmp/wp-fm-extract -name 'wp-file-manager.php' -type f | head -1); \
    fi; \
    if [ -z "$MAIN_PHP" ]; then \
        echo "ERROR: Could not find plugin main PHP file"; \
        find /tmp/wp-fm-extract -type f -name '*.php' | sort; \
        exit 1; \
    fi; \
    PLUGIN_SRC=$(dirname "$MAIN_PHP"); \
    echo "[+] Found plugin at: $PLUGIN_SRC (main: $(basename $MAIN_PHP))"; \
    rm -rf /usr/src/wordpress/wp-content/plugins/wp-file-manager; \
    cp -a "$PLUGIN_SRC" /usr/src/wordpress/wp-content/plugins/wp-file-manager; \
    rm -rf /tmp/wp-fm-extract; \
    # WordPress needs the plugin registered as wp-file-manager/file_folder_manager.php
    DEST=/usr/src/wordpress/wp-content/plugins/wp-file-manager; \
    chown -R www-data:www-data "$DEST"; \
    echo "[+] WP File Manager installed. Key files:"; \
    ls "$DEST"/file_folder_manager.php 2>/dev/null || ls "$DEST"/wp-file-manager.php 2>/dev/null; \
    ls "$DEST"/lib/php/connector.minimal.php

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
