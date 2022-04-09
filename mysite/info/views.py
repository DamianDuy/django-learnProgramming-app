from django.shortcuts import render

from .models import GDPR, About, Terms_And_Conditions

# Create your views here.
def gdpr_view(request):
    gdpr = GDPR.objects.all()
    content = ""
    if gdpr:
        content = gdpr[0].content

    return render(
        request, 
        'common/common.html', 
        {
            'title': 'GDPR',
            'message': content,
        }
    )

def terms_and_conditions_view(request):
    terms_and_conditions = Terms_And_Conditions.objects.all()
    content = ""
    if terms_and_conditions:
        content = terms_and_conditions[0].content

    return render(
        request, 
        'common/common.html', 
        {
            'title': 'Terms and Conditions',
            'message': content,
        }
    )

def about_view(request):
    about = About.objects.all()
    content = ""
    if about:
        content = about[0].content

    return render(
        request, 
        'common/common.html', 
        {
            'title': 'About',
            'message': content,
        }
    )
