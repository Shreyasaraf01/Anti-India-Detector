# api_app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.api.decision import predict_fake  # import the updated function
import sys
import os

# Add 'api' folder to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.join(BASE_DIR, "api")
if API_DIR not in sys.path:
    sys.path.append(API_DIR)

from decision import predict_fake

@api_view(["POST"])
def analyze_view(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "text is required"}, status=400)
    res = predict_fake(text)
    return Response(res)
