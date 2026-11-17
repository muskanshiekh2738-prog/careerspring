import requests
import streamlit as st
from database.db import initialize_database, get_connection
from utils.auth import register_user, login_user
from utils.resume import generate_resume
from utils.courses import (
    initialize_courses,
    get_courses,
    get_course_content,
    save_course_progress,
    get_student_progress
)

from utils.certificate import generate_certificate

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="CareerSpring | Learn. Prepare. Achieve.",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def setup_database():
    initialize_database()
    initialize_courses()

setup_database()

# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- CUSTOM DESIGN ----------------



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background-color: #F5F0E5;
    font-family: 'DM Sans', sans-serif;
}

/* Make website text black */
.stApp p,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp label,
.stApp span,
.stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    color: #000000;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #F5F0E5 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #000000 !important;
}

/* Navigation options */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: transparent !important;
    color: #000000 !important;
    border-radius: 6px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color:  #E6D7AE !important;
}

/* Quiz options */
div[role="radiogroup"] label {
    background-color: #F5F0E5 !important;
    border-radius: 8px;
    padding: 10px;
}

/* Hero section */
.hero {
    background: linear-gradient(120deg, #A8BDAF, #C1D2C5);
    padding: 55px 45px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero h1,
.hero h3,
.hero p {
    color: #000000 !important;
}

/* Cards */
.card {
    background-color: #FFFFFF;
    padding: 24px;
    border-radius: 14px;
    border: 1px solid #E4DDCE;
    min-height: 155px;
    margin-bottom: 15px;
}

.card h3,
.card p {
    color: #000000 !important;
}

/* Section headings */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    margin-top: 25px;
    color: #000000 !important;
}

/* Buttons */
.stButton > button {
    background-color: #F5F0E5 !important;
    color: #000000 !important;
    border: 1px solid #A8BDAF !important;
    border-radius: 8px;
    padding: 10px 22px;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* Dropdowns */
.stSelectbox,
.stMultiSelect {
    color: #000000 !important;
}
/* Dropdowns */
/* Make error messages clearly visible */
div[data-testid="stAlert"] {
    background-color: #F5F0E5 !important;
    border: 1px solid #A8BDAF !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div {
    color: #C62828 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)




# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("# 🌱 CareerSpring")
    st.caption("LEARN. PREPARE. ACHIEVE.")
    st.divider()

    if st.session_state.logged_in:
        st.write(f"Welcome, {st.session_state.user['name']}!")

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "My Profile",
                "Resume Builder",
                "Career Assistant",
                "Job Matching",
                "Internship Finder",
                "Course Hub",
                "Mock Interview",
                "GitHub Analyzer",
                "Placement Readiness",
            ]
        )

        st.divider()

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    else:
        page = "Home"


# ---------------- HOME PAGE ----------------

if not st.session_state.logged_in:

    st.markdown("""
    <div class="hero">
        <h1>Build Your Future.<br>One Skill at a Time.</h1>
        <p>
        Your journey from student to professional starts here.
        Learn new skills, build your resume, discover opportunities,
        and prepare for your dream career.
        </p>
        <h3>Learn. Prepare. Achieve.</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔐 Student Login")

        email = st.text_input(
            "Email address",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):
            if not email.strip() or not password:
                st.error("Please enter your email and password.")
            else:
                success, user = login_user(email, password)

                if success:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with col2:
        st.markdown("### 📝 Create Student Account")

        name = st.text_input("Full name", key="register_name")
        new_email = st.text_input(
            "Email address",
            key="register_email"
        )
        new_password = st.text_input(
            "Create password (minimum 8 characters)",
            type="password",
            key="register_password"
        )

        if st.button("Register", use_container_width=True):
            success, message = register_user(
                name,
                new_email,
                new_password
            )

            if success:
                st.success(message)
                st.info("You can now log in using your new account.")
            else:
                st.error(message)

    st.divider()

    st.markdown("### Everything You Need to Grow")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <h3>📄 Resume Builder</h3>
            <p>Create professional resumes for your career journey.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h3>🎯 Smart Job Matching</h3>
            <p>Discover jobs and understand the skills you need.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <h3>📚 Learning Hub</h3>
            <p>Learn programming and improve your career readiness.</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------- STUDENT DASHBOARD ----------------

else:

    user = st.session_state.user

    if page == "Dashboard":

        st.markdown(
            f'<div class="hero"><h1>Welcome, {user["name"]}!</h1>'
            '<p>Your career journey starts with one small step.</p>'
            '<h3>Learn. Prepare. Achieve.</h3></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">Your Career Dashboard</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="card">
                <h3>📄 Resume</h3>
                <p>Build and download your professional resume.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card">
                <h3>🎓 Learning</h3>
                <p>Explore courses and develop new skills.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="card">
                <h3>💼 Opportunities</h3>
                <p>Explore jobs and internship opportunities.</p>
            </div>
            """, unsafe_allow_html=True)

        st.info(
            "Complete your profile and start building your career."
        )

        st.markdown(
            '<div class="section-title">📊 Your Career Progress</div>',
            unsafe_allow_html=True
        )

        progress_col1, progress_col2, progress_col3 = st.columns(3)

       
        
        # Get logged-in student's course progress
        user_id = st.session_state.user["id"]
        student_progress = get_student_progress(user_id)

        total_courses = len(get_courses())
        completed_courses = sum(
            1 for course in student_progress if course["completed"] == 1
        )

        progress_percentage = (
            int((completed_courses / total_courses) * 100)
            if total_courses > 0 else 0
        )

        
        
        with progress_col1:
            st.markdown(f"""
            <div style="background-color:#FFFFFF; padding:20px;
                        border-radius:12px; border:1px solid #E4DDCE;">
                <p style="color:#E5E5E5.; font-size:14px;">📚 Courses Available</p>
                <h2 style="color:#A8BDAF; margin:0;">{total_courses}</h2>
            </div>
            """, unsafe_allow_html=True)

        with progress_col2:
            st.markdown(f"""
            <div style="background-color:#FFFFFF; padding:20px;
                        border-radius:12px; border:1px solid #E4DDCE;">
                <p style="color:#E5E5E5.; font-size:14px;">🎯 Courses Completed</p>
                <h2 style="color:#A8BDAF; margin:0;">{completed_courses}</h2>
            </div>
            """, unsafe_allow_html=True)

        with progress_col3:
            st.markdown(f"""
            <div style="background-color:#FFFFFF; padding:20px;
                        border-radius:12px; border:1px solid #E4DDCE;">
                <p style="color:#E5E5E5.; font-size:14px;">📈 Learning Progress</p>
                <h2 style="color:#A8BDAF; margin:0;">{progress_percentage}%</h2>
            </div>
            """, unsafe_allow_html=True)




        st.markdown(
            '<div class="section-title">🚀 Quick Access</div>',
            unsafe_allow_html=True
        )

        quick_col1, quick_col2, quick_col3 = st.columns(3)

        with quick_col1:
            if st.button("📄 Open Resume Builder", use_container_width=True):
                st.session_state.page = "Resume Builder"
                st.rerun()

        with quick_col2:
            if st.button("🎓 Explore Courses", use_container_width=True):
                st.session_state.page = "Course Hub"
                st.rerun()

        with quick_col3:
            if st.button("💼 Find Jobs", use_container_width=True):
                st.session_state.page = "Job Matching"
                st.rerun()


    elif page == "My Profile":
        st.title("👤 My Student Profile")
        st.write("Complete your details to improve your career opportunities.")

        connection = get_connection()
        profile = connection.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        with st.form("profile_form"):

            st.subheader("Personal Information")

            phone = st.text_input(
                "Phone Number",
                value=(profile["phone"] or "") if profile else ""
            )

            college = st.text_input(
                "College Name",
                value=(profile["college"] or "") if profile else ""
            )

            st.subheader("Education")

            degree = st.text_input(
                "Degree (e.g. B.Tech, BCA, B.Sc.)",
                value=(profile["degree"] or "") if profile else ""
            )

            branch = st.text_input(
                "Branch / Specialization",
                value=(profile["branch"] or "") if profile else ""
            )

            graduation_year = st.number_input(
                "Graduation Year",
                min_value=2000,
                max_value=2100,
                value=(
                    int(profile["graduation_year"])
                    if profile and profile["graduation_year"]
                    else 2027
                )
            )

            st.subheader("Career Information")

            skills = st.text_area(
                "Technical Skills",
                value=(profile["skills"] or "") if profile else "",
                placeholder="Python, SQL, HTML, CSS, Java"
            )

            career_goal = st.text_area(
                "Career Goal",
                value=(profile["career_goal"] or "") if profile else "",
                placeholder="Example: Become a Python developer"
            )

            github_username = st.text_input(
                "GitHub Username",
                value=(profile["github_username"] or "") if profile else ""
            )

            submitted = st.form_submit_button(
                "Save My Profile",
                use_container_width=True
            )

        if submitted:
            connection = get_connection()

            connection.execute("""
                INSERT INTO profiles (
                    user_id, phone, college, degree, branch,
                    graduation_year, skills, career_goal,
                    github_username
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    phone = excluded.phone,
                    college = excluded.college,
                    degree = excluded.degree,
                    branch = excluded.branch,
                    graduation_year = excluded.graduation_year,
                    skills = excluded.skills,
                    career_goal = excluded.career_goal,
                    github_username = excluded.github_username
            """,
            )
            (
                user["id"],
                phone,
                college,
                degree,
                branch,
                int(graduation_year),
                skills,
                career_goal,
                github_username
            )

            connection.commit()
            connection.close()

            st.success("Your profile has been saved successfully! 🎉")

    elif page == "Resume Builder":
        st.title("📄 CareerSpring Resume Builder")
        st.write("Create a professional resume using your saved profile.")

        connection = get_connection()
        profile = connection.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        if not profile:
            st.warning("Please complete your profile before creating a resume.")
            st.info("Open My Profile and save your details first.")

        else:
            with st.form("resume_form"):
                st.subheader("Personal Details")

                st.text_input("Full Name", value=user["name"], disabled=True)
                st.text_input("Email", value=user["email"], disabled=True)
                st.text_input(
                    "Phone",
                    value=profile["phone"] or "",
                    disabled=True
                )
                st.text_input(
                    "College",
                    value=profile["college"] or "",
                    disabled=True
                )

                st.subheader("Professional Summary")

                objective = st.text_area(
                    "Career Objective",
                    placeholder="Write a short introduction about your career goals."
                )

                st.subheader("Education and Skills")

                education = st.text_area(
                    "Education",
                    value=(
                        f"{profile['degree'] or ''} - "
                        f"{profile['branch'] or ''}, "
                        f"{profile['college'] or ''}, "
                        f"Graduation: {profile['graduation_year'] or ''}"
                    )
                )

                skills = st.text_area(
                    "Technical Skills",
                    value=profile["skills"] or "",
                    help="Separate skills using commas."
                )

                st.subheader("Projects and Experience")

                projects = st.text_area(
                    "Projects",
                    placeholder="Example: Student Management System - Built using Python and SQLite."
                )

                experience = st.text_area(
                    "Internship / Experience",
                    placeholder="Enter your internship or work experience, if any."
                )

                certifications = st.text_area(
                    "Certifications",
                    placeholder="Enter your completed certifications."
                )

                submitted = st.form_submit_button(
                    "Generate My Resume",
                    use_container_width=True
                )

            if submitted:
                resume_data = {
                    "name": user["name"],
                    "email": user["email"],
                    "phone": profile["phone"] or "",
                    "location": "",
                    "career_objective": objective,
                    "education": [education] if education.strip() else [],
                    "skills": [
                        skill.strip()
                        for skill in skills.split(",")
                        if skill.strip()
                    ],
                    "projects": [
                        project.strip()
                        for project in projects.split("\n")
                        if project.strip()
                    ],
                    "experience": [
                        item.strip()
                        for item in experience.split("\n")
                        if item.strip()
                    ],
                    "certifications": [
                        item.strip()
                        for item in certifications.split("\n")
                        if item.strip()
                    ],
                    "linkedin": "",
                    "github": (
                        "https://github.com/" + profile["github_username"]
                        if profile["github_username"]
                        else ""
                    )
                }

                filename = f"resume_user_{user['id']}.docx"

                try:
                    file_path = generate_resume(
                        resume_data,
                        filename
                    )

                    st.success("Your resume has been generated successfully! 🎉")

                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download My Resume",
                            data=file.read(),
                            file_name="CareerSpring_Resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                except Exception as error:
                    st.error(f"Resume generation failed: {error}")

        
    elif page == "Career Assistant":
        st.title("🤖 AI Career Assistant")
        st.write("Get career suggestions based on your skills and interests.")

        connection = get_connection()
        profile = connection.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        if not profile or not profile["skills"]:
            st.warning("Please add your skills in My Profile first.")
        else:
            skills = [
                skill.strip().lower()
                for skill in profile["skills"].split(",")
                if skill.strip()
            ]

            st.subheader("Your Skills")
            st.write(", ".join(skills))

            st.subheader("Recommended Career Paths")

            career_paths = {
                "Python Developer": ["python", "sql", "django", "flask"],
                "Web Developer": ["html", "css", "javascript", "react"],
                "Data Analyst": ["python", "sql", "excel", "power bi"],
                "Machine Learning Engineer": ["python", "machine learning", "pandas", "numpy"],
                "Database Administrator": ["sql", "mysql", "database"]
            }

            for career, required_skills in career_paths.items():
                matched = [
                    skill for skill in required_skills
                    if skill in skills
                ]

                percentage = int(
                    len(matched) / len(required_skills) * 100
                )

                with st.expander(f"🎯 {career} — {percentage}% skill match"):
                    st.write("Matching skills:", ", ".join(matched) if matched else "None")
                    missing = [
                        skill for skill in required_skills
                        if skill not in skills
                    ]
                    st.write("Skills to learn:", ", ".join(missing) if missing else "You have all listed skills!")
                    st.progress(percentage / 100)


    
    elif page == "Job Matching":
        st.title("🎯 Job Matching")
        st.write("Find suitable career opportunities based on your skills.")

        # Get student skills from profile
        connection = get_connection()
        profile = connection.execute(
            "SELECT skills FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        if not profile or not profile["skills"].strip():
            st.warning("Please add your technical skills in My Profile first.")

        else:
            student_skills = {
                skill.strip().lower()
                for skill in profile["skills"].split(",")
                if skill.strip()
            }

            st.subheader("Your Skills")
            st.write(", ".join(sorted(student_skills)))

            # Sample job roles and required skills
            jobs = [
                {
                    "title": "Python Developer",
                    "type": "Entry Level",
                    "skills": ["python", "sql", "django", "git"]
                },
                {
                    "title": "Data Analyst",
                    "type": "Entry Level",
                    "skills": ["python", "sql", "excel", "power bi"]
                },
                {
                    "title": "Frontend Developer",
                    "type": "Internship",
                    "skills": ["html", "css", "javascript", "react"]
                },
                {
                    "title": "SQL Developer",
                    "type": "Entry Level",
                    "skills": ["sql", "mysql", "database", "python"]
                },
                {
                    "title": "Machine Learning Intern",
                    "type": "Internship",
                    "skills": ["python", "machine learning", "pandas", "numpy"]
                }
            ]

            # Calculate job matches
            results = []

            for job in jobs:
                matched = [
                    skill for skill in job["skills"]
                    if skill in student_skills
                ]

                missing = [
                    skill for skill in job["skills"]
                    if skill not in student_skills
                ]

                percentage = int(
                    len(matched) / len(job["skills"]) * 100
                )

                results.append({
                    "job": job,
                    "matched": matched,
                    "missing": missing,
                    "percentage": percentage
                })

            results.sort(
                key=lambda item: item["percentage"],
                reverse=True
            )

            st.subheader("💼 Recommended Job Roles")
            st.caption("These are sample recommendations, not live job vacancies.")

            for result in results:
                job = result["job"]

                with st.expander(
                    f"{job['title']} — {result['percentage']}% Match"
                ):
                    st.write("**Job Type:**", job["type"])

                    st.write(
                        "**Matching Skills:**",
                        ", ".join(result["matched"])
                        if result["matched"] else "No matching skills yet"
                    )

                    st.write(
                        "**Skills to Learn:**",
                        ", ".join(result["missing"])
                        if result["missing"] else "You have all required skills!"
                    )

                    st.progress(result["percentage"] / 100)

                    if result["percentage"] >= 75:
                        st.success("Strong skill match!")
                    elif result["percentage"] >= 40:
                        st.info("Good starting point. Improve your missing skills.")
                    else:
                        st.warning("Build more relevant skills for this role.")


    
    elif page == "Internship Finder":
        st.title("💼 Internship Finder")
        st.write("Discover internships that match your technical skills.")

        # Get skills from student profile
        connection = get_connection()
        profile = connection.execute(
            "SELECT skills FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        if not profile or not profile["skills"].strip():
            st.warning("Please add your technical skills in My Profile first.")

        else:
            student_skills = {
                skill.strip().lower()
                for skill in profile["skills"].split(",")
                if skill.strip()
            }

            internships = [
                {
                    "title": "Python Developer Intern",
                    "domain": "Software Development",
                    "duration": "3 Months",
                    "mode": "Remote",
                    "skills": ["python", "sql", "django", "git"]
                },
                {
                    "title": "Data Analyst Intern",
                    "domain": "Data Science",
                    "duration": "2 Months",
                    "mode": "Hybrid",
                    "skills": ["python", "sql", "excel", "power bi"]
                },
                {
                    "title": "Frontend Developer Intern",
                    "domain": "Web Development",
                    "duration": "3 Months",
                    "mode": "Remote",
                    "skills": ["html", "css", "javascript", "react"]
                },
                {
                    "title": "Machine Learning Intern",
                    "domain": "Artificial Intelligence",
                    "duration": "6 Months",
                    "mode": "On-site",
                    "skills": ["python", "machine learning", "pandas", "numpy"]
                },
                {
                    "title": "Database Intern",
                    "domain": "Database",
                    "duration": "2 Months",
                    "mode": "Hybrid",
                    "skills": ["sql", "mysql", "database", "python"]
                }
            ]

            st.subheader("🔎 Find Your Internship")

            domains = ["All Domains"] + sorted(
                set(item["domain"] for item in internships)
            )

            selected_domain = st.selectbox(
                "Choose Internship Domain",
                domains
            )

            if selected_domain != "All Domains":
                filtered_internships = [
                    item for item in internships
                    if item["domain"] == selected_domain
                ]
            else:
                filtered_internships = internships

            st.subheader("Available Internship Opportunities")
            st.caption("These are sample opportunities for demonstration, not live vacancies.")

            for internship in filtered_internships:
                matched = [
                    skill for skill in internship["skills"]
                    if skill in student_skills
                ]

                missing = [
                    skill for skill in internship["skills"]
                    if skill not in student_skills
                ]

                percentage = int(
                    len(matched) / len(internship["skills"]) * 100
                )

                with st.expander(
                    f"💼 {internship['title']} — {percentage}% Match"
                ):
                    st.write("**Domain:**", internship["domain"])
                    st.write("**Duration:**", internship["duration"])
                    st.write("**Work Mode:**", internship["mode"])

                    st.write(
                        "**Matching Skills:**",
                        ", ".join(matched) if matched else "None yet"
                    )

                    st.write(
                        "**Skills to Improve:**",
                        ", ".join(missing) if missing else "You have all required skills!"
                    )

                    st.progress(percentage / 100)


    elif page == "Course Hub":
        st.title("📚 Course Learning Hub")
        st.write("Learn new skills, complete quizzes and earn certificates!")

        # Get available courses
        courses = get_courses()

        if not courses:
            st.warning("No courses available. Please restart the application.")
        else:
            course_names = [course["title"] for course in courses]

            selected_course_name = st.selectbox(
                "Choose a Course",
                options=course_names,
                index=0,
                key="course_selector"
            )


            selected_course = next(
                course for course in courses
                if course["title"] == selected_course_name
            )

            course_content = get_course_content(selected_course_name)

            if course_content:
                st.markdown("---")
                st.subheader(f"📖 {selected_course_name}")
                st.write(selected_course["description"])

                # Lessons
                lessons = course_content["lessons"]

                lesson_titles = [
                    lesson["title"] for lesson in lessons
                ]

                selected_lesson_title = st.selectbox(
                    "Choose a Lesson",
                    lesson_titles
                )

                selected_lesson = next(
                    lesson for lesson in lessons
                    if lesson["title"] == selected_lesson_title
                )

                st.markdown("### 📘 Lesson Content")
                st.write(selected_lesson["content"])

                # Quiz
                st.markdown("---")
                st.subheader("📝 Course Quiz")
                st.write("Answer all five questions. You need 60% to pass.")

                quiz = course_content["quiz"]

                with st.form(
                    key=f"quiz_form_{selected_course['id']}"
                ):
                    answers = []

                    for index, question in enumerate(quiz):
                        st.markdown(
                            f"**Q{index + 1}. {question['question']}**"
                        )

                        answer = st.radio(
    "Select your answer:",
    options=question["options"],
    key=f"answer_{selected_course['id']}_{index}"
)

                        answers.append(answer)

                    quiz_submitted = st.form_submit_button(
                        "Submit Quiz"
                    )

                if quiz_submitted:
                    if any(answer is None for answer in answers):
                        st.warning("Please answer all questions before submitting.")
                    else:
                        correct_answers = 0

                        for index, question in enumerate(quiz):
                            if answers[index] == question["answer"]:
                                correct_answers += 1

                        score = int(
                            (correct_answers / len(quiz)) * 100
                        )

                        passed = score >= 60

                        save_course_progress(
                            user["id"],
                            selected_course["id"],
                            score
                        )

                        result_key = (
                            f"course_result_{selected_course['id']}"
                        )

                        st.session_state[result_key] = {
                            "score": score,
                            "passed": passed
                        }

                        if passed:
                            certificate_path = generate_certificate(
                                user["name"],
                                selected_course_name
                            )

                            st.session_state[
                                f"certificate_{selected_course['id']}"
                            ] = str(certificate_path)

                # Display quiz result
                result_key = f"course_result_{selected_course['id']}"
                result = st.session_state.get(result_key)

                if result:
                    st.markdown("---")
                    st.subheader("📊 Your Quiz Result")

                    st.metric(
                        "Your Score",
                        f"{result['score']}%"
                    )

                    if result["passed"]:
                        st.success(
                            "Congratulations! You passed the quiz."
                        )

                        certificate_path = st.session_state.get(
                            f"certificate_{selected_course['id']}"
                        )

                        if certificate_path:
                            with open(certificate_path, "rb") as file:
                                st.download_button(
                                    label="🎓 Download Your Certificate",
                                    data=file,
                                    file_name=(
                                        f"{selected_course_name}_Certificate.pdf"
                                    ),
                                    mime="application/pdf"
                                )
                    else:
                        st.warning(
                            "You did not pass. Score at least 60% "
                            "to earn your certificate. Try again!"
                        )

            # Student progress
            st.markdown("---")
            st.subheader("📈 Your Learning Progress")

            progress = get_student_progress(user["id"])

            if progress:
                for item in progress:
                    st.write(
                        f"**{item['title']}** — "
                        f"Score: {item['score']}%"
                    )

                    st.progress(
                        min(item["score"] / 100, 1.0)
                    )
            else:
                st.info("You haven't completed any course quizzes yet.")

    

    
    elif page == "Mock Interview":

       

        st.markdown("""
        <style>
        /* Mock Interview page only */

        /* Question box */
        div[data-testid="stAlert"] {
            background-color: #A8BDAF !important;
        }

        div[data-testid="stAlert"] * {
            color: #F5F0E5 !important;
        }

        /* Answer text area */
        div[data-testid="stTextArea"] textarea {
            background-color: #FFFFFF !important;
            color: #A8BDAF !important;
            border: 1px solid #A9BDAA !important;
        }

        div[data-testid="stTextArea"] textarea::placeholder {
            color: #66786D !important;
            opacity: 1 !important;
        }

        /* Buttons */
        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button {
            background-color: #E6D7AE !important;
            color: #A8BDAF !important;
            border: 1px solid #E6D7AE !important;
        }

        div[data-testid="stButton"] button p,
        div[data-testid="stFormSubmitButton"] button p {
            color: #A8BDAF !important;
        }

        </style>
        """, unsafe_allow_html=True)


        st.title("🎤 AI Mock Interview")
        st.write("Practice interview questions and improve your answers.")

        interview_questions = {
            "Python Developer": [
                ("What is Python and why is it popular?",
                 ["python", "programming", "language", "simple", "readable"]),
                ("What is the difference between a list and a tuple?",
                 ["list", "tuple", "mutable", "immutable"]),
                ("What is object-oriented programming?",
                 ["class", "object", "inheritance", "encapsulation"]),
                ("What is exception handling in Python?",
                 ["try", "except", "error", "exception"])
            ],
            "Web Developer": [
                ("What is HTML used for?",
                 ["html", "structure", "webpage", "elements"]),
                ("What is the difference between CSS and JavaScript?",
                 ["css", "style", "javascript", "functionality"]),
                ("What is responsive web design?",
                 ["responsive", "devices", "screen", "layout"]),
                ("What is a frontend framework?",
                 ["framework", "react", "components", "interface"])
            ],
            "Data Analyst": [
                ("What is data analysis?",
                 ["data", "analyze", "insights", "decisions"]),
                ("What is SQL used for?",
                 ["sql", "database", "query", "data"]),
                ("What is the purpose of data visualization?",
                 ["visualization", "charts", "graphs", "patterns"]),
                ("What is the difference between mean and median?",
                 ["mean", "average", "median", "middle"])
            ]
        }

        selected_role = st.selectbox(
            "Select your interview role",
            list(interview_questions.keys())
        )

        if "mock_question_index" not in st.session_state:
            st.session_state.mock_question_index = 0

        questions = interview_questions[selected_role]

        question_index = (
            st.session_state.mock_question_index % len(questions)
        )

        question, keywords = questions[question_index]

        st.subheader(
            f"Question {question_index + 1} of {len(questions)}"
        )

        st.info(question)

        with st.form("mock_interview_form"):
            answer = st.text_area(
                "Write your answer:",
                height=180,
                placeholder="Type your interview answer here..."
            )

            submitted = st.form_submit_button(
                "Submit Answer",
                use_container_width=True
            )

        if submitted:
            if not answer.strip():
                st.warning("Please write an answer before submitting.")

            else:
                answer_words = answer.lower().split()

                matched_keywords = [
                    word for word in keywords
                    if word in answer.lower()
                ]

                score = int(
                    len(matched_keywords) / len(keywords) * 100
                )

                st.subheader("📊 Interview Feedback")

                st.write("**Your Score:**", f"{score}%")
                st.progress(score / 100)

                st.write(
                    "**Relevant concepts covered:**",
                    ", ".join(matched_keywords)
                    if matched_keywords else "No expected keywords found"
                )

                st.write(
                    "**Answer Length:**",
                    f"{len(answer_words)} words"
                )

                if score >= 70:
                    st.success("Good answer! You covered several important concepts.")
                elif score >= 40:
                    st.info("Good attempt! Add more relevant concepts to improve.")
                else:
                    st.warning("Keep practicing. Try including more key concepts.")

                st.caption(
                    "This is basic keyword-based feedback, not an evaluation "
                    "of the full correctness or quality of your answer."
                )

        if st.button("Next Question", use_container_width=True):
            st.session_state.mock_question_index += 1
            st.rerun()


    
    elif page == "GitHub Analyzer":
        st.title("🐙 GitHub Portfolio Analyzer")
        st.write("Analyze your public GitHub profile and coding portfolio.")

        # Get GitHub username from student profile
        connection = get_connection()
        profile = connection.execute(
            "SELECT github_username FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        saved_username = (
            profile["github_username"]
            if profile and profile["github_username"]
            else ""
        )

        github_username = st.text_input(
            "Enter your GitHub username",
            value=saved_username,
            placeholder="Example: torvalds"
        )

        if st.button("Analyze GitHub Profile", use_container_width=True):

            if not github_username.strip():
                st.warning("Please enter your GitHub username.")

            else:
                username = github_username.strip()

                try:
                    response = requests.get(
                        f"https://api.github.com/users/{username}",
                        timeout=10
                    )

                    if response.status_code == 200:
                        github_data = response.json()

                        repo_response = requests.get(
                            f"https://api.github.com/users/{username}/repos",
                            params={"per_page": 100, "sort": "updated"},
                            timeout=10
                        )

                        if repo_response.status_code == 200:
                            repositories = repo_response.json()

                            total_stars = sum(
                                repo["stargazers_count"]
                                for repo in repositories
                            )

                            st.subheader("👤 GitHub Profile")

                            col1, col2, col3 = st.columns(3)

                            col1.metric(
                                "Public Repositories",
                                github_data["public_repos"]
                            )

                            col2.metric(
                                "Followers",
                                github_data["followers"]
                            )

                            col3.metric(
                                "Total Stars",
                                total_stars
                            )

                            st.write(
                                "**Name:**",
                                github_data.get("name") or username
                            )

                            st.write(
                                "**Bio:**",
                                github_data.get("bio") or "No bio available"
                            )

                            st.markdown(
                                f"[Visit GitHub Profile](https://github.com/{username})"
                            )

                            st.subheader("💻 Programming Languages")

                            language_counts = {}

                            for repo in repositories:
                                language = repo.get("language")

                                if language:
                                    language_counts[language] = (
                                        language_counts.get(language, 0) + 1
                                    )

                            if language_counts:
                                st.bar_chart(language_counts)
                            else:
                                st.info("No programming language data found.")

                            st.subheader("📁 Recently Updated Repositories")

                            if repositories:
                                for repo in repositories[:5]:
                                    st.markdown(
                                        f"**[{repo['name']}]({repo['html_url']})**"
                                    )

                                    st.write(
                                        f"Language: {repo.get('language') or 'Not specified'}"
                                        f" | ⭐ Stars: {repo['stargazers_count']}"
                                    )
                            else:
                                st.info("No public repositories found.")

                        else:
                            st.error("Could not retrieve repositories.")

                    elif response.status_code == 404:
                        st.error("GitHub username not found.")

                    else:
                        st.error(
                            f"GitHub API error: {response.status_code}"
                        )

                except requests.exceptions.Timeout:
                    st.error("GitHub request timed out. Please try again.")

                except requests.exceptions.RequestException as error:
                    st.error(f"Connection error: {error}")

    
    elif page == "Placement Readiness":
        st.title("🎓 Placement Readiness Dashboard")
        st.write("Track your preparation and assess your placement readiness.")

        # Get student profile
        connection = get_connection()
        profile = connection.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()
        connection.close()

        # Get course progress
        student_progress = get_student_progress(user["id"])
        total_courses = len(get_courses())

        completed_courses = sum(
            1 for course in student_progress
            if course["completed"] == 1
        )

        course_percentage = (
            int(completed_courses / total_courses * 100)
            if total_courses else 0
        )

        # Check profile completion
        profile_fields = [
            "phone", "college", "degree", "branch",
            "skills", "career_goal", "github_username"
        ]

        filled_fields = 0

        if profile:
            filled_fields = sum(
                1 for field in profile_fields
                if profile[field] and str(profile[field]).strip()
            )

        profile_percentage = int(
            filled_fields / len(profile_fields) * 100
        )

        # Check resume availability
        resume_percentage = 100 if profile and profile["skills"] else 0

        # Overall readiness score
        readiness_score = int(
            (profile_percentage * 0.3)
            + (course_percentage * 0.4)
            + (resume_percentage * 0.3)
        )

        st.subheader("📊 Your Placement Readiness")

        st.metric("Overall Readiness Score", f"{readiness_score}%")
        st.progress(readiness_score / 100)

        col1, col2, col3 = st.columns(3)

        col1.metric("Profile Completion", f"{profile_percentage}%")
        col2.metric("Course Completion", f"{course_percentage}%")
        col3.metric("Resume Preparation", f"{resume_percentage}%")

        st.subheader("📚 Learning Progress")

        st.write(
            f"Completed Courses: {completed_courses} / {total_courses}"
        )

        st.write(
            f"Remaining Courses: {max(total_courses - completed_courses, 0)}"
        )

        st.subheader("🚀 Recommendations")

        if profile_percentage < 100:
            st.info("Complete your My Profile section.")

        if course_percentage < 100:
            st.info("Complete more courses and quizzes in Course Hub.")

        if resume_percentage == 0:
            st.info("Add your technical skills in My Profile before preparing your resume.")

        if readiness_score >= 80:
            st.success("You are making strong progress towards placement readiness!")
        elif readiness_score >= 50:
            st.info("You are progressing well. Keep improving your preparation.")
        else:
            st.warning("Focus on completing your profile and learning activities.")
