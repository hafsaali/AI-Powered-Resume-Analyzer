from src.resume_analyzer.utils.pdf_utils import read_pdf, convert_to_pdf
from data.skills_db import DOMAIN_SKILLS, TOOLS, SOFT_SKILLS
import tempfile
import os
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


def extract_skills(text, domains=None):
    text = text.lower()
    skills_found = set()

    # Search domain-specific skills
    search_domains = domains if domains else DOMAIN_SKILLS.keys()
    for domain in search_domains:
        for skill in DOMAIN_SKILLS[domain]:
            if re.search(rf"\b{re.escape(skill)}\b", text):
                skills_found.add((skill, domain))  # Store skill with domain

    # Search soft skills
    for skill in SOFT_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            skills_found.add((skill, "soft_skill"))

    # Search tools
    for category, tools in TOOLS.items():
        for tool in tools:
            if re.search(rf"\b{re.escape(tool)}\b", text):
                skills_found.add((tool, f"tool_{category}"))

    return list(skills_found)


def parse_resume(filename: str, content: bytes):
    # Initialize variables to avoid UnboundLocalError
    temp_doc_path = None
    pdf_path = None

    try:
        if filename.lower().endswith(".pdf"):
            text = read_pdf(content)
        elif filename.lower().endswith((".docx", ".doc")):
            # Create temp file
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_doc:
                temp_doc.write(content)
                temp_doc_path = temp_doc.name

            # Convert to PDF
            pdf_path = convert_to_pdf(temp_doc_path)  # This must return the PDF path

            # Read the converted PDF
            with open(pdf_path, "rb") as pdf_file:
                text = read_pdf(pdf_file.read())
        else:
            raise ValueError(f"Unsupported file format: {filename}")

        # Process extracted text
        return {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text),
            "years_experience": extract_years_experience(text),
            "raw_text": text[:1000]
        }

    except Exception as e:
        raise ValueError(f"Resume parsing failed: {str(e)}")

    finally:
        # Cleanup in reverse order of creation
        if pdf_path and os.path.exists(pdf_path):
            os.unlink(pdf_path)
        if temp_doc_path and os.path.exists(temp_doc_path):
            os.unlink(temp_doc_path)