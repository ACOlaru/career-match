from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from careermatch.matching.scorer import score_job
from careermatch.services import analyse_cv, get_recommendations, list_jobs, get_job, CVTooLongError

router = APIRouter(prefix="/api", tags=["CareerMatch"])

class CVRequest(BaseModel):
    cv_text: str = Field(min_length=1, max_length=20000)
    interests: list[str] = Field(default_factory=list)

class RecommendationRequest(CVRequest):
    limit: int = Field(default=10, ge=1, le=50)

class MatchRequest(BaseModel):
    profile: dict
    job: dict

@router.get("/jobs")
def jobs():
    return {"jobs": list_jobs()}

@router.get("/jobs/{job_id}")
def job_detail(job_id: str):
    item = get_job(job_id)
    if item is None:
        raise HTTPException(404, "Job not found.")
    return item

@router.post("/cv/analyse")
def cv_analyse(request: CVRequest):
    try:
        return analyse_cv(request.cv_text, request.interests)
    except CVTooLongError as exc:
        raise HTTPException(413, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.post("/recommendations")
def recommendations(request: RecommendationRequest):
    try:
        return get_recommendations(request.cv_text, request.interests, request.limit)
    except CVTooLongError as exc:
        raise HTTPException(413, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.post("/match")
def match(request: MatchRequest):
    return score_job(request.profile, request.job).to_dict()
