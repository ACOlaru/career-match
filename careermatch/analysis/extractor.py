from dataclasses import asdict, dataclass
from careermatch.analysis.catalog import SKILLS, ALIASES
from careermatch.analysis.text import has_phrase

@dataclass(frozen=True)
class Skill:
    name: str
    category: str
    confidence: float
    evidence: str

    def to_dict(self):
        return asdict(self)

def extract_skills(text: str) -> list[Skill]:
    found = {}
    for name, category in SKILLS.items():
        if has_phrase(text, name):
            found[name] = Skill(name, category, 0.95, name)
    for alias, canonical in ALIASES.items():
        if has_phrase(text, alias) and canonical not in found:
            found[canonical] = Skill(canonical, SKILLS[canonical], 0.85, alias)
    return sorted(found.values(), key=lambda item: (item.category, item.name))

def skill_names(text: str) -> list[str]:
    return [skill.name for skill in extract_skills(text)]

def skills_by_category(text: str) -> dict[str, list[str]]:
    result = {}
    for skill in extract_skills(text):
        result.setdefault(skill.category, []).append(skill.name)
    return result

def explain_extraction(text: str) -> list[dict]:
    return [skill.to_dict() for skill in extract_skills(text)]
