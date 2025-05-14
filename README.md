# AI Resume Analyzer (FastAPI)

An AI-powered resume analyzer that extracts key information from resumes (PDF/DOCX) and matches it against a given job description using semantic similarity (Sentence-BERT) and skills matching.

---

## Features

- Resume parsing: extract email, phone, skills, years of experience
- Supports `.pdf` and `.docx` resumes
- Job match scoring using BERT embeddings (`sentence-transformers`)
- Built with FastAPI for rapid API development
