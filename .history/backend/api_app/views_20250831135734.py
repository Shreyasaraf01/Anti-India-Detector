# api_app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
import re
import sys
import os

# -------------------------
# Add 'api' folder to Python path
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend folder
API_DIR = os.path.join(BASE_DIR, "api")  # path to your 'api' folder
if API_DIR not in sys.path:
    sys.path.append(API_DIR)

# Import from the api folder
from decision import predict_fake  # <- use this, not backend.api.decision

@api_view(["GET"])
def stats_view(request):
    # Dummy data; replace with DB queries
    flagged = 12
    normal = 88
    return Response({
        "flagged": flagged,
        "normal": normal,
        "pie": [flagged, normal]
    })

@api_view(["GET"])
def wordcloud_view(request):
    # Dummy: replace with actual negative terms extraction
    texts = ["bad", "hate", "problem", "fake", "corrupt", "attack"]
    freq = Counter(texts)
    return Response({"words": freq})

# -------------------------
# API endpoint
# -------------------------
@api_view(["POST"])
def analyze_view(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "text is required"}, status=400)
    
    result = predict_fake(text)
    return Response(result)
