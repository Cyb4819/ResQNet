import pytest
from app.sensors.image_analyzer import analyze_image

@pytest.fixture
def sample_image(monkeypatch, tmp_path):
    # Create a dummy image file (blank)
    img_path = tmp_path / "dummy.jpg"
    img_path.write_bytes(b"\xff\xd8\xff\xdb")  # minimal JPEG header
    return str(img_path)

def test_analyze_image_detects_hazard(sample_image, monkeypatch):
    # Mock the Gemma3n or image model behavior
    monkeypatch.setattr('app.sensors.image_analyzer.load_model', lambda: None)
    monkeypatch.setattr('app.sensors.image_analyzer.predict', lambda model, img: {"hazard": True, "type": "smoke"})

    result = analyze_image(sample_image)
    assert isinstance(result, dict)
    assert result["hazard"] is True
    assert "type" in result
