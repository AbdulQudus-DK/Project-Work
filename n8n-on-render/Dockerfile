# Base image
FROM n8nio/n8n

# Set timezone (optional)
ENV GENERIC_TIMEZONE=Europe/Madrid

# Enable Basic Auth (recommended for security)
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=strong-password

# Correct base URL for Render
# Replace YOUR_SERVICE_NAME and YOUR_RENDER_DOMAIN with your actual Render URL
ENV N8N_EDITOR_BASE_URL=https://n8n-deploy-ze3y.onrender.com
ENV WEBHOOK_URL=https://n8n-deploy-ze3y.onrender.com

# Expose the default n8n port
EXPOSE 5678

