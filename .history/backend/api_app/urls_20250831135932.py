from django.urls import path
from .views import analyze_view, stats_view, wordcloud_view

urlpatterns = [
    path("analyze/", analyze_view),
    path("stats/", stats_view),
    path("wordcloud/", wordcloud_view),
]
