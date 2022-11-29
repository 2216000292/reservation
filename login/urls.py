"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from  Restaurant.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', reservation,name='home'),
    path('register/', register,name='register'),
    path('login/', login,name='login'),
    path('logout/', logout,name='logout'),

    path('update-table/',create_free_tables,name='cft'),
    path('generate_preferred/',generate_preferred,name='generate_preferred'),
    path('search_dinner/',search_dinner,name='search_dinner'),
    path('getIntroduce/',getIntroduce,name='getIntroduce'),
    path('reservation-form/',resevation_order,name='rform'),
    path('reservation/',reservation,name='reservation'),
    path('change/',change,name='change'),

]
