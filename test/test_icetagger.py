import pytest

from test.test_data import (
    SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
    SINGLE_SENTENCE_LEGACY_TAG_PAIRS_STRING_IN_A_LIST,
    SINGLE_SENTENCE_LEGACY_TAGS,
    TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
    TWO_SENTENCE_LEGACY_TAG_PAIR_STRINGS_IN_A_LIST,
    TWO_SENTENCE_LEGACY_TAGS,
)

from src.icenlpy import icetagger


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


@pytest.mark.parametrize(
    "tokenized_sentences, tags",
    [
        (
            SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
            SINGLE_SENTENCE_LEGACY_TAGS,
        ),
        (
            TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
            TWO_SENTENCE_LEGACY_TAGS,
        ),
    ],
)
def test_icetagger_tags_only(tokenized_sentences, tags):
    tagged = icetagger.tag_text(tokenized_sentences, return_tags_only=True)
    for idx in range(len(tokenized_sentences)):
        assert tagged[idx] == tags[idx]
