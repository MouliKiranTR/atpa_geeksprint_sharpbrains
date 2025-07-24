"""
Configuration settings for the Onboarding Agent API
"""

from typing import Optional
# from pydantic import field_validator  # Commented out - validators disabled
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    TEST_DATABASE_URL: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Data Sources Configuration
    CONFLUENCE_API_URL: Optional[str] = None
    CONFLUENCE_USERNAME: Optional[str] = None
    CONFLUENCE_API_TOKEN: Optional[str] = None
    
    SHAREPOINT_SITE_URL: Optional[str] = None
    SHAREPOINT_CLIENT_ID: Optional[str] = None
    SHAREPOINT_CLIENT_SECRET: Optional[str] = None
    
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_SIGNING_SECRET: Optional[str] = None
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = "pdf,docx,txt,xlsx,csv"
    
    # Lucid API Configuration
    LUCID_API_KEY: Optional[str] = None
    LUCID_API_BASE_URL: str = "https://api.lucid.co"
    
    # Figma API Configuration
    FIGMA_API_TOKEN: Optional[str] = None
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_DIR: str = "./cache"
    CACHE_EXPIRY_HOURS: int = 24
    AUTO_UPLOAD_TO_OPENARENA: bool = True
    
    # Validators disabled for compatibility
    # @field_validator('ALLOWED_FILE_TYPES')
    # @classmethod
    # def parse_allowed_file_types(cls, v):
    #     """Parse comma-separated file types into a list"""
    #     return [ext.strip().lower() for ext in v.split(',')]
    
    # @field_validator('OPENAI_API_KEY')
    # @classmethod
    # def validate_openai_key(cls, v):
    #     """Validate OpenAI API key format if provided"""
    #     if v and not v.startswith('sk-'):
    #         raise ValueError('OPENAI_API_KEY should start with "sk-"')
    #     return v
    
    # @field_validator('SECRET_KEY')
    # @classmethod
    # def validate_secret_key(cls, v):
    #     """Validate secret key length if provided"""
    #     if v and len(v) < 32:
    #         raise ValueError(
    #             'SECRET_KEY should be at least 32 characters long'
    #         )
    #     return v
    
    model_config = {
        "env_file": ".env", 
        "case_sensitive": True,
        "extra": "ignore",
        "validate_assignment": False,  # Disable validation on assignment
        "validate_default": False,     # Disable validation of default values
        "arbitrary_types_allowed": True  # Allow any types
    }


# Create settings instance
settings = Settings() 