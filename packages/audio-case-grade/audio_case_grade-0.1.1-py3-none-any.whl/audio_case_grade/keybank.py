"""Handle the KeyBank data"""

import importlib.resources as pkg_resources
from typing import Optional, Tuple

import jiwer  # type: ignore
import pandas as pd
from pandas import DataFrame, Series

from .types import Case

SEPERATOR = ", "
CODE_COLUMN = "ICD10"
SYSTEM_COLUMN = "System"
COLUMNS_TO_DROP = ["Case", "ICD10", "System"]


def _clean_keybank(keybank: DataFrame):
    """Cleans the KeyBank"""

    for _i in range(3, len(keybank.columns)):
        k = 0
        for _j in keybank.iloc[:, _i]:
            if _j != "":

                t = jiwer.SubstituteWords({",": SEPERATOR})(_j)
                t = jiwer.Strip()(t)
                t = jiwer.RemoveMultipleSpaces()(t)
                keybank.loc[k, keybank.columns[_i]] = t
                k = k + 1
            else:
                keybank.loc[k, keybank.columns[_i]] = _j
                k = k + 1


def _correct_keybank(full_keybank: DataFrame, case: Case) -> Series:
    """Get the correct keyword bank"""

    # Get keys for the case
    correct_keys = full_keybank[full_keybank[CODE_COLUMN] == case.code].drop(
        COLUMNS_TO_DROP, axis=1
    )

    # Split the keys
    correct_keybank = pd.Series(
        [correct_keys[col].str.split(SEPERATOR) for col in correct_keys.columns]
    )

    return correct_keybank


def _wrong_keybank(
    full_keybank: DataFrame, case: Case, correct_keybank: Series
) -> Series:

    # Get the keywords for the system
    keywords_for_system = full_keybank[full_keybank[SYSTEM_COLUMN] == case.system].drop(
        COLUMNS_TO_DROP, axis=1
    )

    # Concatenate the keywords
    keywords_with_dupes = pd.Series(
        [
            keywords_for_system[col].str.cat(sep=SEPERATOR)
            for col in keywords_for_system.columns
        ]
    )

    # Remove duplicates
    keyword_bank = pd.Series(
        [
            list(dict.fromkeys(string_list.split(SEPERATOR)))
            for string_list in keywords_with_dupes
        ],
        index=keywords_for_system.columns,
    )

    # Get the wrong keywords
    wrong_key_list: list[list[str]] = []
    for i in range(len(keywords_for_system.columns)):
        a = keyword_bank.iloc[i]
        b = list(correct_keybank.iloc[i].item())
        key = list(set(a) ^ set(b))
        wrong_key_list.append(key)

    wrong_keybank = pd.Series(wrong_key_list, index=keywords_for_system.columns)
    return wrong_keybank


def get_keybank_csv() -> DataFrame:
    """Get the KeyBank from the csv file"""

    resources = "audio_case_grade.resources"
    keybank_file = "keybank.csv"

    with pkg_resources.open_text(resources, keybank_file) as csv_file:
        return pd.read_csv(
            csv_file,
            na_filter=False,
        )


def get_keybank(
    case: Case, keybank_override: Optional[DataFrame] = None
) -> Tuple[Series, Series]:
    """Get the KeyBank"""

    keybank = get_keybank_csv() if keybank_override is None else keybank_override

    _clean_keybank(keybank)

    correct_keybank = _correct_keybank(keybank, case)
    wrong_keybank = _wrong_keybank(keybank, case, correct_keybank)

    return correct_keybank, wrong_keybank
