"""
TechShop User Service
Gestion des utilisateurs et authentification
Technologie : Python / FastAPI
Port : 8001
"""

import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram

from app.routes.users import router as users_router
from app.models.database import engine, Base


# ============================================
# Métriques Prometheus
# ============================================
REQUEST_COUNT = Counter(
    'user_service_requests_total',
    'Total des requêtes',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'user_service_request_duration_seconds',
    'Latence des requêtes en secondes',
    ['method', 'endpoint']
)


# ============================================
# Lifecycle
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup : créer les tables
    print("🚀 User Service - Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ User Service - Base de données initialisée")
    yield
    # Shutdown
    print("👋 User Service - Arrêt en cours...")


# ============================================
# Application FastAPI
# ============================================
app = FastAPI(
    title="TechShop User Service",
    description="Service de gestion des utilisateurs et authentification",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Métriques Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# ============================================
# Middleware de métriques
# ============================================
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response


# ============================================
# Routes
# ============================================
app.include_router(users_router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def root():
    return {
        "service": "TechShop User Service",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint pour Kubernetes et monitoring"""
    return {
        "status": "up",
        "service": "user-service",
        "version": "1.0.0",
    }
