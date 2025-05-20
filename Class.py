from pdfminer.high_level import extract_text
from docx import Document
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError("PDF not found!")
    return extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    if not os.path.exists(docx_path):
        raise FileNotFoundError("DOCX not found!")
    doc = Document(docx_path)
    return '\n'.join([para.text for para in doc.paragraphs])

# Test PDF
if __name__ == "__main__":
    # 🛠 Replace with your actual file path — use raw strings with 'r' or double backslashes
    pdf_resume = r"C:\Users\satis\Desktop\Satish Raurmath Resumes\Satish_Raurmath_Software_Developer_Resume.pdf"
    docx_resume = r"C:\Users\satis\Desktop\Satish Raurmath Resumes\Satish Raurmath Resume OG (2).docx"

    print("---- PDF Resume ----")
    print(extract_text_from_pdf(pdf_resume))

    print("---- DOCX Resume ----")
    print(extract_text_from_docx(docx_resume))
