from src.resume_analyzer.utils.pdf_utils import read_pdf, read_docx
from datetime import datetime
import re

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{7,}\d", text)
    return match.group(0) if match else ""


def extract_years_experience(text):
    current_date = datetime.now()
    total_months = 0

    # Match patterns like "2020 – 2022" or "2019 - present"
    matches = re.findall(r"(19\d{2}|20\d{2})\s*[-–]\s*(present|19\d{2}|20\d{2})", text, re.IGNORECASE)

    for start, end in matches:
        try:
            start_year = int(start)
            end_year = current_date.year if end.lower() == 'present' else int(end)
            start_month = 6  # Assume mid-year
            end_month = current_date.month if end.lower() == 'present' else 6

            start_date = datetime(start_year, start_month, 1)
            end_date = datetime(end_year, end_month, 1)

            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            if months > 0:
                total_months += months
        except:
            continue

    return round(total_months / 12.0, 1) if total_months else 0



def parse_resume(filename: str, content: bytes):
    text = read_pdf(content) if filename.endswith(".pdf") else read_docx(content)
    email = extract_email(text)
    phone = extract_phone(text)
    experience_years = extract_years_experience(text)
    skills = re.findall(r"(?i)(python|java|sql|aws|docker|kubernetes|ml|ai|flask|fastapi)", text)
    return {
        "email": email,
        "phone": phone,
        "skills": list(set([s.lower() for s in skills])),
        "years_experience": experience_years,
        "raw_text": text[:1000]  # Preview
    }