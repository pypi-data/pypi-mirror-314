import math
import pickle
import warnings
import logging
import os

from collections import defaultdict
from pathlib import Path
from typing import Iterator, Union, Dict, NoReturn, List

from . import utils


logger = logging.getLogger(__name__)


LANGDETECT_SUPPORTED_LANGS = utils.get_supported_build_languages()

class NgramModelBuilder:
    def __init__(
            self,
            n: int = 2,
            lang: str | None = None,
            accepted_chars: str = "abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' "
    ):
        """
        Initialize the NgramModelBuilder.

        Parameters
        ----------
        n : int
            The size of the n-grams (e.g., 2 for bigrams, 3 for trigrams).
        lang : str
            Language code (ISO-639-1).
        accepted_chars : str
            A string of accepted characters for the n-gram model.

        Warnings
        ------
        UserWarning
            If the lang parameter is not a valid ISO-639-1 code supported by `langdetect`.
        """

        if lang is not None and lang not in LANGDETECT_SUPPORTED_LANGS:
            warning_message = (
                f"Language '{lang}' is not supported by `langdetect`. "
                "Are you sure you want to use it? "
                "`langdetect` supports language codes in ISO-639-1 format. "
                f"Complete list of languages supported by `langdetect`: {LANGDETECT_SUPPORTED_LANGS}."
            )
            warnings.warn(warning_message)
            logger.warning(f"Initiating a NgramModelBuilder object with language not supported by `langdetect` ('{lang}').")

        self.n = n
        self.lang = lang
        self.accepted_chars = accepted_chars
        self.char_count = len(self.accepted_chars)
        self.ngram_counts = defaultdict(lambda: defaultdict(int))
        self.log_probabilities = defaultdict(dict)  # Prefix -> {Suffix: log probability}

    def _normalize(self, text: str) -> str:
        """
        Normalize text by converting to lowercase and removing unaccepted characters.

        Parameters
        ----------
        text : str
            Text to be normalized.

        Returns
        -------
        str
            Normalized text.
        """
        return "".join([c.lower() for c in text if c.lower() in self.accepted_chars])

    def build_model(self, text_corpus: str | Iterator[str]) -> NoReturn:
        """
        Build the n-gram model based on the given text corpus.

        Parameters
        ----------
        text_corpus : str | Iterator[str]
            Text or iterator to build the n-gram model from.

        Returns
        -------
        None
        """
        logger.debug(f"Start training a model for language '{self.lang}'...")

        # If string is passes as a text_corpus,
        # reformat it as a list to make it compatible
        # with iterator output
        if isinstance(text_corpus, str):
            text_corpus = [text_corpus]

        for text in text_corpus:

            normalized_text = self._normalize(text)

            for i in range(len(normalized_text) - self.n + 1):
                ngram = normalized_text[i:i + self.n]
                prefix = ngram[:-1]
                suffix = ngram[-1]
                self.ngram_counts[prefix][suffix] += 1

        for prefix, suffix_counts in self.ngram_counts.items():
            total_count = sum(suffix_counts.values())
            for suffix in self.accepted_chars:
                count = self.ngram_counts[prefix].get(suffix, 0) + 1  # Add-one smoothing
                prob = count / total_count
                self.log_probabilities[prefix][suffix] = math.log(prob)

        logger.debug(f"Finished training a text quality evaluation model for language '{self.lang}'!")


    def save_model(self, file_path: str) -> NoReturn:
        """
        Save the model as a dictionary to a pickle file.

        Parameters
        ----------
        file_path : str
            The model save path.

        Returns
        -------
        None
        """

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        model_dict = {
            "n_gram": self.n,
            "accepted_chars": self.accepted_chars,
            "log_probabilities": self.log_probabilities
        }

        if self.lang:
            model_dict["lang"] = self.lang

        with open(file_path, "wb") as f:
            pickle.dump(model_dict, f)

        logger.debug(f"Saved text quality evaluation model for language '{self.lang}' into '{file_path}'.")
