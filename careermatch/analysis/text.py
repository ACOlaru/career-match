import re
import unicodedata

def normalise(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.lower().replace("’", "'")
    value = re.sub(r"[^a-z0-9+#.\\s/-]", " ", value)
    return re.sub(r"\\s+", " ", value).strip()

def has_phrase(text: str, phrase: str) -> bool:
    text, phrase = normalise(text), normalise(phrase)
    if not phrase:
        return False
    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None

def split_lines(text: str) -> list[str]:
    return [line.strip() for line in (text or "").splitlines() if line.strip()]

def clean_bullet(line: str) -> str:
    return re.sub(r"^[\\-*•\\d.)\\s]+", "", line).strip()

def truncate(value: str, limit: int) -> str:
    return (value or "")[:limit]
