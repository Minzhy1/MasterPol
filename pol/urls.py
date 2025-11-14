"""
URL configuration for pol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from maspol.views import partner_list, add_partner, partner_history, calculate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', partner_list, name='partner_list'),
    path('add/', add_partner, name='add_partner'),
    path('edit/<int:partner_id>/', add_partner, name='edit_partner'),
    path('history/<int:partner_id>/', partner_history, name='partner_history'),
    path('calc/', calculate, name='calculate'),
]
