from typing import List
from importlib import resources
import logging

logger = logging.getLogger(__name__)

DATA_PATH = resources.files(f"rara_text_evaluator.data")
SUPPORTED_BUILD_LANGUAGES_FILE_PATH = DATA_PATH / "supported_build_languages.txt"

def load_languages(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        languages = [
            lang.strip()
            for lang in f.read().split("\n")
        ]
    return languages

def get_supported_build_languages(file_path: str = SUPPORTED_BUILD_LANGUAGES_FILE_PATH) -> List[str]:
    try:
        # Try loading supported languages straight from langdetect
        from langdetect.detector_factory import DetectorFactory, PROFILES_DIRECTORY

        factory = DetectorFactory()
        factory.load_profile(PROFILES_DIRECTORY)

        supported_build_languages = factory.langlist

    except Exception as e:
        # Use hardcoded version in case something has changed in langdetect
        # and some functions are no longer working as expected
        log_message = (
            f"Detecting supported build languages with `langdetect` failed with exception: '{e}'. "
            "Trying to load languages from file instead (the list might not be up to date)."
        )
        logger.debug(log_message)
        supported_build_languages = load_languages(file_path)

    logger.debug(f"Finished loading {len(supported_build_languages)} supported build languages.")
    return supported_build_languages
