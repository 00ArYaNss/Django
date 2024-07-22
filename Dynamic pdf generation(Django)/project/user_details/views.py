from django.shortcuts import render, redirect
from .forms import UserDetailsForm
from .models import UserDetails
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def user_details_view(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            user_details = form.save()
            return redirect('generate_pdf', pk=user_details.pk)
    else:
        form = UserDetailsForm()
    return render(request, 'user_details/user_details_form.html', {'form': form})

def generate_pdf(request, pk):
    user_details = UserDetails.objects.get(pk=pk)
    template_path = 'user_details/user_details_pdf.html'
    context = {'user_details': user_details}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user_details.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
