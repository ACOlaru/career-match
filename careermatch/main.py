from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from careermatch.api import router
from careermatch import __version__

app = FastAPI(title="CareerMatch", version=__version__)
app.include_router(router)

@app.get("/health")
def health():
    return {"status":"ok", "version":__version__}

@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE

PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>CareerMatch</title><style>
body{font:16px system-ui;margin:0;background:#f4f6fa;color:#18243a}
header{background:#172b4d;color:white;padding:2rem max(1rem,calc((100% - 850px)/2))}
main{max-width:850px;margin:2rem auto;padding:0 1rem}
section{background:white;padding:1.3rem;border-radius:12px;margin-bottom:1rem}
textarea,input{box-sizing:border-box;width:100%;padding:.8rem;border:1px solid #ccd3df;border-radius:7px;margin:.4rem 0 1rem}
textarea{min-height:180px}button{background:#2864dc;color:white;border:0;border-radius:7px;padding:.8rem 1rem;cursor:pointer}
.job{border-top:1px solid #ddd;padding:1rem 0}.score{color:#17623b;font-weight:bold}
</style></head><body><header><h1>CareerMatch</h1><p>Understand your skills. Discover your next step.</p></header>
<main><section><h2>Analyse your CV</h2><label for="cv">Paste CV text</label>
<textarea id="cv" placeholder="Python developer with SQL, Git and teamwork..."></textarea>
<label for="interests">Interests (comma separated)</label><input id="interests" placeholder="software, data">
<button id="run">Analyse and recommend jobs</button><p id="status" role="status"></p></section>
<section id="results" hidden><h2>Your profile</h2><p id="profile"></p><h2>Recommended jobs</h2><div id="jobs"></div></section></main>
<script>
document.querySelector("#run").onclick=async()=>{
 const status=document.querySelector("#status"), results=document.querySelector("#results");
 status.textContent="Analysing..."; results.hidden=true;
 try{
  const response=await fetch("/api/recommendations",{method:"POST",headers:{"Content-Type":"application/json"},
   body:JSON.stringify({cv_text:document.querySelector("#cv").value,
   interests:document.querySelector("#interests").value.split(",").map(x=>x.trim()).filter(Boolean)})});
  const data=await response.json(); if(!response.ok) throw Error(data.detail||"Request failed");
  document.querySelector("#profile").textContent="Skills: "+(data.profile.skills.join(", ")||"No known skills detected");
  const target=document.querySelector("#jobs"); target.replaceChildren();
  data.recommendations.forEach(item=>{
   const card=document.createElement("article"); card.className="job";
   const title=document.createElement("h3"); title.textContent=item.job_title+" — "+item.company;
   const score=document.createElement("p"); score.className="score"; score.textContent="Match: "+item.score+"%";
   const why=document.createElement("p"); why.textContent="Why: "+item.reasons.join(" ");
   const gaps=document.createElement("p"); gaps.textContent="Skills to develop: "+(item.missing_skills.join(", ")||"No required skill gaps found");
   const tips=document.createElement("p"); tips.textContent="Next steps: "+item.improvement_tips.join(" ");
   card.append(title,score,why,gaps,tips); target.append(card);
  });
  results.hidden=false; status.textContent="Analysis complete.";
 }catch(error){status.textContent=error.message;}
};
</script></body></html>'''
