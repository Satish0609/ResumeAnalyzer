A smart Streamlit web app that compares your resume with a job description (JD) and gives you a match score along with keyword insights.
It helps job seekers tailor their resumes to improve visibility and alignment with the target JD.

🔥 Features
🧠 Smart Resume Analysis – Upload a resume or provide a LinkedIn PDF URL

🎯 JD Matching – Paste the Job Description text

📊 Match Score – See how well your resume aligns with the JD (in %)

✅ Common Skills – Skills found in both resume and JD

❌ Missing Keywords – Keywords present in JD but missing in your resume

💡 Improvement Suggestions – Tips on what to add for better alignment

🎨 Attractive UI – Inspired by Swiggy/Zomato color scheme with neat layout

🛠️ Tech Stack
Frontend: Streamlit

Backend: Python

PDF Parsing: PyMuPDF (fitz)

NLP: Scikit-learn, NLTK / SpaCy (as per your matcher.py logic)

 How to Run Locally
Clone the Repository
git clone https://github.com/yourusername/resume-jd-matcher.git
cd resume-jd-matcher

Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install Requirements
pip install -r requirements.txt

Run the App
streamlit run app.py

📁 Folder Structure

resume-jd-matcher/
│
├── app.py                  # Main Streamlit app
├── matcher.py              # Core functions: PDF parsing, scoring, keyword extraction
├── requirements.txt        # Python dependencies
└── README.md               # You're reading this!
📸 Screenshot
![Screenshot (27)](https://github.com/user-attachments/assets/9aaec02d-50a1-4a83-8637-d006599b501a)
![Screenshot (28)](https://github.com/user-attachments/assets/12ded07a-538f-4e52-8a9c-041959c72296)

✨ Created By
Satish Raurmath
🎓 MCA Graduate | 💻 Software Developer | 🧠 Resume & Job Matcher Innovator
🔗 LinkedIn www.linkedin.com/in/satish-raurmath

