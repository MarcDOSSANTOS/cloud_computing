# ============================================
# TechShop Product Service - Dockerfile
# TODO pour les étudiants :
# - Implémenter un multi-stage build (Maven + JRE)
# - Utiliser un JRE minimal (Eclipse Temurin)
# - Optimiser les layers avec le layer-tools de Spring Boot
# - Ajouter un utilisateur non-root
# ============================================

# Étape 1 : Build avec Maven
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src/ ./src/
RUN mvn package -DskipTests

# Étape 2 : Runtime avec JRE léger
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
RUN adduser -D appuser && chown appuser:appuser app.jar
USER appuser
EXPOSE 8002
CMD ["java", "-jar", "app.jar"]
