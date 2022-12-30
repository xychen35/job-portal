import json


def test_create_job(client):
    data = {
        "title":"SDE", 
        "company":"GOOGLE", 
        "company_url":"GOOGLE",
        "location":"LAS",
        "description":"GOOD",
        "date_posted":"2022-12-28"
        }
    response = client.post("/jobs/create-job", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["company"] == "GOOGLE"
    
def test_retreive_job_by_id(client):
    data = {
        "title":"SDE", 
        "company":"GOOGLE", 
        "company_url":"GOOGLE",
        "location":"LAS",
        "description":"GOOD",
        "date_posted":"2022-12-28"
        }
    client.post("/jobs/create-job", json.dumps(data))
    response = client.get("/jobs/get/1")
    assert response.status_code == 200
    assert response.json()["title"] == "SDE"