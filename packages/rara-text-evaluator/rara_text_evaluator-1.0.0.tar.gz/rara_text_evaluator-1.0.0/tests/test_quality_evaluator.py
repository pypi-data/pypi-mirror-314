import pytest

from rara_text_evaluator import exceptions
from rara_text_evaluator.quality_evaluator import QualityEvaluator, DEFAULT_RESPONSE, DEFAULT_TEXT_SIZE_REQUIREMENT


def test_quality_evaluator_process():
    evaluator = QualityEvaluator()
    text = "Elas kord üks muinasjutt ja see muinasjutt sai läbi!!"
    probability = evaluator.get_probability(text)
    assert len(text) > DEFAULT_TEXT_SIZE_REQUIREMENT
    assert probability > DEFAULT_RESPONSE


def test_short_text_returning_default_response():
    evaluator = QualityEvaluator()
    text = "See on lühike!"
    probability = evaluator.get_probability(text)
    assert len(text) < DEFAULT_TEXT_SIZE_REQUIREMENT
    assert probability == DEFAULT_RESPONSE


def test_fallback_language_being_used():
    evaluator = QualityEvaluator()
    text = ("Maanantaista torstaihin herään viisitoista yli seitsemän. "
            "Perjantaisin herään kahdeksalta, koska oppituntini alkavat myöhemmin. "
            "Herättyäni syön aamupalaa, puen päälleni ja menen kouluun.!")
    evaluator.get_probability(text)
    assert evaluator.model_lang is None


def test_using_defined_language_instead_of_autodetect():
    evaluator = QualityEvaluator()
    text = "Milline on kiirem, euroopa või aafrika pääsuke? Ma tahan teada!"
    evaluator.get_probability(text, lang="en")
    assert evaluator.model_lang == "en"


def test_using_wrong_language_code_results_in_fallback():
    evaluator = QualityEvaluator()
    text = "Milline on kiirem, euroopa või aafrika pääsuke? Ma tahan teada!"
    language_code = "fin"
    evaluator.get_probability(text, lang=language_code)
    assert language_code not in evaluator.language_model_container
    assert evaluator.model_lang is None


def test_different_texts_returning_unique_test_quality_answers():
    evaluator = QualityEvaluator()
    texts = [
        "Teadavasti, kui inimene on kergem kui part, siis ta on nõid!",
        "Võtke pühalt käsigranaadilt tema kaitse ja lugege arve kolm, ei loe mitte kaks ja kindlasti mitte neli.",
        "Mis on su nimi? Kust sa tuled? Mis on ühe pääsukese maksimum lendamiskiirus?"
    ]

    qualities = []
    for text in texts:
        qualities.append(evaluator.get_probability(text))

    assert len(set(qualities)) == len(texts)


def test_exception_being_thrown_when_no_models_loaded():
    evaluator = QualityEvaluator(load_defaults=False)
    text = "Milline on kiirem, euroopa või aafrika pääsuke? Ma tahan teada!"
    with pytest.raises(exceptions.InvalidRegistryError):
        evaluator.get_probability(text, lang="et")


def test_updating_length_limit():
    evaluator = QualityEvaluator()
    test_text = "tere tere vana kere"

    probability_1 = evaluator.get_probability(test_text, lang="et")
    assert probability_1 == DEFAULT_RESPONSE

    probability_2 = evaluator.get_probability(test_text, lang="et", length_limit=5)
    assert probability_2 != DEFAULT_RESPONSE


def test_updating_default_response():
    evaluator = QualityEvaluator()
    test_text = "tere tere vana kere"
    length_limit = 50
    language = "et"

    probability_1 = evaluator.get_probability(
        test_text,
        lang=language,
        length_limit=length_limit
    )
    assert probability_1 == DEFAULT_RESPONSE

    updated_default_response = -1

    probability_2 = evaluator.get_probability(
        test_text,
        lang=language,
        length_limit=length_limit,
        default_response=updated_default_response
    )
    assert probability_2 != DEFAULT_RESPONSE
    assert probability_2 == updated_default_response


def test_is_valid_et():
    test_text = "Wanemuine. Piihapüewal, 7. weebruaril s. a, Kmemllk KM. Operett 3 järgus. Planquette muusika. Kakatus kess 8 õhtu."
    evaluator = QualityEvaluator()
    evaluator.set_threshold(lang="et", threshold=0.8)

    is_valid_1 = evaluator.is_valid(test_text, lang="et")
    assert not is_valid_1

    evaluator.set_threshold(lang="et", threshold=0.4)
    is_valid_2 = evaluator.is_valid(test_text, lang="et")
    assert is_valid_2


def test_restoring_default_thresholds():
    evaluator = QualityEvaluator()
    default_threshold = evaluator.default_threshold

    et_old_threshold = evaluator.thresholds["et"]
    et_new_threshold = 0.234
    assert et_old_threshold != et_new_threshold
    assert default_threshold == et_old_threshold

    evaluator.set_threshold(lang="et", threshold=et_new_threshold)
    assert et_new_threshold == evaluator.thresholds["et"]
    assert default_threshold != evaluator.thresholds["et"]

    evaluator.set_threshold(lang="et", threshold=evaluator.default_threshold)
    assert evaluator.thresholds["et"] == default_threshold


def test_invalid_threshold_setting():
    evaluator = QualityEvaluator()
    # Check that erroris raised with invalid language
    with pytest.raises(exceptions.InvalidInputError) as exception_info:
        evaluator.set_threshold(lang="blablabla", threshold=0.8)

    # Check that error is raised with invalid threshold
    with pytest.raises(exceptions.InvalidInputError) as exception_info:
        evaluator.set_threshold(lang="et", threshold=7.6)

    # Check that NO errors are raise with valid input
    evaluator.set_threshold(lang="et", threshold=0.6)
