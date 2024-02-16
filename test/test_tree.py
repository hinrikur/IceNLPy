import pytest
from src.icenlpy.tree import TerminalNode, Phrase, IceNLPySentence

from typing import List, Tuple

# Test data for Phrase and IceNLPySentence classes
NP_DATA: List[Tuple[str, str]] = [
    ("ein", "det"),
    ("foven", "adj"),
    ("setningin", "noun"),
]
VP_DATA: List[Tuple[str, str]] = [("kemur", "verb")]


# Test TerminalNode
@pytest.mark.parametrize("word, tag", [("word", "tag"), ("another", "noun")])
def test_terminal_node_creation(word, tag):
    node = TerminalNode(word, tag)
    assert node.word == word
    assert node.tag == tag


# Test Phrase
def test_phrase_creation_and_terminal_addition():
    np_phrase = Phrase("NP")
    for word, tag in NP_DATA:
        np_phrase.add_child(TerminalNode(word, tag))

    assert np_phrase.label == "NP"
    assert len(np_phrase.elements) == len(NP_DATA)
    for terminal, (word, tag) in zip(np_phrase.elements, NP_DATA):
        assert terminal.word == word
        assert terminal.tag == tag


def test_phrase_adding_invalid_child():
    phrase = Phrase("X")
    with pytest.raises(TypeError):
        phrase.add_child("not a phrase")


# Test IceNLPySentence
def test_sentence_creation_and_child_adding():
    np_phrase = Phrase("NP")
    for word, tag in NP_DATA:
        np_phrase.add_child(TerminalNode(word, tag))

    vp_phrase = Phrase("VP")
    for word, tag in VP_DATA:
        vp_phrase.add_child(TerminalNode(word, tag))

    sentence = IceNLPySentence([np_phrase, vp_phrase])

    assert len(sentence.phrases) == 2
    assert sentence.phrases[0] == np_phrase
    assert sentence.phrases[1] == vp_phrase


def test_sentence_creation_with_invalid_phrases():
    with pytest.raises(ValueError):
        IceNLPySentence(["not a phrase", Phrase("NP")])


# Test for Phrase __str__
def test_phrase_repr():
    np_phrase = Phrase("NP")
    np_phrase.add_children([TerminalNode("ein", "det"), TerminalNode("bók", "noun")])
    expected_repr = "[NP ein det bók noun ]"
    assert repr(np_phrase) == expected_repr


# Test for IceNLPySentence __str__
@pytest.mark.parametrize(
    "phrases, expected_repr",
    [
        (
            [Phrase("NP"), Phrase("VP")],
            "[NP  ] [VP  ]",
        ),
        (
            [Phrase("NP"), Phrase("VP"), Phrase("PP")],
            "[NP  ] [VP  ] [PP  ]",
        ),
        ([Phrase("NP", elements=[TerminalNode("ein", "det")])], "[NP ein det ]"),
        (
            [
                Phrase("NP", elements=[TerminalNode("ein", "det")]),
                Phrase("VP", elements=[TerminalNode("kemur", "verb")]),
            ],
            "[NP ein det ] [VP kemur verb ]",
        ),
        (
            [
                Phrase(
                    "NP",
                    elements=[
                        TerminalNode("ein", "det"),
                        Phrase(
                            "PP",
                            elements=[
                                TerminalNode("í", "prep"),
                                TerminalNode("bók", "noun"),
                            ],
                        ),
                    ],
                ),
                Phrase("VP", elements=[TerminalNode("kemur", "verb")]),
            ],
            "[NP ein det [PP í prep bók noun ] ] [VP kemur verb ]",
        ),
    ],
)
def test_sentence_repr(phrases, expected_repr):
    sentence = IceNLPySentence(phrases)
    assert str(sentence) == expected_repr


def test_from_string():
    single_phrase = IceNLPySentence("[NP ein det bók noun ]")
    assert str(single_phrase) == "[NP ein det bók noun ]"
    assert single_phrase.phrases[0].label == "NP"
    assert single_phrase.phrases[0].elements[0].word == "ein"
    assert single_phrase.phrases[0].elements[0].tag == "det"
    assert single_phrase.phrases[0].elements[1].word == "bók"
    assert single_phrase.phrases[0].elements[1].tag == "noun"
    single_nested_phrase = IceNLPySentence("[NP ein det [PP í prep bók noun ] ]")
    assert str(single_nested_phrase) == "[NP ein det [PP í prep bók noun ] ]"
    assert single_nested_phrase.phrases[0].label == "NP"
    assert single_nested_phrase.phrases[0].elements[0].word == "ein"
    assert single_nested_phrase.phrases[0].elements[0].tag == "det"
    assert single_nested_phrase.phrases[0].elements[1].label == "PP"
    assert single_nested_phrase.phrases[0].elements[1].elements[0].word == "í"
    assert single_nested_phrase.phrases[0].elements[1].elements[0].tag == "prep"
    assert single_nested_phrase.phrases[0].elements[1].elements[1].word == "bók"
    assert single_nested_phrase.phrases[0].elements[1].elements[1].tag == "noun"
    complex_nested_phrase = IceNLPySentence(
        "[NP ein det [PP í prep bók noun ] ] [VP kemur verb ]"
    )
    assert (
        str(complex_nested_phrase)
        == "[NP ein det [PP í prep bók noun ] ] [VP kemur verb ]"
    )
    assert complex_nested_phrase.phrases[0].label == "NP"
    assert complex_nested_phrase.phrases[0].elements[0].word == "ein"
    assert complex_nested_phrase.phrases[0].elements[0].tag == "det"
    assert complex_nested_phrase.phrases[0].elements[1].label == "PP"
    assert complex_nested_phrase.phrases[0].elements[1].elements[0].word == "í"
    assert complex_nested_phrase.phrases[0].elements[1].elements[0].tag == "prep"
    assert complex_nested_phrase.phrases[0].elements[1].elements[1].word == "bók"
    assert complex_nested_phrase.phrases[0].elements[1].elements[1].tag == "noun"

    actual_output = (
        "[AdvP Stundum aa ] , , [VP held sfg1en ] [NP ég fp1en ] , ,"
        "[VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ]"
        "[CP en c ] [NP ekkert fohen ] ] . . \n"
    )
    expected_format = (
        "[AdvP Stundum aa ] , , [VP held sfg1en ] [NP ég fp1en ] , , "
        "[VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ] "
        "[CP en c ] [NP ekkert fohen ] ] . ."
    )

    sentence = IceNLPySentence(actual_output)

    assert str(sentence) == expected_format
