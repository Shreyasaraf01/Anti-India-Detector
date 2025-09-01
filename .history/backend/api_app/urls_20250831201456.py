from django.urls import path
from .views import analyze_view, stats_view, wordcloud_view

urlpatterns = [
    path("analyze/", analyze_view),
]
