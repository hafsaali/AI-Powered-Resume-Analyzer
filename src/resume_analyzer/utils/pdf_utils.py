from io import BytesIO
import fitz  # PyMuPDF
import docx

def read_pdf(content: bytes) -> str:
    text = ""
    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def read_docx(content: bytes) -> str:
    doc = docx.Document(BytesIO(content))
    return "\n".join([p.text for p in doc.paragraphs])