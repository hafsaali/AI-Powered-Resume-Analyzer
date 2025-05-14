import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resume_to_jd(resume_data, job_description: str):
    resume_text = resume_data.get("raw_text", "")
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_jd = model.encode(job_description, convert_to_tensor=True)
    similarity = util.cos_sim(emb_resume, emb_jd).item()

    # Scoring boost by experience and skill match
    experience = resume_data.get("years_experience", 0)
    skills = set(resume_data.get("skills", []))
    jd_keywords = set(re.findall(r"(?i)python|java|sql|aws|docker|ml|ai|flask|fastapi", job_description))
    skill_match = len(skills.intersection(jd_keywords)) / (len(jd_keywords) + 1e-5)

    final_score = (similarity * 0.6 + min(experience / 10, 1.0) * 0.2 + skill_match * 0.2) * 100
    return round(final_score, 2)