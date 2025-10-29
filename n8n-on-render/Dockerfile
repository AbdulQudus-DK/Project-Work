# ---------------------------------------------------------
# Base image (includes the n8n binary)
# ---------------------------------------------------------
FROM n8nio/n8n:latest

# ---------------------------------------------------------
# Set timezone
# ---------------------------------------------------------
ENV GENERIC_TIMEZONE=Africa/Lagos

# ---------------------------------------------------------
# Database config (from Render env vars)
# ---------------------------------------------------------
ENV DB_TYPE=postgresdb
ENV DB_POSTGRESDB_CONNECTION_URL=ENV DB_POSTGRESDB_CONNECTION_URL=postgresql://neondb_owner:npg_nvj5bU9TZNim@ep-bold-pond-a9fg15e0-pooler.gwc.azure.neon.tech/neondb?sslmode=require

ENV DB_POSTGRESDB_HOST=ep-bold-pond-a9fg15e0-pooler.gwc.azure.neon.tech
ENV DB_POSTGRESDB_PORT=5432
ENV DB_POSTGRESDB_DATABASE=neondb
ENV DB_POSTGRESDB_USER=neondb_owner
ENV DB_POSTGRESDB_PASSWORD=npg_nvj5bU9TZNim

ENV DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED=false

# ---------------------------------------------------------
# Encryption + Security
# ---------------------------------------------------------
ENV N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=strong-password

# ---------------------------------------------------------
# Network
# ---------------------------------------------------------
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV WEBHOOK_URL=https://n8n-project-hnzs.onrender.com

# ---------------------------------------------------------
# Fix file permissions
# ---------------------------------------------------------
ENV N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true

# ---------------------------------------------------------
# Expose port
# ---------------------------------------------------------
EXPOSE 5678

# ---------------------------------------------------------
# Start n8n
# ---------------------------------------------------------
ENTRYPOINT ["tini", "--"]
CMD ["n8n"]


