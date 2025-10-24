# Archivo 02/43: app/main.py - ACTUALIZADO CON CORS DINÁMICO
# Descripción: Aplicación principal FastAPI con configuración CORS desde variables de entorno
# Funcionalidad: Servidor ASGI, CORS dinámico, rutas y documentación automática

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
    template_routes,
    document_routes,
    pending_activity_routes,
    configuracion_routes,
    employee_routes
)
from app.utils.exceptions import JustTimeException
from app import PROJECT_INFO
from app.config import settings, CORS_CONFIG  # ⭐ IMPORTAR CORS_CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup: intentar crear tablas en base de datos
    print("🚀 Iniciando JustTime Backend...")
    print(f"📡 CORS Origins configurados: {CORS_CONFIG['origins']}")  # ⭐ LOG para debug
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

# ⭐ CONFIGURACIÓN CORS DINÁMICA - Lee desde variables de entorno
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["origins"],      # ✅ Usa la lista desde config.py
    allow_credentials=CORS_CONFIG["credentials"],
    allow_methods=CORS_CONFIG["methods"],
    allow_headers=CORS_CONFIG["headers"],
)


# Endpoint de salud del sistema
@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raíz - verificación de estado del sistema"""
    return {
        "message": f"⚖️ {PROJECT_INFO['name']} API funcionando correctamente",
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
app.include_router(template_routes.router, prefix="/api/plantillas", tags=["Plantillas"])
app.include_router(document_routes.router, prefix="/api/documentos", tags=["Documentos"])
app.include_router(pending_activity_routes.router, prefix="/api/pending-activities", tags=["Actividades Pendientes"])
app.include_router(configuracion_routes.router, prefix="/api/configuraciones", tags=["Configuraciones"])
app.include_router(employee_routes.router, prefix="/api/empleados", tags=["Empleados"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )