import streamlit as st
from PyPDF2 import PdfReader
import re
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from io import BytesIO

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎯 CareerAI")
st.subheader("AI-Powered Career Recommendation & Resume Analyzer")

st.write(
    "Analyze your skills or upload your resume to discover "
    "the most suitable career paths."
)

# --------------------------------------------------
# SKILLS LIST
# --------------------------------------------------

skills_list = [
    # Programming
    "Python", "Java", "C", "C++", "C#", "JavaScript",
    "TypeScript", "PHP", "R", "Go", "Rust", "Kotlin",
    "Swift", "Dart", "MATLAB",

    # Data
    "Excel", "Advanced Excel", "SQL", "Power BI", "Tableau",
    "Google Sheets", "Pandas", "NumPy", "Matplotlib",
    "Seaborn", "Plotly", "Statistics", "Data Analysis",
    "Data Visualization", "Data Cleaning", "ETL",
    "Data Modeling", "Business Intelligence",

    # AI / ML
    "Artificial Intelligence", "Machine Learning",
    "Deep Learning", "NLP", "Computer Vision",
    "Reinforcement Learning", "TensorFlow", "PyTorch",
    "Keras", "Scikit-learn", "OpenCV", "XGBoost",
    "LightGBM", "Hugging Face", "Transformers",

    # Generative AI
    "Generative AI", "LLM", "Prompt Engineering",
    "LangChain", "LlamaIndex", "RAG", "AI Agents",
    "Fine-tuning", "Vector Databases",

    # Web
    "HTML", "CSS", "React", "Angular", "Vue.js",
    "Next.js", "Node.js", "Express.js", "Django",
    "Flask", "Spring Boot", "REST API", "GraphQL",

    # Mobile
    "Android Development", "Java Android",
    "Flutter", "React Native", "iOS Development",

    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Oracle",
    "SQLite", "Microsoft SQL Server", "Redis",
    "Firebase", "Database Design", "Database Administration",

    # Cloud
    "AWS", "Microsoft Azure", "Google Cloud",
    "Cloud Computing", "AWS EC2", "AWS S3",
    "AWS Lambda", "Azure Functions",

    # DevOps
    "Git", "GitHub", "GitLab", "Docker", "Kubernetes",
    "Jenkins", "CI/CD", "Linux", "Terraform", "Ansible",

    # Cybersecurity
    "Cybersecurity", "Ethical Hacking", "Network Security",
    "Application Security", "Cloud Security", "Cryptography",
    "Penetration Testing", "OWASP", "Digital Forensics",
    "Vulnerability Assessment", "Security Operations",

    # Big Data
    "Big Data", "Hadoop", "Apache Spark", "Apache Kafka",
    "Hive", "Databricks", "Data Warehousing",

    # Software Engineering
    "Data Structures", "Algorithms", "OOP",
    "System Design", "Software Architecture",
    "Software Development", "Software Testing",
    "Unit Testing", "Debugging", "Agile", "Scrum",

    # Testing
    "Manual Testing", "Automation Testing",
    "Selenium", "JUnit", "PyTest", "API Testing",
    "Performance Testing",

    # UI/UX
    "UI Design", "UX Design", "UI/UX Design",
    "Figma", "Adobe XD", "Wireframing",
    "Prototyping", "User Research",

    # Tools
    "VS Code", "Jupyter Notebook", "Google Colab",
    "Postman", "Jira", "Notion", "Anaconda",

    # Business
    "Business Analysis", "Market Research",
    "Project Management", "Product Management",
    "Business Strategy", "Financial Analysis",

    # Soft Skills
    "Communication", "Leadership", "Teamwork",
    "Problem Solving", "Critical Thinking",
    "Time Management", "Presentation Skills",
    "Public Speaking"
]

# --------------------------------------------------
# CAREER DATA
# --------------------------------------------------

career_data = {

    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Statistics", "Pandas", "Data Visualization"
    ],

    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning",
        "Pandas", "NumPy", "Scikit-learn"
    ],

    "Business Intelligence Analyst": [
        "SQL", "Excel", "Power BI", "Tableau",
        "Data Visualization"
    ],

    "Business Analyst": [
        "Excel", "SQL", "Power BI", "Statistics",
        "Communication", "Problem Solving", "Jira"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Scikit-learn",
        "TensorFlow", "Git", "SQL", "Docker"
    ],

    "AI Engineer": [
        "Python", "Artificial Intelligence",
        "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch"
    ],

    "Deep Learning Engineer": [
        "Python", "Deep Learning", "TensorFlow",
        "PyTorch", "NumPy"
    ],

    "NLP Engineer": [
        "Python", "NLP", "Machine Learning",
        "Deep Learning", "Transformers"
    ],

    "Computer Vision Engineer": [
        "Python", "Computer Vision", "OpenCV",
        "Deep Learning", "TensorFlow"
    ],

    "Generative AI Engineer": [
        "Python", "Generative AI", "LLM",
        "Prompt Engineering", "LangChain", "RAG"
    ],

    "Python Developer": [
        "Python", "Git", "REST API",
        "Django", "Flask"
    ],

    "Java Developer": [
        "Java", "OOP", "Spring Boot",
        "SQL", "Git"
    ],

    "Software Engineer": [
        "Python", "Java", "Data Structures",
        "Algorithms", "OOP", "Git"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript",
        "React", "Git"
    ],

    "Backend Developer": [
        "Python", "Node.js", "REST API",
        "SQL", "MongoDB", "Git"
    ],

    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript",
        "React", "Node.js", "SQL", "Git"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript",
        "REST API", "Git"
    ],

    "Mobile App Developer": [
        "Flutter", "Dart", "Android Development",
        "React Native"
    ],

    "Cloud Engineer": [
        "AWS", "Cloud Computing", "Linux",
        "Docker", "Git"
    ],

    "DevOps Engineer": [
        "Linux", "Docker", "Kubernetes",
        "Jenkins", "CI/CD", "Git"
    ],

    "Cybersecurity Analyst": [
        "Cybersecurity", "Network Security",
        "Linux", "OWASP"
    ],

    "Ethical Hacker": [
        "Ethical Hacking", "Cybersecurity",
        "Penetration Testing", "Linux"
    ],

    "Database Administrator": [
        "SQL", "MySQL", "PostgreSQL",
        "Database Administration"
    ],

    "Big Data Engineer": [
        "Python", "SQL", "Big Data",
        "Hadoop", "Apache Spark", "Apache Kafka"
    ],

    "QA Engineer": [
        "Software Testing", "Manual Testing",
        "SQL", "Git"
    ],

    "Automation Test Engineer": [
        "Automation Testing", "Selenium",
        "PyTest", "Python", "Git"
    ],

    "UI/UX Designer": [
        "UI Design", "UX Design",
        "Figma", "Wireframing", "Prototyping"
    ],

    "Product Manager": [
        "Product Management", "Communication",
        "Leadership", "Project Management"
    ],

    "Technical Consultant": [
        "Python", "SQL", "Communication",
        "Problem Solving", "Business Analysis"
    ],

    "Solutions Architect": [
        "System Design", "Cloud Computing",
        "AWS", "Software Architecture"
    ],

    "System Administrator": [
        "Linux", "Networking", "Cloud Computing",
        "Cybersecurity"
    ]
}
def calculate_ai_career_match(resume_text):

    career_names = list(career_data.keys())

    career_documents = []

    for career in career_names:

        skills = career_data[career]

        career_documents.append(
            career + " " + " ".join(skills)
        )

    documents = [resume_text] + career_documents

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    results = []

    for i, career in enumerate(career_names):

        score = round(
            similarity_scores[i] * 100,
            2
        )

        results.append({
            "career": career,
            "ai_score": score
        })

    results.sort(
        key=lambda x: x["ai_score"],
        reverse=True
    )

    return results
# --------------------------------------------------
# CAREER ANALYSIS FUNCTION
# --------------------------------------------------

