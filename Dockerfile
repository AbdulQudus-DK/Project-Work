
# ---------------------------------------------------------
# Base image — includes n8n binary already
# ---------------------------------------------------------
FROM n8nio/n8n:latest

# ---------------------------------------------------------
# Set timezone (optional)
# ---------------------------------------------------------
ENV GENERIC_TIMEZONE=Africa/Lagos

# ---------------------------------------------------------
# Basic Auth for n8n UI
# ---------------------------------------------------------
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=strong-password

# ---------------------------------------------------------
# Database (Neon)
# Connection URL will come from Render environment variables
# ---------------------------------------------------------
ENV DB_TYPE=postgresdb
ENV DB_POSTGRESDB_CONNECTION_URL=${DB_POSTGRESDB_CONNECTION_URL}
ENV DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED=false

# ---------------------------------------------------------
# Encryption Key
# ---------------------------------------------------------
ENV N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}

# ---------------------------------------------------------
# Host + Port
# ---------------------------------------------------------
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV WEBHOOK_URL=${WEBHOOK_URL}

# ---------------------------------------------------------
# Fix file permissions warning
# ---------------------------------------------------------
ENV N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true

# ---------------------------------------------------------
# Expose port for Render
# ---------------------------------------------------------
EXPOSE 5678

# ---------------------------------------------------------
# Start n8n
# ---------------------------------------------------------
CMD ["n8n"]

