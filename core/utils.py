from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings
import os

def generate_pdf_pass(student_obj, month, year,selected_town=None):
    town_name = selected_town.name if selected_town else student_obj.town.name
    filename = f"{student_obj.user}_pass.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, filename)

    c = canvas.Canvas(pdf_path, pagesize=A4)

    # Add content
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Student Bus Pass")

    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Name: {student_obj.full_name}")
    c.drawString(100, 750, f"Username: {student_obj.user}")
    c.drawString(100, 730, f"Academic Year: {student_obj.academic_year}")
    c.drawString(100,710,f"Town:{town_name}")
    c.drawString(100, 690, f"Month: {month} {year}")
    c.drawString(100, 670, "Clerk Sign: _______________________")

    # Optionally: Add photo
    if student_obj.photo:
        c.drawImage(student_obj.photo.path, 400, 700, width=100, height=100)

    c.showPage()
    c.save()
    return pdf_path
