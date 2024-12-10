import pathlib

import pytest
import warnings

from rara_text_evaluator.ngram_model_builder import NgramModelBuilder
from rara_text_evaluator.quality_evaluator import QualityEvaluator, DEFAULT_RESPONSE

DEFAULT_FILENAME = "ngram_model.pkl"


@pytest.fixture(autouse=True)
def delete_model_file(request):
    if "override" in request.keywords:
        yield
    else:
        yield
        path = pathlib.Path(DEFAULT_FILENAME)
        path.unlink()
        assert path.exists() is False


def test_model_training_process_with_et_text(delete_model_file):
    language = "et"

    qv = QualityEvaluator()
    test_text_en = "You should be aware that asking whether an african or european swallow is faster is inappropriate!"
    test_text_et = "Ta lisas, et Eesti meretuuleparke alles planeeritakse ning et sinna, kus need hakkavad..."

    en_probability_default_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_default_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")


    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' ")
    text_corpus = "Kas sa oled teadlik sellest et märgade mõõkade loopimine ei ole alus ühe õiglase valitsuse loomiseks!?"
    nmb.build_model(text_corpus)
    nmb.save_model(DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()


    qv.add_model(lang=language, model_path=DEFAULT_FILENAME)
    en_probability_new_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_new_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")

    # The probability for EN text should not change as the model remains the same
    assert en_probability_default_model == en_probability_new_model

    # The probability for ET text should change as we replaced the default model
    # with the new model we trained
    assert et_probability_default_model != et_probability_new_model


def test_model_training_process_with_en_text(delete_model_file):
    language = "en"
    qv = QualityEvaluator()
    test_text_en = "You should be aware that asking whether an african or european swallow is faster is inappropriate!"
    test_text_et = "Ta lisas, et Eesti meretuuleparke alles planeeritakse ning et sinna, kus need hakkavad..."

    en_probability_default_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_default_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")


    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' ")
    text_corpus = "Kas sa oled teadlik sellest et märgade mõõkade loopimine ei ole alus ühe õiglase valitsuse loomiseks!?"
    nmb.build_model(text_corpus)
    nmb.save_model(DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()


    qv.add_model(lang=language, model_path=DEFAULT_FILENAME)
    en_probability_new_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_new_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")

    # The probability for ET text should not change as the model remains the same
    assert et_probability_default_model == et_probability_new_model

    # The probability for EN text should change as we replaced the default model
    # with the new model we trained
    assert en_probability_default_model != en_probability_new_model


def test_model_training_process_with_et_iterator(delete_model_file):
    language = "et"

    qv = QualityEvaluator()
    test_text_en = "You should be aware that asking whether an african or european swallow is faster is inappropriate!"
    test_text_et = "Ta lisas, et Eesti meretuuleparke alles planeeritakse ning et sinna, kus need hakkavad..."

    en_probability_default_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_default_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")


    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' ")
    text_corpus = [
        "Kas sa oled",
        "teadlik sellest et",
        "märgade mõõkade loopimine",
        "ei ole alus ühe õiglase valitsuse loomiseks!?"
    ]
    text_iterator = (text for text in text_corpus)
    nmb.build_model(text_corpus)
    nmb.save_model(DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()


    qv.add_model(lang=language, model_path=DEFAULT_FILENAME)
    en_probability_new_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_new_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")

    # The probability for EN text should not change as the model remains the same
    assert en_probability_default_model == en_probability_new_model

    # The probability for ET text should change as we replaced the default model
    # with the new model we trained
    assert et_probability_default_model != et_probability_new_model
    assert et_probability_new_model > 0


def test_model_training_process_with_en_iterator(delete_model_file):
    language = "en"
    qv = QualityEvaluator()
    test_text_en = "You should be aware that asking whether an african or european swallow is faster is inappropriate!"
    test_text_et = "Ta lisas, et Eesti meretuuleparke alles planeeritakse ning et sinna, kus need hakkavad..."

    en_probability_default_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_default_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")


    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcdefghijklmnopqrstuvwxyzõäöü.,:;-_!\"()%@1234567890' ")
    text_corpus = [
        "You should be aware",
        "that asking whether",
        "an african or european swallow",
        "is inappropriate!?"
    ]
    text_iterator = (text for text in text_corpus)
    nmb.build_model(text_corpus)
    nmb.save_model(DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()


    qv.add_model(lang=language, model_path=DEFAULT_FILENAME)
    en_probability_new_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_new_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")

    # The probability for ET text should not change as the model remains the same
    assert et_probability_default_model == et_probability_new_model

    # The probability for EN text should change as we replaced the default model
    # with the new model we trained
    assert en_probability_default_model != en_probability_new_model
    assert en_probability_new_model > 0

def test_model_training_process_with_ru_text(delete_model_file):
    language = "ru"

    qv = QualityEvaluator()
    test_text_en = "You should be aware that asking whether an african or european swallow is faster is inappropriate!"
    test_text_et = "Ta lisas, et Eesti meretuuleparke alles planeeritakse ning et sinna, kus need hakkavad..."
    test_text_ru = "От планов до строительства еще нужно пройти долгий путь, на этапе планирования у нас"

    en_probability_default_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_default_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")
    ru_probability_default_model = qv.get_probability(text=test_text_ru, length_limit=1, lang="ru")


    nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="бфждёпнчргейъзлвтьэсхщюуишмыкоаця.,:;-_!\"()%@1234567890' ")
    text_corpus = "Мы уже высказали свою точку зрения и будем продолжать это делать. Это требует очень точных!?"
    nmb.build_model(text_corpus)
    nmb.save_model(DEFAULT_FILENAME)

    assert pathlib.Path(DEFAULT_FILENAME).exists()

    qv.add_model(lang=language, model_path=DEFAULT_FILENAME)
    en_probability_new_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_new_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")
    ru_probability_new_model = qv.get_probability(text=test_text_ru, length_limit=1, lang="ru")

    # The probability for EN text should not change as the model remains the same
    assert en_probability_default_model == en_probability_new_model

    # The probability for ET text should not change as the model remains the same
    assert et_probability_default_model == et_probability_new_model

    # The probability for RU text should change as we replaced the default model
    # with the new model we trained
    assert ru_probability_default_model != ru_probability_new_model
    assert ru_probability_new_model > 0


def test_model_training_process_with_custom_lang_text(delete_model_file):
    language = "klingon"

    qv = QualityEvaluator()
    test_text_en = "You should be aware that asking whether an african or european swallow is faster is inappropriate!"
    test_text_et = "Ta lisas, et Eesti meretuuleparke alles planeeritakse ning et sinna, kus need hakkavad..."
    test_text_kl = "vaj nItebHa'vam vIghoS,"

    en_probability_default_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_default_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")
    kl_probability_default_model = qv.get_probability(text=test_text_kl, length_limit=1)

    with warnings.catch_warnings(record=True) as warning_record:
        nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="jilnrguhqtmpseybvwaocd.,:;-_!\"()%@1234567890' ")
        text_corpus = "'ach cha'logh nItebHa' 'ej mIw vIghoS 'e' vIghoS, 'each vIghoS 'ej cha'logh vIghoS"
        nmb.build_model(text_corpus)
        nmb.save_model(DEFAULT_FILENAME)

    # A warning should be thrown for a language not supported by langdetect
    print(warning_record[-1])
    assert len(warning_record) == 1
    assert warning_record[0].category == UserWarning

    assert pathlib.Path(DEFAULT_FILENAME).exists()

    qv.add_model(lang=language, model_path=DEFAULT_FILENAME)
    en_probability_new_model = qv.get_probability(text=test_text_en, length_limit=1, lang="en")
    et_probability_new_model = qv.get_probability(text=test_text_et, length_limit=1, lang="et")
    kl_probability_new_model = qv.get_probability(text=test_text_kl, length_limit=1, lang="klingon")

    # The probability for EN text should not change as the model remains the same
    assert en_probability_default_model == en_probability_new_model

    # The probability for ET text should not change as the model remains the same
    assert et_probability_default_model == et_probability_new_model

    # The probability for klingon text should change as we replaced the default model
    # with the new model we trained
    assert kl_probability_default_model != kl_probability_new_model
    assert kl_probability_new_model > 0

@pytest.mark.override
def test_warning_is_thrown_for_unsupported_language():
    language = "bleh"
    with warnings.catch_warnings(record=True) as warning_record:
        nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcde")

    assert len(warning_record) == 1
    assert warning_record[0].category == UserWarning

@pytest.mark.override
def test_warning_is_not_thrown_for_supported_language():
    language = "ru"
    with warnings.catch_warnings(record=True) as warning_record:
        nmb = NgramModelBuilder(n=2, lang=language, accepted_chars="abcde")

    assert len(warning_record) == 0
