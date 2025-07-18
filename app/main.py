# FastAPI application entry point
#backend\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

# Import your routers
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
        "https://your-frontend-domain.vercel.app",
        "*"  # Remove this in production and specify your frontend domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(file_upload_router.router, prefix="/api/upload", tags=["upload"])
app.include_router(google_auth_router.router, prefix="/api/google", tags=["google"])

# Health check endpoints
@app.get("/")
async def root():
    return {"message": "Smart Pet API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working properly"}

# Test endpoints for debugging
@app.get("/debug")
async def debug_info():
    return {
        "environment": os.getenv("VERCEL_ENV", "development"),
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "secret_key_set": bool(os.getenv("SECRET_KEY"))
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
