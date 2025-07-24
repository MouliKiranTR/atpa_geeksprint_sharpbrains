#!/usr/bin/env python3
"""
Simple startup script for the Onboarding Agent API
"""

import os
import uvicorn
from app.core.config import settings

# Prevent Python from creating __pycache__ directories
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

if __name__ == "__main__":
    print("🚀 Starting Onboarding Agent API...")
    print(f"📡 Server will be available at: "
          f"http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 API Documentation: "
          f"http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print(f"🏥 Health Check: "
          f"http://{settings.API_HOST}:{settings.API_PORT}/health")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        log_level="info"
    ) 