import pytest
import speech_api as api

@pytest.mark.parametrize('filename, output',
                         [('client_audio.wav', 'your paris sufficient i said')])
def test_prediction(filename, output):
    text = api.speech_to_text_task(filename)
    assert text == output
