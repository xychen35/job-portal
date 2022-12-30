import json

def test_create_user(client):
    data = {"username":"testusername", "email":"test@gmail.com", "password":"testpwd"}
    response = client.post("/users/create-user", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["email"] == "test@gmail.com"
    assert response.json()["is_active"] == True