import re
from dataclasses import dataclass, field
from careermatch.analysis.text import split_lines, normalise, clean_bullet

HEADINGS = {
    "summary": ("summary", "profile", "about me"),
    "education": ("education", "qualifications", "academic background"),
    "experience": ("experience", "employment", "work history", "professional experience"),
    "skills": ("skills", "technical skills", "core skills"),
    "interests": ("interests", "hobbies", "activities")
}

@dataclass
class ParsedCV:
    raw_text: str
    sections: dict[str, str] = field(default_factory=dict)
    education: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    interests: list[str] = field(default_factory=list)

def heading_for(line):
    candidate = normalise(line).strip(" :")
    for section, labels in HEADINGS.items():
        if candidate in labels:
            return section
    return None

def extract_items(section):
    return [clean_bullet(line) for line in split_lines(section) if clean_bullet(line)]

def infer_experience(text):
    markers = r"\\b(intern|volunteer|assistant|developer|manager|worked|built|created)\\b"
    return [line for line in split_lines(text) if re.search(markers, line, re.I)][:10]

def parse_cv(text: str) -> ParsedCV:
    buckets = {"summary": []}
    current = "summary"
    for line in split_lines(text):
        heading = heading_for(line)
        if heading:
            current = heading
            buckets.setdefault(current, [])
        else:
            buckets.setdefault(current, []).append(line)
    sections = {key: "\\n".join(value) for key, value in buckets.items()}
    experience = extract_items(sections.get("experience", ""))
    if not experience:
        experience = infer_experience(text or "")
    return ParsedCV(
        raw_text=text or "", sections=sections,
        education=extract_items(sections.get("education", "")),
        experience=experience,
        interests=extract_items(sections.get("interests", ""))
    )
