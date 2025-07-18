from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your configuration
try:
    from core.config import settings
except ImportError:
    # Fallback configuration if import fails
    class FallbackSettings:
        DATABASE_URL = os.getenv("DATABASE_URL", "")
        SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
        ENVIRONMENT = os.getenv("VERCEL_ENV", "development")
    settings = FallbackSettings()

# Create FastAPI app
app = FastAPI(
    title="Smart Pet API",
    description="API for Smart Pet Adoption Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://your-frontend-domain.vercel.app"  # Replace with your actual frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Smart Pet API is running!",
        "status": "success",
        "environment": getattr(settings, 'ENVIRONMENT', 'unknown'),
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "API is running properly"
    }

# Debug endpoint
@app.get("/debug")
async def debug_info():
    return {
        "python_path": sys.path,
        "current_directory": os.getcwd(),
        "environment_variables": {
            "VERCEL_ENV": os.getenv("VERCEL_ENV"),
            "DATABASE_URL_SET": bool(os.getenv("DATABASE_URL")),
            "SECRET_KEY_SET": bool(os.getenv("SECRET_KEY"))
        }
    }

# Import and include routers (with error handling)
try:
    from app.routers import (
        auth_router,
        user_router,
        pet_router,
        admin_router,
        message_router,
        notification_router,
        password_reset_router,
        pet_dashboard_router,
        security_router,
        success_stories_router,
        file_upload_router,
        google_auth_router
    )
    
    # Include routers
    app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(user_router.router, prefix="/api/users", tags=["Users"])
    app.include_router(pet_router.router, prefix="/api/pets", tags=["Pets"])
    app.include_router(admin_router.router, prefix="/api/admin", tags=["Admin"])
    app.include_router(message_router.router, prefix="/api/messages", tags=["Messages"])
    app.include_router(notification_router.router, prefix="/api/notifications", tags=["Notifications"])
    app.include_router(password_reset_router.router, prefix="/api/password", tags=["Password Reset"])
    app.include_router(pet_dashboard_router.router, prefix="/api/dashboard", tags=["Dashboard"])
    app.include_router(security_router.router, prefix="/api/security", tags=["Security"])
    app.include_router(success_stories_router.router, prefix="/api/stories", tags=["Success Stories"])
    app.include_router(file_upload_router.router, prefix="/api/upload", tags=["File Upload"])
    app.include_router(google_auth_router.router, prefix="/api/google", tags=["Google Auth"])
    
    print("✅ All routers loaded successfully")
except ImportError as e:
    print(f"Warning: Could not import routers: {e}")

# Database initialization (with error handling)
try:
    from app.database.database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected successfully")
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

# This is the handler that Vercel will call
handler = app
