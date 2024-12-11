"""Testing for score function"""

from audio_case_grade import Case, Transcriber, Transcript, get_score


def test_score():
    """Test score function"""

    transcript = Transcript(
        type=Transcriber.DEEPGRAM, raw="hello world", clean="hello world"
    )
    case = Case(
        code="I42.1",
        system="Cardiopulm",
        name="concentric left ventricular hypertrophy",
    )
    expected_lexical_density = 0.0

    actual_score = get_score(transcript, case)

    assert actual_score.lexical_density == expected_lexical_density
