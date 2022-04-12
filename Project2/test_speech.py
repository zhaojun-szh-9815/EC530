import pytest
import speech_api as api

@pytest.mark.parametrize('output',
                         [('your paris sufficient i said')])
def test_prediction(output):
    text = api.speech_to_text_task('client_audio.wav')
    assert text == output
