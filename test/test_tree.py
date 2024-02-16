import pytest
from src.icenlpy.tree import TerminalNode, Phrase, IceNLPySentence
from src.icenlpy import iceparser

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


def test_tree_view():
    all_args = {
        "f": True,
        "a": True,
        "m": True,
    }

    single_phrase = IceNLPySentence("[NP ein det bók noun ]")
    expected_view = "S0\n+-NP\n  +-det: 'ein'\n  +-noun: 'bók'\n"
    assert single_phrase.view == expected_view

    single_nested_phrase = IceNLPySentence("[NP ein det [PP í prep bók noun ] ]")
    expected_view = (
        "S0\n+-NP\n  +-det: 'ein'\n  +-PP\n    +-prep: 'í'\n    +-noun: 'bók'\n"
    )

    complex_nested_phrase = IceNLPySentence(
        "[NP ein det [PP í prep bók noun ] ] [VP kemur verb ]"
    )
    expected_view = (
        "S0\n+-NP\n  +-det: 'ein'\n  +-PP\n    +-prep: 'í'\n    +-noun: 'bók'\n"
        "+-VP\n  +-verb: 'kemur'\n"
    )
    assert complex_nested_phrase.view == expected_view

    actual_sentence = "Stundum held ég, er einhver einhverju betri en ekkert ."
    actual_parsed = iceparser.parse_text([actual_sentence], legacy_tagger=True)
    # actual_output = (
    #     "[AdvP Stundum aa ] , , [VP held sfg1en ] [NP ég fp1en ] , ,"
    #     "[VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ]"
    #     "[CP en c ] [NP ekkert fohen ] ] . . \n"
    # )
    sentence = IceNLPySentence(actual_parsed[0])
    # print(sentence.view)
    expected_view = (
        "S0\n+-AdvP\n  +-aa: 'Stundum'\n+-VP\n  +-sfg1en: 'held'\n+-NP\n"
        "  +-fp1en: 'ég'\n+-,: ','\n+-VPb\n  +-sfg3en: 'er'\n+-NPs\n  +-NP\n    +-foken: "
        "'einhver'\n    +-foheþ: 'einhverju'\n    +-AP\n      +-lkenvm: 'betri'\n  +-CP\n    "
        "+-c: 'en'\n  +-NP\n    +-fohen: 'ekkert'\n+-.: '.'\n"
    )
    assert sentence.view == expected_view

    actual_sentence_all_args = iceparser.parse_text(
        [actual_sentence], legacy_tagger=True, args=all_args
    )
    sentence = IceNLPySentence(actual_sentence_all_args[0])
    expected_view_with_args = (
        "S0\n+-AdvP\n  +-aa: 'Stundum'\n+-VP\n  +-sfg1en: 'held'\n+-NP-SUBJ<\n"
        "  +-fp1en: 'ég'\n+-,: ','\n+-VPb?Vn?\n  +-sfg3en: 'er'\n+-NPs-SUBJ<\n  +-NP?NgNc?\n    +-foken: "
        "'einhver'\n    +-foheþ: 'einhverju'\n    +-AP\n      +-lkenvm: 'betri'\n  +-CP\n    "
        "+-c: 'en'\n  +-NP\n    +-fohen: 'ekkert'\n+-.: '.'\n"
    )
    assert sentence.view == expected_view_with_args

    complex_sentence = (
        "Drengirnir fóru í bíó og tóku strætó heim en vagninn "
        "bilaði á miðri leið og þeir þurftu að ganga meira en helming "
        "leiðarinnar því hvorki foreldrar Jóns né Óttars svöruðu símanum "
        "og þeir höfðu ekki aðra til að hringja í og biðja um að sækja sig."
    )

    very_complex_parse = iceparser.parse_text(
        [complex_sentence],
        legacy_tagger=True,
    )
    sentence = IceNLPySentence(very_complex_parse[0])
    complex_sentence_expected_view = (
        "S0\n+-NP\n  +-nkfng: 'Drengirnir'\n+-VP\n  +-sfg3fþ: 'fóru'\n+-PP\n"
        "  +-ao: 'í'\n  +-NP\n    +-nheo: 'bíó'\n+-CP\n  +-c: 'og'\n+-VP\n  +-sfg3fþ: 'tóku'\n+-NP\n"
        "  +-nkeo: 'strætó'\n+-AdvP\n  +-aa: 'heim'\n+-CP\n  +-c: 'en'\n+-NP\n  +-nkeng: 'vagninn'\n+-VP\n"
        "  +-sfg3eþ: 'bilaði'\n+-PP\n  +-aþ: 'á'\n  +-NP\n    +-AP\n      +-lveþsf: 'miðri'\n    +-nveþ: "
        "'leið'\n+-CP\n  +-c: 'og'\n+-NP\n  +-fpkfn: 'þeir'\n+-VP\n  +-sfg3fþ: 'þurftu'\n+-VPi\n  "
        "+-cn: 'að'\n  +-sng: 'ganga'\n+-AP\n  +-lhenvm: 'meira'\n+-CP\n  +-c: 'en'\n+-NP\n  +-nkeo: "
        "'helming'\n+-NP\n  +-nveeg: 'leiðarinnar'\n+-NP\n  +-fpheþ: 'því'\n+-SCP\n  +-c: "
        "'hvorki'\n+-NPs\n  +-NP\n    +-nkfn: 'foreldrar'\n  +-NP\n    +-nkee-s: 'Jóns'\n  "
        "+-CP\n    +-c: 'né'\n  +-NP\n    +-nxfn-s: 'Óttars'\n+-VP\n  +-sfg3fþ: 'svöruðu'\n+-NP\n  "
        "+-nkeþg: 'símanum'\n+-CP\n  +-c: 'og'\n+-NP\n  +-fpkfn: 'þeir'\n+-VP\n  +-sfg3fþ: 'höfðu'\n+-AdvP\n"
        "  +-aa: 'ekki'\n+-NP\n  +-foveo: 'aðra'\n+-MWE_CP\n  +-ae: 'til'\n  +-cn: 'að'\n+-VPi\n  "
        "+-sng: 'hringja'\n+-AdvP\n  +-aa: 'í'\n+-CP\n  +-c: 'og'\n+-VPi\n  +-sng: 'biðja'\n+-PP\n  +-ao: "
        "'um'\n  +-VPi\n    +-cn: 'að'\n    +-sng: 'sækja'\n+-NP\n  +-fpkfo: 'sig'\n+-.: '.'\n"
    )
    assert sentence.view == complex_sentence_expected_view
    complex_sentence_parse_with_args = iceparser.parse_text(
        [complex_sentence], legacy_tagger=True, args=all_args
    )
    sentence = IceNLPySentence(complex_sentence_parse_with_args[0])
    complex_sentence_expected_view_with_args = (
        "S0\n+-NP-SUBJ>\n  +-nkfng: 'Drengirnir'\n+-VP\n  +-sfg3fþ: 'fóru'\n+-PP\n"
        "  +-ao: 'í'\n  +-NP\n    +-nheo: 'bíó'\n+-CP\n  +-c: 'og'\n+-VP\n  +-sfg3fþ: 'tóku'\n+-NP-OBJ<\n"
        "  +-nkeo: 'strætó'\n+-AdvP\n  +-aa: 'heim'\n+-CP\n  +-c: 'en'\n+-NP-SUBJ>\n  +-nkeng: 'vagninn'\n+-VP\n"
        "  +-sfg3eþ: 'bilaði'\n+-PP\n  +-aþ: 'á'\n  +-NP\n    +-AP\n      +-lveþsf: 'miðri'\n    +-nveþ: "
        "'leið'\n+-CP\n  +-c: 'og'\n+-NP-SUBJ>\n  +-fpkfn: 'þeir'\n+-VP\n  +-sfg3fþ: 'þurftu'\n+-VPi\n  "
        "+-cn: 'að'\n  +-sng: 'ganga'\n+-AP\n  +-lhenvm: 'meira'\n+-CP\n  +-c: 'en'\n+-NP\n  +-nkeo: "
        "'helming'\n+-NP-QUAL\n  +-nveeg: 'leiðarinnar'\n+-NP\n  +-fpheþ: 'því'\n+-SCP\n  +-c: "
        "'hvorki'\n+-NPs-SUBJ>\n  +-NP\n    +-nkfn: 'foreldrar'\n  +-NP-QUAL\n    +-nkee-s: 'Jóns'\n  "
        "+-CP\n    +-c: 'né'\n  +-NP\n    +-nxfn-s: 'Óttars'\n+-VP\n  +-sfg3fþ: 'svöruðu'\n+-NP-OBJ<\n  "
        "+-nkeþg: 'símanum'\n+-CP\n  +-c: 'og'\n+-NP-SUBJ>\n  +-fpkfn: 'þeir'\n+-VP\n  +-sfg3fþ: 'höfðu'\n+-AdvP\n"
        "  +-aa: 'ekki'\n+-NP-OBJ<\n  +-foveo: 'aðra'\n+-MWE_CP\n  +-ae: 'til'\n  +-cn: 'að'\n+-VPi\n  "
        "+-sng: 'hringja'\n+-AdvP\n  +-aa: 'í'\n+-CP\n  +-c: 'og'\n+-VPi\n  +-sng: 'biðja'\n+-PP\n  +-ao: "
        "'um'\n  +-VPi\n    +-cn: 'að'\n    +-sng: 'sækja'\n+-NP-OBJ<\n  +-fpkfo: 'sig'\n+-.: '.'\n"
    )
    assert sentence.view == complex_sentence_expected_view_with_args
