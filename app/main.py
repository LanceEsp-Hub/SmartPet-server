from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "asdasdasdsad")

# Initialize FastAPI app
app = FastAPI(
    title="Smart Pet API",
    description="API for Smart Pet Adoption Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and setup database
try:
    from app.database.database import engine, Base
    from app.core.config import settings
    Base.metadata.create_all(bind=engine)
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
except Exception as e:
    print(f"❌ Router loading error: {e}")

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "Smart Pet API is running!",
        "status": "success",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected" if engine else "disconnected"
    }

# Debug endpoint
@app.get("/debug")
async def debug_info():
    return {
        "python_path": sys.path,
        "current_dir": str(Path.cwd()),
        "file_location": str(Path(__file__)),
        "environment_vars": {
            "DATABASE_URL": "***" if os.getenv("DATABASE_URL") else "Not set",
            "SECRET_KEY": "***" if os.getenv("SECRET_KEY") else "Not set"
        }
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

# This is the handler that Vercel will call
handler = app
