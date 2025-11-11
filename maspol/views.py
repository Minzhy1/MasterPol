from django.shortcuts import render
from .models import Partner

def partner_list(request):
    partners = Partner.objects.select_related(
        'partner_type',
        'legal_address__region',
        'legal_address__city',
        'legal_address__street'
    ).all()

    context = {
        'partners': partners,
    }
    return render(request, 'partner.html', context)