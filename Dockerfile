# INO Project — production-ready static dashboard image.
# Designed for portability across local Docker, GCP Cloud Run, and AWS ECS/Fargate/App Runner.
#
# Highlights
#   * Self-contained: app/ is COPY-ed in (no bind mount required in production).
#   * Dynamic $PORT: nginx.conf is rendered at container start. Cloud Run /
#     App Runner override $PORT at deploy time; pass `--port 3403` to keep
#     the default consistent across NAS and cloud.
#   * Non-root: runs as the built-in nginx user.
#   * Small surface: nginx:alpine ~= 50 MB compressed.
#   * HEALTHCHECK on /healthz (used by ECS, App Runner, k8s readiness probes).

FROM nginx:1.27-alpine

# Default port — overridable at runtime via $PORT.
ENV PORT=3403

# Install gettext for envsubst (renders nginx.conf with $PORT).
RUN apk add --no-cache gettext curl tzdata \
    && cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && echo "Asia/Seoul" > /etc/timezone

# Static site assets.
COPY app/ /usr/share/nginx/html/

# Nginx template — rendered to /etc/nginx/conf.d/default.conf at start.
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Entrypoint: render template, then exec nginx in foreground.
COPY docker-entrypoint.sh /docker-entrypoint-ino.sh
RUN chmod +x /docker-entrypoint-ino.sh

# Cloud Run/App Runner ignore EXPOSE but it's good documentation.
EXPOSE 3403

# Container-level healthcheck (ECS/Compose; Cloud Run uses its own probes).
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -fsS "http://127.0.0.1:${PORT:-3403}/healthz" || exit 1

ENTRYPOINT ["/docker-entrypoint-ino.sh"]
CMD ["nginx", "-g", "daemon off;"]
