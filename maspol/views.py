from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partner, PartnerType, Address, Region, City, Street, PartnerProduct, MaterialType, ProductType

def calculate_discount(partner):
    total_qty = PartnerProduct.objects.filter(partner=partner).aggregate(
        total=Sum('quantity')
    )['total'] or 0
    total_qty = int(total_qty)
    if total_qty < 10_000:
        return 0
    elif total_qty < 50_000:
        return 5
    elif total_qty < 300_000:
        return 10
    else:
        return 15


def partner_list(request):
    partners = Partner.objects.select_related(
        'partner_type',
        'legal_address__region',
        'legal_address__city',
        'legal_address__street'
    ).all()
    for partner in partners:
        partner.discount = calculate_discount(partner)

    return render(request, 'partner.html', {'partners': partners})


def partner_history(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    # Получаем все продажи партнёра
    sales = PartnerProduct.objects.filter(partner=partner).select_related('product')

    context = {
        'partner': partner,
        'sales': sales,
    }
    return render(request, 'history.html', context)


def add_partner(request, partner_id=None):
    partner = None
    if partner_id:
        partner = get_object_or_404(Partner, id=partner_id)

    if request.method == 'POST':
        # Получаем данные
        name = request.POST.get('name')
        partner_type_id = request.POST.get('partner_type')
        rating = request.POST.get('rating')
        index = request.POST.get('index')
        region_id = request.POST.get('region')
        city_id = request.POST.get('city')
        street_id = request.POST.get('street')
        dom = request.POST.get('dom')
        director = request.POST.get('director')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Получаем связанные объекты
        partner_type = PartnerType.objects.get(id=partner_type_id)
        region = Region.objects.get(id=region_id)
        city = City.objects.get(id=city_id)
        street = Street.objects.get(id=street_id)

        if partner and partner.legal_address:
            # Редактирование
            address = partner.legal_address
            address.index = index
            address.region = region
            address.city = city
            address.street = street
            address.dom = dom
            address.save()

            partner.name = name
            partner.partner_type = partner_type
            partner.rating = rating
            partner.director = director
            partner.phone = phone
            partner.email = email
            partner.save()
        else:
            # Добавление
            address = Address.objects.create(
                index=index,
                region=region,
                city=city,
                street=street,
                dom=dom
            )
            Partner.objects.create(
                name=name,
                partner_type=partner_type,
                rating=rating,
                director=director,
                phone=phone,
                email=email,
                legal_address=address,
                inn="0000000000"
            )

        return redirect('partner_list')

    # Данные для формы
    context = {
        'partner_types': PartnerType.objects.all(),
        'regions': Region.objects.all(),
        'cities': City.objects.all(),
        'streets': Street.objects.all(),
        'partner': partner,
    }
    return render(request, 'add_partner.html', context)

def calculate(request):
    result = None
    error = None

    if request.method == 'POST':
        try:
            product_type_id = int(request.POST.get('product_type_id'))
            material_type_id = int(request.POST.get('material_type_id'))
            product_count = int(request.POST.get('product_count'))
            param1 = float(request.POST.get('param1'))
            param2 = float(request.POST.get('param2'))

            if param1 <= 0 or param2 <= 0 or product_count <= 0:
                result = -1
            else:
                # Получаем тип продукции
                try:
                    product_type = ProductType.objects.get(id=product_type_id)
                except ProductType.DoesNotExist:
                    result = -1
                else:
                    # Получаем тип материала
                    try:
                        material_type = MaterialType.objects.get(id=material_type_id)
                    except MaterialType.DoesNotExist:
                        result = -1
                    else:
                        # Расчёт
                        material = param1 * param2 * float(product_type.coefficient)
                        total_material = material * product_count
                        # Учёт брака
                        defect = 1 + float(material_type.defect_percentage)
                        total_defect = total_material * defect
                        result = int(total_defect)

        except (ValueError, TypeError):
            result = -1

    return render(request, 'method.html', {'result': result})