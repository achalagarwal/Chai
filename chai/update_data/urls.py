from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('addSku', csrf_exempt(views.add_sku), name='Add SKU to Global Match Book'),
    path('pickle', csrf_exempt(views.pickle_and_backup), name='Pickles current Sku Matchbook and backups previous'),
]
