from pdfminer.high_level import extract_text
from nlp_utils import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🧠 Extract text from PDF
def extract_resume_text(pdf_path):
    return extract_text(pdf_path)


# 🤝 Match resume and JD
def get_match_score(resume_text, jd_text):
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cleaned_resume, cleaned_jd])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    score = round(similarity[0][0] * 100, 2)
    return score


# 🧹 Extract keywords from cleaned text
def extract_keywords(text):
    return set(clean_text(text).split())


# 🚀 MAIN
if __name__ == "__main__":
    resume_path = r"C:\Users\satis\Desktop\Satish Raurmath Resumes\Satish_Raurmath_Software_Developer_Resume.pdf"
    jd_text = """
    We are hiring a Backend Developer with 1-2 years of experience in Python, Flask, and MySQL. 
    Knowledge of REST APIs, Git, Docker, and Agile development is a plus.
    """

    resume_text = extract_resume_text(resume_path)
    match_score = match_resume_with_jd(resume_text, jd_text)

    print(f"\n📝 Resume-JD Match Score: {match_score}%")

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    common_skills = resume_keywords & jd_keywords
    missing_skills = jd_keywords - resume_keywords

    print("\n✅ Skills present in your resume:")
    print(", ".join(sorted(common_skills)))

    print("\n❌ Missing skills from JD:")
    print(", ".join(sorted(missing_skills)))

    print("\n💡 Recommendation:")
    if missing_skills:
        print(f"Try adding these keywords to your resume if relevant: {', '.join(sorted(missing_skills))}")
    else:
        print("Your resume already covers all the main keywords from the JD!")
