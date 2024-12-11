"""Core module for grading medical audio cases"""

from .keyword import get_keywords
from .types import Case, Score, Transcript


def hello() -> str:
    """Welcome message for the package"""

    return "Welcome to audio-case-grade!"


def get_score(transcript: Transcript, case: Case) -> Score:
    """Score an audio case transcript"""

    correct_soap, wrong_soap = get_keywords(transcript.clean, case)

    lexical_density = (
        round((correct_soap.totals.word_count / transcript.word_count), 4) * 100
    )

    return Score(
        lexical_density=lexical_density,
        correct=correct_soap,
        wrong=wrong_soap,
    )
