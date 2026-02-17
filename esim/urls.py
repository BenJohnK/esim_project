# your_app_name/urls.py
from django.urls import path
from . import views  # Import your views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    # Map the activate_esim view to a URL path
    path('v1/esim/activate/', views.activate_esim, name='activate_esim'),
]
