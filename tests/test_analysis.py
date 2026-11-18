import pytest
from careermatch.analysis.extractor import extract_skills, skill_names
from careermatch.analysis.parser import parse_cv
from careermatch.analysis.profile import build_profile

@pytest.mark.parametrize("skill", [
"python","java","javascript","typescript","html","css","react","fastapi","django","flask",
"sql","postgresql","mysql","excel","power bi","tableau","pandas","machine learning",
"data analysis","git","github","docker","linux","aws","azure","communication","teamwork",
"problem solving","time management","leadership","customer service","project management",
"agile","scrum","marketing","sales","research","writing","design","figma","photoshop",
"accounting","bookkeeping","first aid","caregiving","teaching","training"])
def test_skill_vocabulary(skill):
    assert skill in skill_names("Experience with " + skill)

@pytest.mark.parametrize("text,expected", [
("I use JS","javascript"),("MS Excel","excel"),("PowerBI reports","power bi"),
("problem-solving","problem solving"),("people skills","communication"),
("team player","teamwork"),("Postgres database","postgresql")])
def test_aliases(text, expected):
    assert expected in skill_names(text)

def test_no_partial_word_match():
    assert "java" not in skill_names("JavaScript developer")

def test_empty_cv_has_no_skills():
    assert extract_skills("") == []

def test_skills_are_unique():
    assert skill_names("Python python PYTHON") == ["python"]

def test_confidence_is_valid():
    assert all(0 <= item.confidence <= 1 for item in extract_skills("Python SQL"))

def test_extraction_evidence_is_returned():
    assert extract_skills("Python")[0].evidence == "python"

def test_parser_named_sections():
    parsed = parse_cv("Summary\\nJunior developer\\nEducation\\nBSc Computing\\nExperience\\nVolunteer tutor")
    assert parsed.education == ["BSc Computing"]
    assert parsed.experience == ["Volunteer tutor"]

def test_parser_alternative_headings():
    parsed = parse_cv("Qualifications\\nDiploma\\nWork History\\nRetail assistant")
    assert parsed.education == ["Diploma"]
    assert parsed.experience == ["Retail assistant"]

def test_parser_experience_fallback():
    assert parse_cv("I worked as a volunteer").experience

def test_parser_empty_text():
    assert parse_cv("").sections == {}

def test_parser_interests():
    assert parse_cv("Interests\\nCoding\\nReading").interests == ["Coding", "Reading"]

def test_parser_bullet_prefix():
    assert parse_cv("Education\\n- College diploma").education == ["College diploma"]

def test_profile_groups_categories():
    profile = build_profile("Python SQL communication Figma")
    assert "python" in profile.skill_categories["programming"]
    assert "sql" in profile.skill_categories["data"]
    assert "communication" in profile.skill_categories["soft"]
    assert "figma" in profile.skill_categories["creative"]

def test_profile_filters_blank_interests():
    assert build_profile("Python", ["", " data "]).interests == ["data"]

def test_profile_serialises():
    assert build_profile("Python").to_dict()["skills"] == ["python"]

def test_profile_limits_summary():
    assert len(build_profile("x" * 900).summary) <= 500

def test_profile_without_known_skills_is_valid():
    assert build_profile("Motivated applicant").skills == []
