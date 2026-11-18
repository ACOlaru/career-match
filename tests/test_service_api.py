import pytest
from fastapi.testclient import TestClient
from careermatch.main import app
from careermatch.services import analyse_cv, get_recommendations, list_jobs, get_job, CVTooLongError

client = TestClient(app)

def test_analyse_cv_returns_profile():
    assert "python" in analyse_cv("Python developer")["skills"]

def test_analyse_cv_rejects_blank():
    with pytest.raises(ValueError):
        analyse_cv("  ")

def test_analyse_cv_rejects_oversize():
    with pytest.raises(CVTooLongError):
        analyse_cv("x" * 20001)

def test_recommendations_include_profile():
    result = get_recommendations("Python, Git and problem solving", ["software"])
    assert result["profile"] and result["recommendations"]

def test_recommendation_limit():
    assert len(get_recommendations("Python", limit=1)["recommendations"]) == 1

def test_jobs_are_copied():
    jobs = list_jobs()
    jobs[0]["title"] = "Mutated"
    assert list_jobs()[0]["title"] != "Mutated"

def test_job_lookup():
    assert get_job("job-001")["title"] == "Junior Python Developer"

def test_missing_job_lookup():
    assert get_job("missing") is None

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "CareerMatch" in response.text

def test_jobs_api():
    response = client.get("/api/jobs")
    assert response.status_code == 200
    assert response.json()["jobs"]

def test_job_detail_api():
    assert client.get("/api/jobs/job-001").status_code == 200

def test_missing_job_api():
    assert client.get("/api/jobs/invalid").status_code == 404

def test_cv_analysis_api():
    response = client.post("/api/cv/analyse", json={"cv_text":"Python and Git"})
    assert response.status_code == 200
    assert "python" in response.json()["skills"]

def test_recommendations_api():
    response = client.post("/api/recommendations", json={"cv_text":"Python and Git"})
    assert response.status_code == 200
    assert response.json()["recommendations"]

def test_blank_cv_api():
    assert client.post("/api/cv/analyse", json={"cv_text":""}).status_code == 422

def test_match_api():
    response = client.post("/api/match", json={
        "profile":{"skills":["python"]},
        "job":{"id":"t","required_skills":["python"]}})
    assert response.status_code == 200
    assert response.json()["matching_skills"] == ["python"]

def test_invalid_limit_api():
    assert client.post("/api/recommendations",
        json={"cv_text":"Python","limit":0}).status_code == 422

@pytest.mark.parametrize("interests", [[],["software"],["data","research"],[" "],["creative"]])
def test_api_accepts_interest_variations(interests):
    response = client.post("/api/recommendations",
        json={"cv_text":"Python developer","interests":interests})
    assert response.status_code == 200
