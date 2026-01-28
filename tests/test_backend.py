from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "SecureBot API" in response.json()["message"]

def test_tutor_history():
    """Test fetching chat history"""
    response = client.get("/api/tutor/history")
    assert response.status_code == 200
    assert "chats" in response.json()

def test_create_new_chat():
    """Test creating a new chat session"""
    response = client.post("/api/tutor/new")
    assert response.status_code == 200
    data = response.json()
    assert "chat_id" in data
    assert data["message"] == "New chat created"

# Note: We skip testing LLM/RAG dependent endpoints to avoid API costs and external dependencies
# in this basic test suite. Ideally, we would mock the LLM calls for comprehensive testing.
