from django.urls import path
from .views import analyze_view

urlpatterns = [
    path("analyze/", analyze_view),
]
