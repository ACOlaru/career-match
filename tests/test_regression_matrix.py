import pytest
from careermatch.analysis.extractor import skill_names
from careermatch.analysis.profile import build_profile
from careermatch.matching.scorer import score_job
from careermatch.matching.recommender import recommend_jobs

@pytest.mark.parametrize("phrase", [
"python","java","javascript","typescript","html","css","react","fastapi",
"django","flask","sql","postgresql","mysql","excel","power bi","tableau",
"pandas","machine learning","data analysis","git","github","docker","linux",
"aws","azure","communication","teamwork","problem solving","time management",
"leadership","customer service","project management","agile","scrum","marketing",
"sales","research","writing","design","figma","photoshop","accounting",
"bookkeeping","first aid","caregiving","teaching","training"])
def test_skill_extracts_in_sentence(phrase):
    assert phrase in skill_names(f"Candidate has experience with {phrase}.")

@pytest.mark.parametrize("cv", [
"Python developer","SQL analyst","Teamwork and communication","Designer using Figma",
"Excel and data analysis","Volunteer with first aid","Teacher with training experience",
"Project work using Git and Docker"])
def test_profile_creation_for_varied_cv(cv):
    profile = build_profile(cv)
    assert isinstance(profile.skills, list)
    assert isinstance(profile.skill_categories, dict)

@pytest.mark.parametrize("candidate_skills", [
[],["python"],["git"],["python","git"],["python","git","sql"],
["excel","communication"],["design","figma"],["teamwork","leadership"]])
def test_score_is_bounded(candidate_skills):
    result = score_job({"skills":candidate_skills}, {
        "id":"matrix","title":"Test Role","required_skills":["python","git","sql"],
        "preferred_skills":["docker"],"tags":["technology"],"entry_level":True})
    assert 0 <= result.score <= 100
    assert set(result.matching_skills).issubset(candidate_skills)

@pytest.mark.parametrize("job_count", [0,1,2,5,10,25])
def test_recommender_handles_job_counts(job_count):
    jobs = [{"id":str(i),"title":f"Role {i}","required_skills":["python"]}
            for i in range(job_count)]
    assert len(recommend_jobs({"skills":["python"]}, jobs)) == job_count

@pytest.mark.parametrize("interests", [[],["software"],["data"],["creative"],
["business"],["people"],["other"]])
def test_profile_preserves_interests(interests):
    assert build_profile("Python and teamwork", interests).interests == interests

def test_missing_skills_are_visible():
    result = score_job({"skills":["python"]}, {
        "id":"gap","required_skills":["python","sql","git"]})
    assert result.missing_skills == ["git","sql"]

def test_recommendation_tie_breaking_is_stable():
    jobs = [{"id":"b","title":"Same"},{"id":"a","title":"Same"}]
    assert [item.job_id for item in recommend_jobs({}, jobs)] == ["a","b"]

def test_unknown_terms_are_not_fabricated_as_skills():
    assert skill_names("I know a fictional framework called Blorptastic") == []

def test_repeated_mentions_do_not_inflate_profile():
    assert build_profile("Python Python Python and SQL SQL").skills == ["python","sql"]
