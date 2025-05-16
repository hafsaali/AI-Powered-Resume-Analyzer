import fitz  # PyMuPDF
import subprocess
import os
from tempfile import mkdtemp


def read_pdf(content: bytes) -> str:
    text = ""
    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def convert_to_pdf(docx_path: str) -> str:
    """Returns path to converted PDF file"""
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    result = subprocess.run([
        soffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", os.path.dirname(docx_path),
        docx_path
    ], capture_output=True, text=True)

    if result.returncode != 0 or not os.path.exists(pdf_path):
        raise RuntimeError(f"Conversion failed: {result.stderr}")

    return pdf_path

