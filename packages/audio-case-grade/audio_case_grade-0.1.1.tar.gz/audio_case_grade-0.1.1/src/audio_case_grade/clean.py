"""Module for textual Cleaning/Standardization"""

import importlib.resources as pkg_resources
import string
from typing import Mapping

import jiwer  # type: ignore
import nltk  # type: ignore
import pandas as pd
from nltk.corpus import stopwords  # type: ignore
from pandas import DataFrame

from .types import Transcriber, Transcript

ABBREVIATION_COLUMN = "Abbreviation"
MEANING_COLUMN = "Meaning"
STOP_WORDS_LANGUAGE = "english"
ACCEPTABLE_STOP_WORDS = ["no", "not", "most", "some", "out", "s", "t"]
COMMON_SUBSTITUTIONS: Mapping[str, str] = {
    "1+": "one plus",
    "1 +": "one plus",
    "2 d": "2d",
    "o two": "oxygen saturation",
    "o2": "oxygen saturation",
    "mg": "milligrams",
    "x-ray": "xray",
    "x ray": "xray",
    "cr td": "crtd",
    "rails": "rales",
    "rail": "rale",
}


def get_abbreviations_csv() -> DataFrame:
    """Get the medical abbreviations & acronyms from the csv file"""

    resources = "audio_case_grade.resources"
    abbreviations_file = "abbreviations.csv"

    with pkg_resources.open_text(resources, abbreviations_file) as csv_file:
        return pd.read_csv(csv_file, header=0)


def _get_abbreviation_map() -> Mapping[str, str]:
    """Convert medical abbreviation & acronyms to map"""

    acr_abb = get_abbreviations_csv()
    abbrev_map = dict(
        zip(
            acr_abb[ABBREVIATION_COLUMN].str.lower(),
            acr_abb[MEANING_COLUMN].str.lower(),
        )
    )
    abbrev_map.pop("s", None)
    return abbrev_map


def _text_clean(text: str, abbrev_map: Mapping[str, str]) -> str:
    """textual cleaning and standardization"""

    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    t = jiwer.ExpandCommonEnglishContractions()(text)
    t = jiwer.RemoveKaldiNonWords()(t)
    t = t.translate(translator)
    t = jiwer.Strip()(t)
    t = jiwer.SubstituteWords(abbrev_map)(t)
    t = jiwer.SubstituteWords(COMMON_SUBSTITUTIONS)(t)
    clean_text = jiwer.RemoveMultipleSpaces()(t)
    return clean_text


def _load_stop_words() -> list[str]:
    """Load Stop Words"""

    nltk.download("stopwords", quiet=True)
    stop = stopwords.words(STOP_WORDS_LANGUAGE)
    for word in ACCEPTABLE_STOP_WORDS:
        stop.remove(word)
    return stop


def _internal_clean(raw_transcript: str) -> str:
    """Removes stop words from presentations, applies above cleaning functions"""

    stop = _load_stop_words()
    abbrev_map = _get_abbreviation_map()
    cleaned_text = _text_clean(raw_transcript, abbrev_map)
    clean_list = cleaned_text.split()
    clean_response = [word for word in clean_list if word not in stop]
    return " ".join(clean_response)


def clean(transcript: Transcript) -> Transcript:
    """Clean up the transcript"""

    if transcript.type == Transcriber.DEEPGRAM:
        transcript.clean = _internal_clean(transcript.raw)
        return transcript

    if transcript.type == Transcriber.WHISPER:
        transcript.clean = _internal_clean(transcript.raw)
        return transcript

    return transcript
