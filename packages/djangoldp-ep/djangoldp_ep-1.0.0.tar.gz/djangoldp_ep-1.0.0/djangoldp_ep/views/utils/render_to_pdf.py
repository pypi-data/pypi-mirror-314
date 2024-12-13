from io import BytesIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template


# What about a html version of the view generation from a template ?
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result, encoding="utf-8")
    if not pdf.err:
        return HttpResponse(
            result.getvalue(), content_type="application/pdf; charset=utf-8"
        )
    return None
