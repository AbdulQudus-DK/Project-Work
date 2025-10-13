# ---------------------------------------------------------
# Base image
# ---------------------------------------------------------
FROM n8nio/n8n:latest

# ---------------------------------------------------------
# Set timezone (optional)
# ---------------------------------------------------------
ENV GENERIC_TIMEZONE=Africa/Lagos

# ---------------------------------------------------------
# Basic Auth for security
# ---------------------------------------------------------
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=strong-password

# ---------------------------------------------------------
# Database connection (Neon)
# These should come from Render environment variables
# ---------------------------------------------------------
ENV DB_TYPE=postgresdb
ENV DB_POSTGRESDB_CONNECTION_URL=${DB_POSTGRESDB_CONNECTION_URL}

# ---------------------------------------------------------
# Encryption key (from env on Render)
# ---------------------------------------------------------
ENV N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}

# ---------------------------------------------------------
# Web server and network settings
# ---------------------------------------------------------
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=10000
ENV WEBHOOK_URL=${WEBHOOK_URL}

# ---------------------------------------------------------
# Fix permission warnings (recommended)
# ---------------------------------------------------------
ENV N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true

# ---------------------------------------------------------
# Expose the correct port for Render
# ---------------------------------------------------------
EXPOSE 10000

# ---------------------------------------------------------
# Start n8n
# ---------------------------------------------------------
CMD ["n8n", "start"]
