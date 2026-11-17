
from pathlib import Path
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parent.parent
CERTIFICATE_DIR = BASE_DIR / "generated_certificates"


def generate_certificate(student_name, course_name, filename=None):
    """Generate a PDF course completion certificate."""

    CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = "Certificate.pdf"

    # Keep the file inside the certificate folder
    safe_filename = Path(filename).name
    if not safe_filename.lower().endswith(".pdf"):
        safe_filename += ".pdf"

    file_path = CERTIFICATE_DIR / safe_filename

    width, height = landscape(A4)
    pdf = canvas.Canvas(str(file_path), pagesize=(width, height))

    # Background
    pdf.setFillColor(colors.HexColor("#F5F0E5"))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Outer border
    pdf.setStrokeColor(colors.HexColor("#183D32"))
    pdf.setLineWidth(5)
    pdf.rect(25, 25, width - 50, height - 50, fill=0)

    # Inner border
    pdf.setStrokeColor(colors.HexColor("#C6A968"))
    pdf.setLineWidth(2)
    pdf.rect(38, 38, width - 76, height - 76, fill=0)

    # Brand name
    pdf.setFillColor(colors.HexColor("#183D32"))
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawCentredString(
        width / 2, height - 100, "CareerSpring"
    )

    pdf.setFillColor(colors.HexColor("#C6A968"))
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(
        width / 2, height - 125, "LEARN. PREPARE. ACHIEVE."
    )

    # Certificate heading
    pdf.setFillColor(colors.HexColor("#183D32"))
    pdf.setFont("Helvetica-Bold", 32)
    pdf.drawCentredString(
        width / 2, height - 200, "CERTIFICATE OF COMPLETION"
    )

    # Description
    pdf.setFillColor(colors.HexColor("#444444"))
    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        width / 2, height - 250,
        "This certificate is proudly presented to"
    )

    # Student name
    pdf.setFillColor(colors.HexColor("#183D32"))
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2, height - 300, str(student_name)[:60]
    )

    # Course name
    pdf.setFillColor(colors.HexColor("#444444"))
    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        width / 2, height - 345,
        "for successfully completing the course"
    )

    pdf.setFillColor(colors.HexColor("#183D32"))
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        width / 2, height - 380, str(course_name)[:70]
    )

    # Date
    from datetime import date

    pdf.setFillColor(colors.HexColor("#555555"))
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2, 105,
        "Issued on: " + date.today().strftime("%d %B %Y")
    )

    # Footer
    pdf.setFillColor(colors.HexColor("#183D32"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(
        width / 2, 75, "CareerSpring | Student Career Development Platform"
    )

    pdf.save()

    return file_path
