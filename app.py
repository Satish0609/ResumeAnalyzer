import streamlit as st
import validators
import urllib.request
from matcher import extract_resume_text, get_match_score, extract_keywords
from io import BytesIO

# 🎨 Page setup
st.set_page_config(page_title="Resume-JD Matcher", page_icon="📄", layout="centered")
st.markdown("""
    <style>
    .main {
        background-color: #fff9f0;
    }
    h1 {
        color: #ff6600;
        text-align: center;
        font-size: 36px;
    }
    .stButton>button {
        background-color: #ff6600;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTextArea textarea, .stTextInput input {
        border: 2px solid #ff6600;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Resume to Job Description Matcher")

# 🚀 Upload or paste resume
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])
linkedin_url = st.text_input("OR paste your LinkedIn Resume PDF URL")

# 📌 Paste JD
jd_text = st.text_area("Paste Job Description (JD)", height=180)

if st.button("🎯 Get the Score"):
    if not jd_text.strip():
        st.error("⚠️ Please paste a Job Description.")
    else:
        try:
            # Step 1: Get resume text
            if uploaded_file is not None:
                resume_text = extract_resume_text(BytesIO(uploaded_file.read()))
            elif linkedin_url:
                if not validators.url(linkedin_url):
                    st.error("❌ Invalid LinkedIn URL.")
                    st.stop()
                tmp_path = "temp_resume.pdf"
                urllib.request.urlretrieve(linkedin_url, tmp_path)
                resume_text = extract_resume_text(tmp_path)
            else:
                st.error("📄 Please upload a resume file or provide a LinkedIn PDF URL.")
                st.stop()

            # Step 2: Match and extract
            match_score = get_match_score(resume_text, jd_text)
            resume_keywords = extract_keywords(resume_text)
            jd_keywords = extract_keywords(jd_text)

            common_skills = resume_keywords & jd_keywords
            missing_skills = jd_keywords - resume_keywords

            # Output
            st.markdown(f"<h2 style='color:#27ae60;'>✅ Match Score: {match_score}%</h2>", unsafe_allow_html=True)

            st.markdown("### 🎯 Skills Found in Your Resume:")
            st.success(", ".join(sorted(common_skills)) if common_skills else "No common skills found.")

            st.markdown("### 🚫 Missing Keywords From JD:")
            st.warning(", ".join(sorted(missing_skills)) if missing_skills else "None. Great Job!")

            if missing_skills:
                st.info(f"💡 Add these keywords if relevant:\n\n**{', '.join(sorted(missing_skills))}**")
            else:
                st.balloons()
                st.success("🎉 Your resume already aligns well with the JD!")

        except Exception as e:
            st.error(f"❌ Error processing resume: {e}")
