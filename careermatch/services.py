from careermatch.analysis.profile import build_profile
from careermatch.data.jobs import JOBS
from careermatch.matching.recommender import recommend_jobs

MAX_CV_LENGTH = 20000

class CVTooLongError(ValueError):
    pass

def analyse_cv(cv_text: str, interests=None):
    if len(cv_text or "") > MAX_CV_LENGTH:
        raise CVTooLongError(f"CV text must be no longer than {MAX_CV_LENGTH} characters.")
    if not (cv_text or "").strip():
        raise ValueError("Please provide some CV text.")
    return build_profile(cv_text, interests).to_dict()

def get_recommendations(cv_text: str, interests=None, limit=10):
    profile = analyse_cv(cv_text, interests)
    matches = recommend_jobs(profile, JOBS, limit=limit)
    return {"profile": profile, "recommendations": [item.to_dict() for item in matches]}

def list_jobs():
    return [job.copy() for job in JOBS]

def get_job(job_id):
    return next((job.copy() for job in JOBS if job["id"] == job_id), None)
