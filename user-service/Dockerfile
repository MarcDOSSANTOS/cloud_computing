# ============================================
# TechShop User Service - Dockerfile
# TODO pour les étudiants :
# - Implémenter un multi-stage build
# - Optimiser la taille de l'image
# - Ajouter un utilisateur non-root
# - Gérer les dépendances de manière optimale
# ============================================

# Étape 1 : Build
FROM python:3.12-slim
WORKDIR /app

# Installe les dépendances système pour bcrypt
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances Python (avec bcrypt)
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY app/ ./app/

# Crée un utilisateur non-root (optionnel)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]


