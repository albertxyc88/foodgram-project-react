import os

from django.conf import settings
from django.http import FileResponse
from fpdf import FPDF

font = os.path.join(
    settings.BASE_DIR,
    'arial.ttf',
)


def generate_pdf(cart):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", font, uni=True)
    pdf.set_font("Arial", size=14)
    line = 1
    for ingredient in cart:
        pdf.cell(10, 10, txt=ingredient, ln=line, align='L')
        line += 1
    pdf.output('report.pdf', 'F')
    return FileResponse(
        open('report.pdf', 'rb'),
        as_attachment=True,
        content_type='application/pdf'
    )
