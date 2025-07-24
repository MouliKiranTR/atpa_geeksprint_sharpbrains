"""
Basic tests for the main application
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Onboarding Agent API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "active"


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "onboarding-agent-api"


def test_health_detailed_endpoint():
    """Test the detailed health check endpoint"""
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "onboarding-agent-api"
    assert "dependencies" in data


def test_docs_endpoint():
    """Test that the API docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_endpoint():
    """Test that the OpenAPI spec is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Onboarding Agent API" 