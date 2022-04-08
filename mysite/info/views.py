from django.shortcuts import render

from .models import GDPR, About, Terms_And_Conditions

# Create your views here.
def gdpr_view(request):
    gdpr = GDPR.objects.all()[0]

    return render(
        request, 
        'common/common.html', 
        {
            'title': 'GDPR',
            'message': gdpr.content,
        }
    )

def terms_and_conditions_view(request):
    terms_and_conditions = Terms_And_Conditions.objects.all()[0]

    return render(
        request, 
        'common/common.html', 
        {
            'title': 'Terms and Conditions',
            'message': terms_and_conditions.content,
        }
    )

def about_view(request):
    about = About.objects.all()[0]

    return render(
        request, 
        'common/common.html', 
        {
            'title': 'About',
            'message': about.content,
        }
    )
