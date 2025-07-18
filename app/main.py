# FastAPI application entry point
#backend\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

# Import your routers
try:
    from app.routers import (
        auth_router, 
        user_router, 
        google_auth_router, 
        password_reset_router, 
        pet_dashboard_router, 
        pet_router,
        notification_router,
        message_router,
        admin_router,
        success_stories_router,
        security_router
    )
    routers_imported = True
except ImportError as e:
    print(f"Router import error: {e}")
    routers_imported = False

# Import database and models
try:
    from app.database.database import engine
    from app.models import models
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    db_connected = True
except Exception as e:
    print(f"Database connection error: {e}")
    db_connected = False

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "asdasdasdsad")

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://smart-pet-eta.vercel.app",
    "https://*.vercel.app",
    "*"  # For development - remove in production
]

# Initialize FastAPI app
app = FastAPI(
    title="Pet Adoption API",
    description="API for Pet Adoption Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Health check endpoints
@app.get("/")
def root():
    return {
        "status": "✅ FastAPI backend is running on Vercel",
        "environment": "production",
        "database_connected": db_connected,
        "routers_imported": routers_imported
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Pet API is running on Vercel!",
        "database": "connected" if db_connected else "error",
        "routers": "loaded" if routers_imported else "error"
    }

# Include routers if they were imported successfully
if routers_imported:
    try:
        app.include_router(auth_router.router, prefix="/api", tags=["auth"])
        app.include_router(user_router.router, prefix="/api", tags=["users"])
        app.include_router(google_auth_router.router, prefix="/api", tags=["google-auth"])
        app.include_router(password_reset_router.router, prefix="/api", tags=["password-reset"])
        app.include_router(pet_dashboard_router.router, prefix="/api", tags=["pet-dashboard"])
        app.include_router(notification_router.router, prefix="/api", tags=["notifications"])
        app.include_router(message_router.router, prefix="/api", tags=["messages"])
        app.include_router(admin_router.router, prefix="/api/admin", tags=["admin"])
        app.include_router(success_stories_router.router, prefix="/api", tags=["success-stories"])
        app.include_router(security_router.router, prefix="/api", tags=["security"])
        app.include_router(pet_router.router, prefix="/api", tags=["pets"])
        print("✅ All routers included successfully")
    except Exception as e:
        print(f"❌ Error including routers: {e}")

# Test endpoints for debugging
@app.get("/api/test")
def test_api():
    return {"message": "API is working!", "timestamp": "2024-01-01"}

@app.get("/debug")
def debug_info():
    return {
        "environment_vars": {
            "DATABASE_URL": "***" if os.getenv("DATABASE_URL") else "Not set",
            "SECRET_KEY": "***" if os.getenv("SECRET_KEY") else "Not set",
            "VERCEL": os.getenv("VERCEL", "Not set"),
        },
        "python_path": os.getcwd(),
        "database_connected": db_connected,
        "routers_imported": routers_imported
    }

# For Vercel serverless deployment
def handler(request):
    return app(request)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
