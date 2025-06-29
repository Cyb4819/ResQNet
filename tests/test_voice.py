import pytest
from app.voice.voice_assistant import VoiceAssistant

class DummyAssistant(VoiceAssistant):
    def __init__(self):
        super().__init__()
        self.logs = []

    def recognize_speech(self):
        return "help me!"

    def speak(self, message):
        self.logs.append(message)

@pytest.fixture
def assistant():
    return DummyAssistant()

def test_panic_trigger(assistant, monkeypatch):
    # Monkeypatch panic trigger invocation
    from app.comms.panic_trigger import PanicTrigger

    class DummyTrigger(PanicTrigger):
        def send_alert(self, location, message):
            self.sent = {"location": location, "message": message}

    dt = DummyTrigger()
    monkeypatch.setattr('app.comms.panic_trigger.PanicTrigger', lambda: dt)

    assistant.listen_and_respond()
    # confirm assistant triggered panic
    assert hasattr(dt, "sent")
    assert "help me" in dt.sent["message"].lower()
