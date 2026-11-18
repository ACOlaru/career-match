from dataclasses import asdict, dataclass, field
from careermatch.analysis.extractor import extract_skills, skills_by_category
from careermatch.analysis.parser import parse_cv
from careermatch.analysis.text import truncate

@dataclass
class CandidateProfile:
    skills: list[str] = field(default_factory=list)
    skill_categories: dict[str, list[str]] = field(default_factory=dict)
    education: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    interests: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self):
        return asdict(self)

def build_profile(cv_text: str, interests=None) -> CandidateProfile:
    parsed = parse_cv(cv_text)
    return CandidateProfile(
        skills=[item.name for item in extract_skills(cv_text)],
        skill_categories=skills_by_category(cv_text),
        education=parsed.education,
        experience=parsed.experience,
        interests=[item.strip() for item in (interests or []) if item.strip()],
        summary=truncate(parsed.sections.get("summary", ""), 500)
    )
