import pytest

from test.test_data import (
    SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
    SINGLE_SENTENCE_TOKEN_TAG_PAIRS_STRING_IN_A_LIST,
    SINGLE_SENTENCE_ICEPARSER_OUTPUT_OLD_TAGSET,
    SINGLE_SENTENCE_ICEPARSER_OUTPUT_MIM_GOLD,
    TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
    TWO_SENTENCE_TOKEN_TAG_PAIR_STRINGS_IN_A_LIST,
    TWO_SENTENCE_ICEPARSER_OUTPUT_OLD_TAGSET,
    TWO_SENTENCE_ICEPARSER_OUTPUT_MIM_GOLD,
)

from icenlpy import iceparser


@pytest.mark.parametrize(
    "tokenized_sentences, token_tag_pairs, legacy_expected, gold_expected",
    [
        (
            SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
            SINGLE_SENTENCE_TOKEN_TAG_PAIRS_STRING_IN_A_LIST,
            SINGLE_SENTENCE_ICEPARSER_OUTPUT_OLD_TAGSET,
            SINGLE_SENTENCE_ICEPARSER_OUTPUT_MIM_GOLD,
        ),
        (
            TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
            TWO_SENTENCE_TOKEN_TAG_PAIR_STRINGS_IN_A_LIST,
            TWO_SENTENCE_ICEPARSER_OUTPUT_OLD_TAGSET,
            TWO_SENTENCE_ICEPARSER_OUTPUT_MIM_GOLD,
        ),
    ],
)
def test_iceparser(
    tokenized_sentences, token_tag_pairs, legacy_expected, gold_expected
):
    legacy_parsed = iceparser.parse_text(tokenized_sentences, legacy_tagger=True)
    gold_parsed = iceparser.parse_text(token_tag_pairs, legacy_tagger=False)

    assert len(legacy_parsed) == len(legacy_expected)
    assert len(gold_parsed) == len(gold_expected)

    for idx in range(len(tokenized_sentences)):
        assert legacy_parsed[idx] == legacy_expected[idx]
        assert gold_parsed[idx] == gold_expected[idx]
