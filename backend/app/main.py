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
    template_routes  # ⭐ Template routes para gestión de documentos Word
)
from app.utils.exceptions import JustTimeException
from app.config import settings  # ✅ IMPORTAR SETTINGS PARA CORS
from app import PROJECT_INFO


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup: intentar crear tablas en base de datos
    print("🚀 Iniciando JustTime Backend...")
    await create_tables()
    
    # ✅ MOSTRAR CORS ORIGINS CONFIGURADOS
    cors_origins = settings.get_cors_origins()
    print(f"✅ CORS configurado para: {cors_origins}")
    
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

# ✅ CONFIGURACIÓN CORS DINÁMICA - LEE DE VARIABLE DE ENTORNO
cors_origins = settings.get_cors_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # ✅ AHORA ES DINÁMICO - Lee de CORS_ORIGINS en Railway
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight por 1 hora
)


# Endpoint de salud del sistema
@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raíz - verificación de estado del sistema"""
    return {
        "message": f"🛡️ {PROJECT_INFO['name']} API funcionando correctamente",
        "version": PROJECT_INFO["version"],
        "status": "active",
        "docs": "/docs",
        "cors_enabled": True,
        "allowed_origins": cors_origins  # ✅ MOSTRAR ORIGINS PERMITIDOS
    }


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "service": PROJECT_INFO["name"],
        "version": PROJECT_INFO["version"],
        "cors_origins": cors_origins  # ✅ Mostrar CORS configurado
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

# ⭐ Registro de rutas de plantillas
app.include_router(template_routes.router, prefix="/api/plantillas", tags=["Plantillas"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # ✅ Cambiar a 0.0.0.0 para Railway (acepta conexiones externas)
        port=8000,
        reload=True
    )