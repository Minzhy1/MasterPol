from django.db import models

class Region(models.Model):
    name = models.CharField(verbose_name = "Область/Регион", max_length=100, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(verbose_name = "Город", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(verbose_name = "Улица", max_length=100, unique=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    index = models.CharField(verbose_name="Индекс")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")
    street = models.ForeignKey(Street, on_delete=models.CASCADE, verbose_name="Улица")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    dom = models.CharField(verbose_name = "Дом")

    def __str__(self):
        return f"{self.region}, {self.street}, {self.city}"


class PartnerType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Тип партнера")

class Partner(models.Model):
    partner_type = models.ForeignKey(PartnerType, on_delete=models.CASCADE, verbose_name="Тип партнёра")
    name = models.CharField(verbose_name = "Наименование партнёра", max_length=200)
    director = models.CharField(verbose_name = "Директор", max_length=200)
    email = models.EmailField(verbose_name = "Электронная почта")
    phone = models.CharField(verbose_name = "Телефон", max_length=20)
    legal_address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Юридический адрес")
    inn = models.CharField(verbose_name = "ИНН", max_length=12, unique=True)
    rating = models.PositiveSmallIntegerField(verbose_name = "Рейтинг", default=0)

    def __str__(self):
        return self.name



    def __str__(self):
        return self.name

# Модель для Типа продукции
class ProductType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Тип продукции")
    coefficient = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Коэффициент типа продукции")

    def __str__(self):
        return self.name

# Модель для Продукции
class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name="Тип продукции", related_name='products')
    name = models.CharField(max_length=255, verbose_name="Наименование продукции")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    min_partner_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Минимальная стоимость для партнера")

    def __str__(self):
        return self.name

# Модель для Типа материала
class MaterialType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Тип материала")
    defect_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент брака материала (%)")

    def __str__(self):
        return self.name

# Модель для Продажи партнера (Продукция партнера)
class PartnerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукция", related_name='partner_sales')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Наименование партнера", related_name='sales')
    quantity = models.PositiveIntegerField(verbose_name="Количество продукции")
    sale_date = models.DateField(verbose_name="Дата продажи")

    def __str__(self):
        return f"{self.partner.name} - {self.product.name} ({self.quantity} шт. - {self.sale_date})"





