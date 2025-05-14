from fastapi import FastAPI, UploadFile, File, Form
from src.resume_analyzer.utils.parsing_utils import parse_resume
from src.resume_analyzer.resume_analyzer import match_resume_to_jd

app = FastAPI()

@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form("")
):
    content = await file.read()
    extracted_info = parse_resume(file.filename, content)
    match_score = match_resume_to_jd(extracted_info, job_description)
    return {
        "extracted_info": extracted_info,
        "match_score": match_score
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)