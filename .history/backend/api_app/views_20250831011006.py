# api_app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.api.decision import predict_fake  # directly import from api folder

# -------------------------
# API endpoint
# -------------------------
@api_view(["POST"])
def analyze_view(request):
    """
    POST /api/analyze/
    Body: {"text": "your text here"}
    Response: {"label": "fake", "probability": 0.87}
    """
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "text is required"}, status=400)

    # Get prediction from decision.py
    result = predict_fake(text)
    return Response(result)
