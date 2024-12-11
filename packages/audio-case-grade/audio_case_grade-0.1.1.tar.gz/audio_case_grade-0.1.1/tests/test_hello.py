"""Testing for hello function"""

from audio_case_grade import hello


def test_hello():
    """Test hello function"""

    result = hello()
    assert result == "Welcome to audio-case-grade!"
