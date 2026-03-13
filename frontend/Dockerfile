# ============================================
# TechShop Frontend - Dockerfile
# TODO pour les étudiants :
# - Implémenter un multi-stage build
# - Optimiser la taille de l'image
# - Ajouter un utilisateur non-root
# - Configurer les labels OCI
# ============================================

# Étape 1 : Build de l'application React
FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Étape 2 : Serveur Nginx pour servir l'application
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
