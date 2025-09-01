from rest_framework.decorators import api_view
from rest_framework.response import Response
#from .decision import analyze_text

@api_view(["POST"])
def analyze_view(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error":"text is required"}, status=400)
    res = analyze_text(text)
    return Response(res)
