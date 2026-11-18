import pytest
from careermatch.matching.scorer import score_job
from careermatch.matching.recommender import recommend_jobs

PROFILE = {"skills":["python","git","communication"],"interests":["software"],
           "experience":["Personal coding project"]}
JOB = {"id":"x1","title":"Junior Developer","company":"Example",
       "required_skills":["python","git","sql"],"preferred_skills":["docker"],
       "tags":["software"],"entry_level":True}

def test_matching_skills_and_gaps():
    result = score_job(PROFILE, JOB)
    assert result.matching_skills == ["git","python"]
    assert result.missing_skills == ["sql"]

def test_score_bounds():
    assert 0 <= score_job(PROFILE, JOB).score <= 100

def test_reasons_and_tips_exist():
    result = score_job(PROFILE, JOB)
    assert result.reasons and result.improvement_tips

def test_better_profile_scores_higher():
    assert score_job(PROFILE, JOB).score > score_job({"skills":[]}, JOB).score

def test_no_required_skills_is_safe():
    assert score_job(PROFILE, dict(JOB, required_skills=[])).score >= 0

def test_empty_profile_is_safe():
    assert score_job({}, JOB).missing_skills

def test_preferred_skills_explained():
    profile = dict(PROFILE, skills=PROFILE["skills"]+["docker"])
    assert any("docker" in item for item in score_job(profile, JOB).reasons)

def test_sparse_job_is_safe():
    assert score_job({"skills":["python"]}, {"id":"a"}).job_title == "Untitled role"

def test_case_and_whitespace_normalised():
    result = score_job({"skills":[" Python ","GIT"]}, JOB)
    assert result.matching_skills == ["git","python"]

def test_result_serialises():
    assert score_job(PROFILE, JOB).to_dict()["job_id"] == "x1"

def test_recommendations_rank_best_first():
    jobs = [dict(JOB, id="b", required_skills=["excel"]),
            dict(JOB, id="a", required_skills=["python","git"])]
    assert recommend_jobs(PROFILE, jobs)[0].job_id == "a"

@pytest.mark.parametrize("limit", [1,2,3,5,10,20])
def test_recommendation_limit(limit):
    jobs = [{"id":str(i),"title":f"Role {i}"} for i in range(15)]
    assert len(recommend_jobs({}, jobs, limit=limit)) == min(limit, 15)

def test_zero_limit_returns_empty():
    assert recommend_jobs({}, [JOB], limit=0) == []

def test_minimum_score_filters():
    assert recommend_jobs({}, [JOB], minimum_score=100) == []

def test_empty_jobs_returns_empty():
    assert recommend_jobs({}, []) == []

def test_ties_are_deterministic():
    jobs = [{"id":"z","title":"Zulu"},{"id":"a","title":"Alpha"}]
    assert [item.job_title for item in recommend_jobs({}, jobs)] == ["Alpha","Zulu"]

@pytest.mark.parametrize("skills", [[],["python"],["sql"],["python","sql"],
                                    ["communication","teamwork"],["design","figma"]])
def test_scorer_is_deterministic(skills):
    profile = {"skills":skills,"interests":["software"],"experience":[]}
    assert score_job(profile, JOB).to_dict() == score_job(profile, JOB).to_dict()

@pytest.mark.parametrize("entry", [True, False])
def test_entry_level_flag_supported(entry):
    assert 0 <= score_job(PROFILE, dict(JOB, entry_level=entry)).score <= 100
