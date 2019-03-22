from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    path('autocomplete', csrf_exempt(views.complete_query), name='autocomplete search query'),
    path('data', csrf_exempt(views.get_sku_data), name='get all information related to sku'),
]
