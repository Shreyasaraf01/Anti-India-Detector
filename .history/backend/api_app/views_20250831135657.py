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
