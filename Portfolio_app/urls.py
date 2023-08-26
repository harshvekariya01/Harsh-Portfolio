from .views import *
from django.urls import path
from . import views

app_name = "Portfolio_app"

urlpatterns = [ 
    path('',home_view.as_view(), name="home_view"),
]