def analyze_careers(user_skills):

    user_skills_lower = {
        skill.lower() for skill in user_skills
    }

    results = []

    for career, required_skills in career_data.items():

        matching = [
            skill for skill in required_skills
            if skill.lower() in user_skills_lower
        ]

        missing = [
            skill for skill in required_skills
            if skill.lower() not in user_skills_lower
        ]

        score = round(
            (len(matching) / len(required_skills)) * 100
        )

        results.append({
            "career": career,
            "score": score,
            "matching": matching,
            "missing": missing
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:5]


# --------------------------------------------------
# ACCURATE SKILL DETECTION
# --------------------------------------------------

def detect_resume_skills(resume_text):

    detected = []

    text = resume_text.lower()

    for skill in skills_list:

        skill_lower = skill.lower()

        # Special handling for one-letter skills
        if skill_lower in ["c", "r"]:
            pattern = r"(?<![a-z])" + re.escape(skill_lower) + r"(?![a-z])"

        # Special handling for "Go"
        elif skill_lower == "go":
            pattern = r"(?<![a-z])go(?![a-z])"

        else:
            pattern = r"(?<![a-z0-9])" + re.escape(skill_lower) + r"(?![a-z0-9])"

        if re.search(pattern, text):
            detected.append(skill)

    return detected
def create_career_report(career, final_score, skill_score, ai_score, matching, missing):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("CareerAI Career Report", styles["Title"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Recommended Career: {career}", styles["Heading2"]))
    story.append(Paragraph(f"Final CareerAI Score: {final_score}%", styles["BodyText"]))
    story.append(Paragraph(f"Skill Match Score: {skill_score}%", styles["BodyText"]))
    story.append(Paragraph(f"AI Similarity Score: {ai_score}%", styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Matching Skills", styles["Heading3"]))
    if matching:
        for skill in matching:
            story.append(Paragraph(f"- {skill}", styles["BodyText"]))
    else:
        story.append(Paragraph("- None", styles["BodyText"]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Skills to Learn", styles["Heading3"]))
    if missing:
        for skill in missing:
            story.append(Paragraph(f"- {skill}", styles["BodyText"]))
    else:
        story.append(Paragraph("- None", styles["BodyText"]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Recommended Roadmap", styles["Heading3"]))
    if missing:
        story.append(Paragraph(
            "Learn the missing skills, build 2-3 practical projects, and prepare for interviews.",
            styles["BodyText"]
        ))
    else:
        story.append(Paragraph(
            "Build real-world projects and prepare for interviews.",
            styles["BodyText"]
        ))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------------------------------
# CANDIDATE PROFILE
# --------------------------------------------------

st.divider()

st.header("👤 Candidate Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Enter Your Name"
    )

with col2:

    education = st.selectbox(
        "Education",
        [
            "B.Tech / B.E",
            "B.Sc",
            "BCA",
            "MCA",
            "M.Tech",
            "Other"
        ]
    )

selected_skills = st.multiselect(
    "Select Your Skills",
    skills_list
)


# --------------------------------------------------
# MANUAL CAREER ANALYSIS
# --------------------------------------------------

if st.button(
    "🚀 Find My Best Career Paths",
    use_container_width=True
):

    if not name:

        st.warning(
            "Please enter your name."
        )

    elif not selected_skills:

        st.warning(
            "Please select at least one skill."
        )

    else:

        results = analyze_careers(
            selected_skills
        )

        st.success(
            f"Hello {name}! Here are your best career paths."
        )

        for index, result in enumerate(results, 1):

            st.subheader(
                f"{index}. {result['career']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Career Match",
                    f"{result['score']}%"
                )

            with col2:
                st.metric(
                    "Matching Skills",
                    len(result["matching"])
                )

            with col3:
                st.metric(
                    "Skills to Learn",
                    len(result["missing"])
                )

            if result["matching"]:

                st.write(
                    "✅ **Matching:** " +
                    ", ".join(result["matching"])
                )

            if result["missing"]:

                st.write(
                    "📚 **Skills to Learn:** " +
                    ", ".join(result["missing"])
                )

        # Best career
        best = results[0]

        st.divider()

        st.header("🥇 Best Career For You")

        st.success(
            f"{best['career']} — {best['score']}% Match"
        )

        # Skill gap chart
        if best["missing"]:

            st.subheader("📊 Skill Gap Chart")

            chart_data = {
                "Category": [
                    "Matching Skills",
                    "Skills to Learn"
                ],
                "Count": [
                    len(best["matching"]),
                    len(best["missing"])
                ]
            }

            fig = px.bar(
                chart_data,
                x="Category",
                y="Count",
                title=f"Skill Gap – {best['career']}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "🎉 You already have all required skills for this career!"
            )


# --------------------------------------------------
# RESUME ANALYZER
# --------------------------------------------------

st.divider()
st.header("📄 Resume Analyzer")
st.write(
    "Upload your resume PDF. CareerAI will extract the text, "
    "detect your skills and recommend careers."
)

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


if uploaded_resume:
    st.success("Resume uploaded successfully!")

    try:
        reader = PdfReader(uploaded_resume)
        resume_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text += page_text + "\\n"

        if resume_text.strip():
            st.subheader("📑 Extracted Resume Text")
            st.text_area(
                "Resume Content",
                resume_text,
                height=250
            )

            detected_skills = detect_resume_skills(resume_text)

            st.subheader("🔍 Skills Detected From Resume")

            if detected_skills:
                for skill in detected_skills:
                    st.write(f"✅ {skill}")

                st.success(
                    f"{len(detected_skills)} skills detected from your resume!"
                )

                # --------------------------------------------------
                # FINAL CAREERAI RANKING
                # 60% skill match + 40% NLP similarity
                # --------------------------------------------------
                ai_results = calculate_ai_career_match(resume_text)
                ai_scores = {
                    item["career"]: item["ai_score"]
                    for item in ai_results
                }

                resume_results = []
                user_skills_lower = {
                    skill.lower() for skill in detected_skills
                }

                for career, required_skills in career_data.items():
                    matching = [
                        skill for skill in required_skills
                        if skill.lower() in user_skills_lower
                    ]

                    missing = [
                        skill for skill in required_skills
                        if skill.lower() not in user_skills_lower
                    ]

                    skill_score = round(
                        (len(matching) / len(required_skills)) * 100
                    )

                    ai_score = ai_scores.get(career, 0)

                    final_score = round(
                        (skill_score * 0.60) + (ai_score * 0.40),
                        2
                    )

                    resume_results.append({
                        "career": career,
                        "score": skill_score,
                        "ai_score": ai_score,
                        "final_score": final_score,
                        "matching": matching,
                        "missing": missing
                    })

                resume_results.sort(
                    key=lambda x: x["final_score"],
                    reverse=True
                )

                top_results = resume_results[:5]

                st.subheader("🏆 Final CareerAI Ranking")

                for index, result in enumerate(top_results, 1):
                    st.write(f"### {index}. {result['career']}")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Final CareerAI Score",
                            f"{result['final_score']}%"
                        )

                    with col2:
                        st.metric(
                            "Skill Match",
                            f"{result['score']}%"
                        )

                    with col3:
                        st.metric(
                            "AI Similarity",
                            f"{result['ai_score']}%"
                        )

                    st.progress(
                        min(result["final_score"] / 100, 1.0)
                    )

                    if result["matching"]:
                        st.write(
                            "✅ Matching: " +
                            ", ".join(result["matching"])
                        )

                    if result["missing"]:
                        st.write(
                            "📚 Skills to Learn: " +
                            ", ".join(result["missing"])
                        )

                # --------------------------------------------------
                # BEST CAREER
                # --------------------------------------------------
                best_resume_career = top_results[0]

                st.divider()
                st.header("🥇 Best Career Based on Resume")

                st.success(
                    f"{best_resume_career['career']} — "
                    f"{best_resume_career['final_score']}% Final Match"
                )

                # --------------------------------------------------
                # DOWNLOAD REPORT
                # --------------------------------------------------
                report_pdf = create_career_report(
                    best_resume_career["career"],
                    best_resume_career["final_score"],
                    best_resume_career["score"],
                    best_resume_career["ai_score"],
                    best_resume_career["matching"],
                    best_resume_career["missing"]
                )

                st.download_button(
                    label="📄 Download CareerAI Report PDF",
                    data=report_pdf,
                    file_name="CareerAI_Career_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

                # --------------------------------------------------
                # SKILL GAP
                # --------------------------------------------------
                st.subheader("🗺️ Your Skill Gap")

                missing = best_resume_career["missing"]
                matching = best_resume_career["matching"]

                if missing:
                    st.warning("Skills you should learn:")

                    for skill in missing:
                        st.write(f"📚 {skill}")

                    chart_data = {
                        "Category": [
                            "Current Skills",
                            "Skills to Learn"
                        ],
                        "Count": [
                            len(matching),
                            len(missing)
                        ]
                    }

                    fig = px.bar(
                        chart_data,
                        x="Category",
                        y="Count",
                        title="Resume Skill Gap"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                else:
                    st.success(
                        "🎉 Your resume already contains all required skills for this career!"
                    )

                # --------------------------------------------------
                # ROADMAP
                # --------------------------------------------------
                st.subheader("🛣️ Recommended Learning Roadmap")

                if missing:
                    for i, skill in enumerate(missing, 1):
                        st.write(f"**Step {i}:** Learn {skill}")

                    st.write(
                        "💡 After learning these skills, build 2–3 practical "
                        "projects and add them to your GitHub and LinkedIn."
                    )
                else:
                    st.write(
                        "Your next step should be building real-world projects "
                        "and preparing for interviews."
                    )

            else:
                st.warning(
                    "No supported skills were detected. "
                    "Try uploading a text-based PDF resume."
                )

        else:
            st.warning(
                "Could not extract text from this PDF. "
                "Please upload a text-based resume."
            )

    except Exception as e:
        st.error(f"Error reading resume: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "🎯 CareerAI | AI & Data Science Career Recommendation Platform"
)