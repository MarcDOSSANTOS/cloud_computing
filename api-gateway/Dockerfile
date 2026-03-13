# ============================================
# TechShop API Gateway - Dockerfile
# TODO pour les étudiants :
# - Optimiser les layers Docker
# - Ajouter un utilisateur non-root
# - Configurer les health checks
# - Réduire la taille de l'image
# ============================================

FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/
EXPOSE 3000
CMD ["node", "src/server.js"]
