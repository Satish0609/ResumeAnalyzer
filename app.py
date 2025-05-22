import streamlit as st
from matcher import get_match_score, extract_resume_text
from jd_loader import load_jd# Assuming you have these in matcher.py

st.set_page_config(page_title="Resume-JD Matcher", page_icon="📄")

st.title("🤖 AI-Powered Resume & Job Description Matcher")
st.write(
    """
    Upload your resume and job description, and get instant feedback on how well your resume matches the job.
    Identify your strengths and find the skills you need to add to improve your chances.
    """
)

# Upload files & input JD text
resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description here")

if resume_file and jd_text:
    # Save uploaded resume temporarily
    with open("temp_resume", "wb") as f:
        f.write(resume_file.getbuffer())

    # Extract text based on file type
    if resume_file.type == "application/pdf":
        resume_text = extract_resume_text("temp_resume")
    else:
        from docx import Document

        doc = Document("temp_resume")
        resume_text = "\n".join([para.text for para in doc.paragraphs])

    # Load and clean JD
    # Assuming load_jd cleans text; if not, just use jd_text directly
    jd_cleaned = jd_text  # Or use your load_jd function if you want NLP cleaning

    # Get match results (assuming get_match_score returns dict with keys)
    results = get_match_score(resume_text, jd_cleaned)

    st.markdown("---")

    # Show overall score with color-coded progress bar
    score = results["score"]
    st.subheader(f"📝 Resume-JD Match Score: {score:.2f}%")
    st.progress(score / 100)

    st.markdown("---")

    # Show matched vs missing skills in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Skills present in your resume")
        for skill in results["matched_skills"]:
            st.markdown(f"<span style='color:green; font-weight:bold;'>• {skill}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("### ❌ Missing skills from JD")
        for skill in results["missing_skills"]:
            st.markdown(f"<span style='color:red; font-weight:bold;'>• {skill}</span>", unsafe_allow_html=True)

    st.markdown("---")

    # Recommendations
    st.subheader("💡 Recommendation")
    st.write("Try adding these keywords to your resume if relevant:")
    st.write(", ".join(results["missing_skills"]))

else:
    st.info("Upload your resume and paste the job description to see the match score.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2025 AI Resume Matcher — by Satish Raurmath")
