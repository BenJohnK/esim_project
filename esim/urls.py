# your_app_name/urls.py
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Map the activate_esim view to a URL path
    path('v1/esim/activate/', views.activate_esim, name='activate_esim'),
]