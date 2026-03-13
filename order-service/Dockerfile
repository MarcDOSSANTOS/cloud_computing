# ============================================
# TechShop Order Service - Dockerfile
# TODO pour les étudiants :
# - Implémenter un multi-stage build
# - Compiler un binaire statique
# - Utiliser une image scratch ou distroless
# - Ajouter un utilisateur non-root
# ============================================

# Étape 1 : Build avec Go 1.25
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY . .

# Initialise le module et build
RUN go mod init github.com/techshop/order-service && \
    go get github.com/gin-gonic/gin@v1.9.1 github.com/lib/pq github.com/google/uuid && \
    go mod tidy && \
    echo "Building..." && \
    CGO_ENABLED=0 GOOS=linux go build -o /order-service ./cmd/server && \
    echo "Build successful!" && \
    ls -la /order-service

# Étape 2 : Runtime
FROM alpine:3.19
WORKDIR /app
RUN apk --no-cache add ca-certificates
COPY --from=builder /order-service .
RUN adduser -D appuser && chown appuser:appuser /app
USER appuser
EXPOSE 8003
CMD ["/order-service"]




