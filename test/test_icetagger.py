import pytest

from test.test_data import (
    SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
    SINGLE_SENTENCE_LEGACY_TAG_PAIRS_STRING_IN_A_LIST,
    TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
    TWO_SENTENCE_LEGACY_TAG_PAIR_STRINGS_IN_A_LIST,
)

from icenlpy import icetagger


@pytest.mark.parametrize(
    "tokenized_sentences, token_tag_pairs",
    [
        (
            SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
            SINGLE_SENTENCE_LEGACY_TAG_PAIRS_STRING_IN_A_LIST,
        ),
        (
            TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
            TWO_SENTENCE_LEGACY_TAG_PAIR_STRINGS_IN_A_LIST,
        ),
    ],
)
def test_icetagger(
    tokenized_sentences,
    token_tag_pairs,
):
    tagged = icetagger.tag_text(tokenized_sentences)
    print(tagged)
    print(token_tag_pairs)
    for idx in range(len(tokenized_sentences)):
        assert tagged[idx] == token_tag_pairs[idx]
