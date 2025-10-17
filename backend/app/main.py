# Archivo 02/43: app/main.py - ACTUALIZADO CON PLANTILLAS
# Descripción: Aplicación principal FastAPI con configuración completa
# Funcionalidad: Servidor ASGI, CORS, rutas y documentación automática
# ⭐ AGREGADO: Ruta de plantillas para gestión de documentos Word

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.database import engine, create_tables
from app.routers import (
    auth_routes, 
    task_routes, 
    project_routes, 
    contact_routes, 
    analytics_routes,
    template_routes  # ⭐ CAMBIAR DE plantilla_routes A template_routeslas
)
from app.utils.exceptions import JustTimeException
from app import PROJECT_INFO


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup: intentar crear tablas en base de datos
    print("🚀 Iniciando JustTime Backend...")
    await create_tables()
    print("✅ JustTime Backend iniciado")
    yield
    # Shutdown: cleanup si es necesario
    print("🛑 Cerrando JustTime Backend...")


# Configuración de la aplicación FastAPI
app = FastAPI(
    title=PROJECT_INFO["name"],
    description=PROJECT_INFO["description"],
    version=PROJECT_INFO["version"],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configuración CORS para frontend Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Endpoint de salud del sistema
@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raíz - verificación de estado del sistema"""
    return {
        "message": f"🛡️ {PROJECT_INFO['name']} API funcionando correctamente",
        "version": PROJECT_INFO["version"],
        "status": "active",
        "docs": "/docs"
    }


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "service": PROJECT_INFO["name"],
        "version": PROJECT_INFO["version"]
    }


# Manejador global de excepciones personalizadas
@app.exception_handler(JustTimeException)
async def justtime_exception_handler(request, exc: JustTimeException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_type": exc.error_type}
    )


# Manejador para errores HTTP generales
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# ============================================================================
# REGISTRO DE RUTAS DE LA APLICACIÓN
# ============================================================================

app.include_router(auth_routes.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(task_routes.router, prefix="/api/tasks", tags=["Tareas"])
app.include_router(project_routes.router, prefix="/api/projects", tags=["Proyectos"])
app.include_router(contact_routes.router, prefix="/api/contactos", tags=["Contactos"])
app.include_router(analytics_routes.router, prefix="/api/analytics", tags=["Analytics"])

# ⭐ NUEVO: Registro de rutas de plantillas
app.include_router(template_routes.router, prefix="/api/plantillas", tags=["Plantillas"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )