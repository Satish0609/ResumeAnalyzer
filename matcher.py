from nlp_utils import clean_text
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_resume_text(pdf_path):
    return extract_text(pdf_path)

def match_resume_with_jd(resume_text, jd_text):
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cleaned_resume, cleaned_jd])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    score = round(similarity[0][0] * 100, 2)
    return score

if __name__ == "__main__":
    # Change this to your actual PDF file path
    resume_path = r"C:\Users\satis\Desktop\Satish Raurmath Resumes\Satish_Raurmath_Software_Developer_Resume.pdf"
    jd_text = """
    3+ years of experience as a Python Developer with a strong portfolio of projects.
Bachelor's degree in Computer Science, Software Engineering or a related field.
In-depth understanding of the Python software development stacks, ecosystems, frameworks and tools such as Numpy, Scipy, Pandas, Dask, spaCy, NLTK, sci-kit-learn and PyTorch.
Experience with front-end development using HTML, CSS, and JavaScript.
Familiarity with database technologies such as SQL and NoSQL.
Excellent problem-solving ability with solid communication and collaboration skills.
Preferred skills and qualifications

Experience with popular Python frameworks such as Django, Flask or Pyramid.
Knowledge of data science and machine learning concepts and tools.
A working understanding of cloud platforms such as AWS, Google Cloud or Azure.
Contributions to open-source Python projects or active involvement in the Python community.
    """

    resume_text = extract_resume_text(resume_path)
    match_score = match_resume_with_jd(resume_text, jd_text)

    print(f"\n📝 Resume-JD Match Score: {match_score}%")
