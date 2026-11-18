from careermatch.matching.scorer import score_job

def recommend_jobs(profile: dict, jobs: list[dict], limit=10, minimum_score=0):
    if limit < 1:
        return []
    results = [score_job(profile, job) for job in jobs]
    results = [item for item in results if item.score >= minimum_score]
    results.sort(key=lambda item: (-item.score, item.job_title.lower(), item.job_id))
    return results[:limit]
