#!/bin/sh
# INO Project — container entrypoint.
# Renders nginx.conf with the runtime $PORT (Cloud Run / App Runner pattern),
# then execs the upstream nginx command.

set -e

: "${PORT:=3403}"
export PORT

TEMPLATE=/etc/nginx/templates/default.conf.template
TARGET=/etc/nginx/conf.d/default.conf

if [ -f "$TEMPLATE" ]; then
  envsubst '${PORT}' < "$TEMPLATE" > "$TARGET"
fi

echo "[ino] starting nginx on port ${PORT}"
exec "$@"
