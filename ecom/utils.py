from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files.base import ContentFile

def generate_invoice_pdf(order, save_to_model=True):
    """
    Generates a PDF invoice for the given order.
    Optionally saves the PDF to order.invoice_pdf if save_to_model=True.
    Returns the PDF bytes or None if generation fails.
    """
    try:
        template = get_template('ecom/invoice.html')
        html = template.render({'order': order})
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)

        if pisa_status.err:
            return None

        pdf_bytes = pdf_file.getvalue()

        if save_to_model:
            filename = f"invoice_order_{order.id}.pdf"
            order.invoice_pdf.save(filename, ContentFile(pdf_bytes), save=False)
            order.save(update_fields=['invoice_pdf'])

        return pdf_bytes

    except Exception as e:
        # Optional: log error or raise
        return None