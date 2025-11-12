from django.shortcuts import render
from django.http import HttpResponse
from .models import Partner, PartnerType

def partner_list(request):
    partners = Partner.objects.select_related(
        'partner_type',
        'legal_address__region',
        'legal_address__city',
        'legal_address__street'
    ).all()
    context = {'partners': partners,}
    return render(request, 'partner.html', context)

def add_partner(request):
    if request.method == 'POST':
        return HttpResponse("")
    partner_types = PartnerType.objects.all()
    context = {'partner_types': partner_types, }
    return render(request, 'add_partner.html', context)