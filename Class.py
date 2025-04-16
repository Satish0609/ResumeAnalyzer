import fitz  # PyMuPDF
import requests
import spacy
import re
import json
from bs4 import BeautifulSoup
from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_sm")

rapidapi_key = "<YOUR_RAPIDAPI_KEY>"  # Replace with your RapidAPI key
rapidapi_host = "jsearch.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": rapidapi_key,
    "X-RapidAPI-Host": rapidapi_host
}

# Extract text from uploaded resume PDF
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Fetch job descriptions via API
def fetch_job_descriptions_api(role: str) -> List[str]:
    url = f"https://jsearch.p.rapidapi.com/search?query={role}&num_pages=1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jobs = response.json().get("data", [])
        return [job.get("description", "") for job in jobs]
    return []

# Web scraping fallback

def fetch_job_descriptions_scrape(role: str) -> List[str]:
    url = f"https://in.indeed.com/jobs?q={role}&l="
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    for div in soup.find_all("div", class_="job_seen_beacon"):
        snippet = div.find("div", class_="job-snippet")
        if snippet:
            jobs.append(snippet.text.strip())
    return jobs[:5]  # limit to top 5

# Extract keywords from text
def extract_keywords(text: str) -> List[str]:
    skills = []
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        keyword = chunk.text.strip().lower()
        if len(keyword.split()) <= 3 and keyword.isalpha():
            skills.append(keyword)
    skills += re.findall(r"[A-Za-z0-9#\.\+\-]{2,}", text)  # catch tech terms
    return list(set([kw.lower() for kw in skills if len(kw) > 2]))

# Resume analyzer endpoint
@app.post("/analyze_resume")
async def analyze_resume(
        file: UploadFile = File(...),
        job_title: str = Form(...)):

    file_bytes = await file.read()
    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Failed to read PDF"})

    resume_keywords = extract_keywords(resume_text)

    # Fetch JDs from API and Scraping
    api_jds = fetch_job_descriptions_api(job_title)
    scrape_jds = fetch_job_descriptions_scrape(job_title)
    all_jds = " ".join(api_jds + scrape_jds)

    if not all_jds.strip():
        return JSONResponse(status_code=404, content={"error": "Could not fetch job description for given title."})

    job_keywords = extract_keywords(all_jds)

    # Keyword Matching
    missing_keywords = list(set(job_keywords) - set(resume_keywords))

    return {
        "matched_keywords": list(set(resume_keywords) & set(job_keywords)),
        "missing_keywords": missing_keywords,
        "suggestions": f"Try to include these terms in your resume to improve ATS score: {', '.join(missing_keywords[:15])}"
    }
