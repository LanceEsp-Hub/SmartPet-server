import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if using one)
load_dotenv()

# Secret key for signing tokens
SECRET_KEY = os.getenv("SECRET_KEY", "asdasdasdsad")

# Email settings
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "pogisicj31@gmail.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "huqiwrsknzfyxqkh")
MAIL_FROM = os.getenv("MAIL_FROM", "nas@gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")

# Google OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "653397573990-30qo6aca71lgldvilfhktc08n3280qhn.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "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")

# Supabase settings
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://fkpimtcxncgwtdsfyrjb.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZrcGltdGN4bmNnd3Rkc2Z5cmpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2OTQyODEsImV4cCI6MjA2ODI3MDI4MX0.vZWZNOGRekiuudIQM1RM9dNAJy8dRcjXU6pglwcyPm4")

# Database URL for Supabase
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.fkpimtcxncgwtdsfyrjb:lance@aws-0-us-east-2.pooler.supabase.com:6543/postgres")

# CORS origins for production
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.vercel.app",  # Replace with your actual Vercel frontend URL
    "https://*.vercel.app"
]
