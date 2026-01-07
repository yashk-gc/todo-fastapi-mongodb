from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_todo():
    """Test POST /todos - create a new todo"""
    payload = {
        "title": "Test Todo 1",
        "description": "This is a test todo item",
        "is_completed": False,
        "is_deleted": False,
    }
    response = client.post("/todos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Todo 1"
    assert data["description"] == "This is a test todo item"
    assert data["is_completed"] is False
    assert data["is_deleted"] is False


def test_get_all_todos():
    """Test GET /todos - list all non-deleted todos"""
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should have at least the todo we just created (if run after test_create_todo)
    # but pytest runs independently so this might be empty initially


def test_get_single_todo():
    """Test GET /todos/{id} - get one todo (requires existing todo)"""
    # First create a todo
    payload = {
        "title": "Get Single Todo Test",
        "description": "Test single todo retrieval",
    }
    create_response = client.post("/todos", json=payload)
    assert create_response.status_code == 200
    todo_id = create_response.json()["id"]
    
    # Now get it
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Single Todo Test"


def test_update_todo():
    """Test PUT /todos/{id} - update existing todo"""
    # Create todo first
    payload = {
        "title": "Todo to Update",
        "description": "Original description",
    }
    create_response = client.post("/todos", json=payload)
    todo_id = create_response.json()["id"]
    
    # Update it
    update_payload = {
        "title": "Updated Todo Title",
        "description": "Updated description",
        "is_completed": True,
    }
    response = client.put(f"/todos/{todo_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo Title"
    assert data["is_completed"] is True


def test_delete_todo():
    """Test DELETE /todos/{id} - soft delete todo"""
    # Create todo
    payload = {"title": "Todo to Delete", "description": "Will be soft deleted"}
    create_response = client.post("/todos", json=payload)
    todo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task Deleted Successfully"
    
    # Verify it's gone from list (soft deleted)
    list_response = client.get("/todos")
    todos = list_response.json()
    todo_ids = [todo["id"] for todo in todos]
    assert todo_id not in todo_ids


def test_not_found():
    """Test 404 for invalid ObjectId format"""
    fake_id = "000000000000000000000000"
    response = client.get(f"/todos/{fake_id}")
    assert response.status_code == 404


def test_bulk_create():
    """Test POST /todos/bulk - create multiple todos"""
    payload = [
        {"title": "Bulk 1", "description": "First bulk todo"},
        {"title": "Bulk 2", "description": "Second bulk todo"},
    ]
    response = client.post("/todos/bulk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Bulk 1"
    assert data[1]["title"] == "Bulk 2"
