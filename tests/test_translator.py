import pytest
from app.comms.translator import Translator

class DummyTranslator(Translator):
    def __init__(self):
        super().__init__()

    def translate(self, text, src='en', dst='es'):
        # bypass actual offline model
        return f"[{src}->{dst}]{text}"

@pytest.fixture
def translator():
    return DummyTranslator()

def test_translate_simple_phrase(translator):
    input_text = "hello world"
    output = translator.translate(input_text, src="en", dst="fr")
    assert output.startswith("[en->fr]")
    assert "hello world" in output
