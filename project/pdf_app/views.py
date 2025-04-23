from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .forms import PDFForm
from xhtml2pdf import pisa

def generate_pdf_view(request):
    if request.method == 'POST':
        form = PDFForm(request.POST)
        if form.is_valid():
            template = get_template('pdf_template.html')
            context = form.cleaned_data
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="user_input.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse("Something went wrong.")
            return response
    else:
        form = PDFForm()
    return render(request, 'form.html', {'form': form})
