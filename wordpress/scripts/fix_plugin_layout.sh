#!/bin/bash
PLUGIN_DIR="/var/www/html/intranet/wp-content/plugins/wp-file-manager"
if [ -d "$PLUGIN_DIR" ]; then
  echo "Normalizing plugin layout for $PLUGIN_DIR"
  if [ -d "$PLUGIN_DIR/wp-file-manager" ]; then
    echo "Flattening nested wp-file-manager directory"
    mv "$PLUGIN_DIR"/wp-file-manager/* "$PLUGIN_DIR"/ || true
    rmdir "$PLUGIN_DIR"/wp-file-manager || true
  fi
  for z in "$PLUGIN_DIR"/*.zip; do
    if [ -f "$z" ]; then
      echo "Unpacking nested zip $z"
      unzip -o "$z" -d "$PLUGIN_DIR" && rm -f "$z" || true
    fi
  done
  chown -R www-data:www-data "$PLUGIN_DIR"
else
  echo "Plugin dir not present: $PLUGIN_DIR"
fi
