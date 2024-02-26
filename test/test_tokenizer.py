from test.test_data import (
    SINGLE_SENTENCE_STRING,
    SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST,
    SINGLE_SENTENCE_TOKENS,
    TWO_SENTENCE_STRING,
    TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST,
    TWO_SENTENCE_TOKENS,
)


def test_tokenizer():
    from src.icenlpy import tokenizer

    tokenized = tokenizer.tokenize(SINGLE_SENTENCE_STRING)
    for sentence in SINGLE_SENTENCE_TOKENS:
        tok_sent = next(tokenized)
        for token in sentence:
            assert token == next(tok_sent)

    tokenized = tokenizer.tokenize(TWO_SENTENCE_STRING)
    for sentence in TWO_SENTENCE_TOKENS:
        tok_sent = next(tokenized)
        for token in sentence:
            assert token == next(tok_sent)


def test_split_into_sentences():
    from src.icenlpy import tokenizer

    input_sentence = SINGLE_SENTENCE_STRING
    expected = SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST[0]
    sentences = tokenizer.split_into_sentences(input_sentence)
    assert sentences == [expected]

    input_sentence = TWO_SENTENCE_STRING
    expected = TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST
    sentences = tokenizer.split_into_sentences(input_sentence)
    assert sentences == expected
