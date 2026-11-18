# Architecture

- `analysis`: parses CV text, extracts known skills and builds candidate profiles.
- `matching`: calculates transparent weighted scores and explanations.
- `services`: coordinates application use cases and sample job data.
- `api`: exposes endpoints through FastAPI.
- `main`: serves the API and simple browser interface.

Scoring weights: 70% required-skill coverage, 15% interest/tag alignment,
10% experience evidence and 5% entry-level suitability. Missing skills are shown
as development suggestions, not hidden rejection rules.

CV text is processed in memory and not persisted. Add consent, authentication,
secure storage and retention controls before using real candidate data.
