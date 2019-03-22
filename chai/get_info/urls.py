from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('alcohol', csrf_exempt(views.check_alcohol_limit), name='check alcohol limit'),
    path('unmatched', csrf_exempt(views.get_top_unmatched), name='gets top unmatched user queried terms'),
]
