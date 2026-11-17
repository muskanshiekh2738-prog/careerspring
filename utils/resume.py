
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_DIR = BASE_DIR / "generated_resumes"


def generate_resume(data, filename="CareerSpring_Resume.docx"):
    """
    Generate a professional student resume.

    Expected data keys:
    name, email, phone, location, career_objective,
    education, skills, projects, certifications,
    experience, linkedin, github
    """

    RESUME_DIR.mkdir(parents=True, exist_ok=True)

    # Prevent directory traversal through the filename
    safe_filename = Path(filename).name
    if not safe_filename.lower().endswith(".docx"):
        safe_filename += ".docx"

    file_path = RESUME_DIR / safe_filename

    document = Document()

    # Page margins
    section = document.sections[0]
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # Default font
    styles = document.styles
    styles["Normal"].font.name = "Calibri"
    styles["Normal"].font.size = Pt(10)

    # Name heading
    name = document.add_heading(
        data.get("name", "Student Name"), level=0
    )
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for run in name.runs:
        run.font.color.rgb = RGBColor(24, 61, 50)
        run.font.size = Pt(24)

    # Contact details
    contact = document.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER

    contact_parts = [
        data.get("email", ""),
        data.get("phone", ""),
        data.get("location", "")
    ]

    contact.add_run(" | ".join(
        part for part in contact_parts if part
    ))

    # Links
    links = []
    if data.get("linkedin"):
        links.append("LinkedIn: " + data["linkedin"])
    if data.get("github"):
        links.append("GitHub: " + data["github"])

    if links:
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run(" | ".join(links))

    def add_section(title, content):
        """Add a resume section when content is available."""

        if not content:
            return

        document.add_heading(title, level=1)

        if isinstance(content, list):
            for item in content:
                paragraph = document.add_paragraph(style="List Bullet")
                paragraph.add_run(str(item))
        else:
            document.add_paragraph(str(content))

    # Resume sections
    add_section(
        "CAREER OBJECTIVE",
        data.get("career_objective")
    )

    add_section(
        "EDUCATION",
        data.get("education", [])
    )

    add_section(
        "TECHNICAL SKILLS",
        data.get("skills", [])
    )

    add_section(
        "PROJECTS",
        data.get("projects", [])
    )

    add_section(
        "INTERNSHIP / EXPERIENCE",
        data.get("experience", [])
    )

    add_section(
        "CERTIFICATIONS",
        data.get("certifications", [])
    )

    document.save(file_path)

    return file_path
