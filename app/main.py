"""
Onboarding Agent API - Main Application
Middleware API for frontend to communicate with various data sources and LLM
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
from dotenv import load_dotenv

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine, Base

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Onboarding Agent API",
    description="Middleware API for onboarding agent that reads data from "
                "various sources and provides LLM-powered summaries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure based on your deployment
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    print(f"🚀 Onboarding Agent API starting on "
          f"{settings.API_HOST}:{settings.API_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    print("🛑 Onboarding Agent API shutting down")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Onboarding Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "onboarding-agent-api"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4
    ) 