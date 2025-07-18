# FastAPI application entry point
#backend\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.models import models
from pathlib import Path

import os
from starlette.middleware.sessions import SessionMiddleware
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
from fastapi.staticfiles import StaticFiles  # Add this import

# Configuration
SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "asdasdasdsad")
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://smart-pet-eta.vercel.app",
    "https://smart-pet-eta.vercel.app",  # Both with and without colon for compatibility
]

# Create upload directories
UPLOAD_DIR = Path("app/uploads/pet_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Path("app/uploads/success_stories").mkdir(parents=True, exist_ok=True)
Path("app/uploads/messages").mkdir(parents=True, exist_ok=True)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Pet Adoption API",
    description="API for Pet Adoption Platform",
    version="1.0.0"
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers with API prefix
app.include_router(auth_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(google_auth_router.router, prefix="/api")
app.include_router(password_reset_router.router, prefix="/api")
app.include_router(pet_dashboard_router.router, prefix="/api")
app.include_router(notification_router.router, prefix="/api")
app.include_router(message_router.router, prefix="/api")
app.include_router(admin_router.router, prefix="/admin")
app.include_router(success_stories_router.router, prefix="/api")
app.include_router(security_router.router, prefix="/api")
app.include_router(pet_router.router, prefix="/api")

# Mount static files (for local development)
if not os.getenv("VERCEL"):
    app.mount("/uploads/pet_images", StaticFiles(directory="app/uploads/pet_images"), name="pet_images")
    app.mount("/uploads/messages", StaticFiles(directory="app/uploads/messages"), name="message_images")
    app.mount("/uploads/success_stories", StaticFiles(directory="app/uploads/success_stories"), name="stories_images")

@app.get("/")
def health_check():
    return {"status": "✅ FastAPI backend is running on Vercel", "environment": "production"}

@app.get("/api/health")
def api_health():
    return {"status": "healthy", "message": "Pet API is running on Vercel!"}

# For Vercel serverless functions
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False,
        workers=1
    )
