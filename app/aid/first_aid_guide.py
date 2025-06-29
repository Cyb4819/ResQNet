import json
from pathlib import Path

class FirstAidGuide:
    def __init__(self, json_path: str = "data/first_aid_guide.json"):
        self.data_path = Path(json_path)
        self.guides = self._load_guides()

    def _load_guides(self) -> dict:
        if not self.data_path.exists():
            return {}
        try:
            with self.data_path.open("r", encoding="utf-8") as f:
                return {k.lower(): v for k, v in json.load(f).items()}
        except json.JSONDecodeError:
            return {}

    def get_guide(self, topic: str) -> dict:
        return self.guides.get(topic.lower(), {
            "title": "Not Found",
            "steps": ["No first aid data available for this topic."]
        })