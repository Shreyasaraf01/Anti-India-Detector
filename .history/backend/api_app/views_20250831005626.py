# api_app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.api.decision import predict_fake  # import the updated function

@api_view(["POST"])
def analyze_view(request):
    """
    POST endpoint to analyze text for fake content.
    Expects JSON: { "text": "some text here" }
    Returns JSON: { "label": 0/1/... } or { "error": "..." }
    """
    # Get text from request
    text = request.data.get("text", "").strip()
    
    if not text:
        return Response({"error": "text is required"}, status=400)
    
    # Predict using the fixed model
    result = predict_fake(text)
    
    # Return prediction
    return Response(result)
