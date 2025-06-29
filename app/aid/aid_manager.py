from .first_aid_guide import FirstAidGuide
from .aid_scanner import scan_aid_image, Gemma3nModel
from .hazard_analyzer import analyze_image_for_hazards
from .gemma_assistant import Gemma3nOffline

gemma = Gemma3nOffline()

def handle_aid_request(query: str) -> dict:
    guide = FirstAidGuide().get_guide(query)
    ai_response = gemma.generate_response(f"How to: {query}")
    return {
        "title": guide.get("title", query.title()),
        "steps": guide.get("steps", []),
        "ai_explanation": ai_response
    }