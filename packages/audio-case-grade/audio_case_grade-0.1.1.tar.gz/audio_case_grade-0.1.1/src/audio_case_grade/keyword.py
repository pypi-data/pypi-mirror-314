"""Keyword algorithm module"""

import re
from typing import Optional, Tuple

from pandas import Series

from .keybank import get_keybank
from .types import (
    Assessments,
    Case,
    Foundations,
    Histories,
    Metrics,
    Objectives,
    Plans,
    Soap,
)


def count_words(keyword_list: list[str]) -> int:
    """Get the word count of a list of keywords"""

    keyword_string = " ".join(keyword_list)  # Keywords can contain multiple words
    return len(keyword_string.split(" "))


def count_keywords(text: str, keybank: Series) -> Optional[Metrics]:
    """Get the keyword count and other metrics for a piece of text"""

    if keybank.empty:
        return None

    # Replace empty strings with None and drop them
    cleaned_keybank = keybank.explode().replace("", None).dropna()

    if cleaned_keybank.empty:
        return None

    keyword_sequence: dict[str, int] = {}
    keywords_used: list[str] = []

    expected = len(cleaned_keybank)

    count = 0
    not_found = -1

    for keyword in cleaned_keybank:
        if keyword in text:
            keywords_used.append(keyword)
            count += 1
            match = re.search(keyword, text)
            keyword_sequence[keyword] = match.start() + 1 if match else not_found
        else:
            keyword_sequence[keyword] = not_found

    word_count = count_words(keywords_used)

    return Metrics(
        count=count,
        expected=expected,
        sequence=keyword_sequence,
        used=keywords_used,
        word_count=word_count,
    )


def _histories(text: str, keybank: Series) -> Histories:
    """Get the history metrics for a transcript"""

    cc = count_keywords(text, keybank.iloc[0])
    hpi = count_keywords(text, keybank.iloc[1])
    ros = count_keywords(text, keybank.iloc[2])
    meds = count_keywords(text, keybank.iloc[3])

    return Histories(cc=cc, hpi=hpi, ros=ros, meds=meds)


def _objectives(text: str, keybank: Series) -> Objectives:
    """Get the objectives metrics for a transcript"""

    vitals = count_keywords(text, keybank.iloc[0])
    gen = count_keywords(text, keybank.iloc[1])
    dl = count_keywords(text, keybank.iloc[2])
    di = count_keywords(text, keybank.iloc[3])

    return Objectives(vitals=vitals, gen=gen, dl=dl, di=di)


def _plans(text: str, keybank: Series) -> Plans:
    """Get the plan metrics for a transcript"""

    tx = count_keywords(text, keybank.iloc[0])
    consults = count_keywords(text, keybank.iloc[1])
    interventions = count_keywords(text, keybank.iloc[2])

    return Plans(tx=tx, consults=consults, interventions=interventions)


def _assessments(text: str, keybank: Series) -> Assessments:
    """Get the assessment metrics for a transcript"""

    dx = count_keywords(text, keybank.iloc[0])
    ddx = count_keywords(text, keybank.iloc[1])

    return Assessments(dx=dx, ddx=ddx)


def _foundations(text: str, keybank: Series) -> Foundations:
    """Get the assessment metrics for a transcript"""

    root = count_keywords(text, keybank.iloc[0])

    return Foundations(root=root)


def _soap(
    text: str, correct_keybank: Series, wrong_keybank: Series
) -> Tuple[Soap, Soap]:
    """calculate all metrics of the SOAP note flow and return the data frames for each section"""

    correct = Soap(
        histories=_histories(text, correct_keybank),
        objectives=_objectives(text, correct_keybank),
        assessments=_assessments(text, correct_keybank),
        plans=_plans(text, correct_keybank),
        foundations=_foundations(text, correct_keybank),
    )

    wrong = Soap(
        histories=_histories(text, wrong_keybank),
        objectives=_objectives(text, wrong_keybank),
        assessments=_assessments(text, wrong_keybank),
        plans=_plans(text, wrong_keybank),
        foundations=_foundations(text, wrong_keybank),
    )

    return correct, wrong


def get_keywords(text: str, case: Case) -> tuple[Soap, Soap]:
    """main function for keyword algorithm, applies above functions to all student transcripts"""

    (correct_keybank, wrong_keybank) = get_keybank(case)
    (correct_soap, wrong_soap) = _soap(
        text,
        correct_keybank,
        wrong_keybank,
    )

    return correct_soap, wrong_soap
