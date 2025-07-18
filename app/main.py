from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "asdasdasdsad")

# Initialize FastAPI app
app = FastAPI(
    title="Smart Pet API",
    description="API for Smart Pet Adoption Platform",
    version="1.0.0"
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://smart-pet-eta.vercel.app",
        "https://*.vercel.app",
        "*"  # Remove this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and setup database
try:
    from app.database.database import engine
    from app.models import models
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database connected successfully")
except Exception as e:
    print(f"❌ Database connection error: {e}")

# Import routers
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
        google_auth_router
    )
    
    # Include routers
    app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
    app.include_router(user_router.router, prefix="/api/users", tags=["users"])
    app.include_router(pet_router.router, prefix="/api/pets", tags=["pets"])
    app.include_router(admin_router.router, prefix="/api/admin", tags=["admin"])
    app.include_router(message_router.router, prefix="/api/messages", tags=["messages"])
    app.include_router(notification_router.router, prefix="/api/notifications", tags=["notifications"])
    app.include_router(password_reset_router.router, prefix="/api/password", tags=["password"])
    app.include_router(pet_dashboard_router.router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(security_router.router, prefix="/api/security", tags=["security"])
    app.include_router(success_stories_router.router, prefix="/api/stories", tags=["stories"])
    app.include_router(google_auth_router.router, prefix="/api/google", tags=["google"])
    
    print("✅ All routers loaded successfully")
except Exception as e:
    print(f"❌ Router loading error: {e}")

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "🐾 Smart Pet API is running!",
        "status": "success",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "API is working properly",
        "environment": os.getenv("VERCEL_ENV", "development")
    }

@app.get("/api/test")
async def test_endpoint():
    return {"message": "API test successful", "timestamp": "2024-01-01"}

# Debug endpoint
@app.get("/debug")
async def debug_info():
    return {
        "environment": os.getenv("VERCEL_ENV", "development"),
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "secret_key_set": bool(os.getenv("SECRET_KEY")),
        "python_version": "3.9+",
        "fastapi_version": "0.104.1"
    }

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
