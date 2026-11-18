from dataclasses import asdict, dataclass, field

@dataclass
class MatchResult:
    job_id: str
    job_title: str
    company: str
    score: float
    matching_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    improvement_tips: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

def clean_set(values):
    return {str(value).strip().lower() for value in (values or []) if str(value).strip()}

def score_job(profile: dict, job: dict) -> MatchResult:
    candidate = clean_set(profile.get("skills"))
    required = clean_set(job.get("required_skills"))
    preferred = clean_set(job.get("preferred_skills"))
    matching = sorted(candidate & required)
    missing = sorted(required - candidate)
    preferred_matches = sorted(candidate & preferred)
    skill_part = len(matching) / len(required) if required else 1.0
    interests, tags = clean_set(profile.get("interests")), clean_set(job.get("tags"))
    interest_part = len(interests & tags) / len(tags) if tags else 0.5
    experience_part = 1.0 if profile.get("experience") else 0.5
    entry_part = 1.0 if job.get("entry_level", False) else 0.5
    score = round(skill_part * 70 + interest_part * 15 + experience_part * 10 + entry_part * 5, 1)
    reasons = []
    if matching:
        reasons.append("Your profile includes " + ", ".join(matching) + ".")
    if preferred_matches:
        reasons.append("You also have preferred skills: " + ", ".join(preferred_matches) + ".")
    if interests & tags:
        reasons.append("The role aligns with your interests.")
    if job.get("entry_level"):
        reasons.append("The role is marked as suitable for entry-level applicants.")
    if not reasons:
        reasons.append("There is limited profile information to compare with this role.")
    tips = []
    if missing:
        tips.append("Consider developing: " + ", ".join(missing) + ".")
    if not profile.get("experience"):
        tips.append("Add projects, volunteering, placements or work experience.")
    if not interests:
        tips.append("Add career interests to improve recommendation relevance.")
    if not tips:
        tips.append("Keep your CV updated with recent projects and achievements.")
    return MatchResult(
        str(job.get("id", "")), str(job.get("title", "Untitled role")),
        str(job.get("company", "Unknown company")), min(100.0, max(0.0, score)),
        matching, missing, reasons, tips
    )
