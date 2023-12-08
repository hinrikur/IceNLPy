from typing import List, Tuple


SINGLE_SENTENCE_STRING: str = "Stundum, held ég, er einhver einhverju betri en ekkert."

SINGLE_SENTENCE_TOKENS: List[Tuple[str, ...]] = [
    (
        "Stundum",
        ",",
        "held",
        "ég",
        ",",
        "er",
        "einhver",
        "einhverju",
        "betri",
        "en",
        "ekkert",
        ".",
    ),
]

SINGLE_SENTENCE_TAGS: Tuple[Tuple[str, ...], ...] = (
    (
        "aa",
        "pk",
        "sfg1en",
        "fp1en",
        "pk",
        "sfg3en",
        "foken",
        "foheþ",
        "lkenvm",
        "c",
        "fohen",
        "pl",
    ),
)

SINGLE_SENTENCE_TAG_PAIRS: List[Tuple[Tuple[str, str], ...]] = [
    (
        ("Stundum", "aa"),
        (",", "pk"),
        ("held", "sfg1en"),
        ("ég", "fp1en"),
        (",", "pk"),
        ("er", "sfg3en"),
        ("einhver", "foken"),
        ("einhverju", "foheþ"),
        ("betri", "lkenvm"),
        ("en", "c"),
        ("ekkert", "fohen"),
        (".", "pl"),
    )
]

TWO_SENTENCE_STRING: str = (
    "Stundum, held ég, er einhver einhverju betri en ekkert. Hvað heldur þú?"
)

TWO_SENTENCE_TOKENS: List[Tuple[str, ...]] = [
    (
        "Stundum",
        ",",
        "held",
        "ég",
        ",",
        "er",
        "einhver",
        "einhverju",
        "betri",
        "en",
        "ekkert",
        ".",
    ),
    (
        "Hvað",
        "heldur",
        "þú",
        "?",
    ),
]

TWO_SENTENCE_TAGS: Tuple[Tuple[str, ...], ...] = (
    (
        "aa",
        "pk",
        "sfg1en",
        "fp1en",
        "pk",
        "sfg3en",
        "foken",
        "foheþ",
        "lkenvm",
        "c",
        "fohen",
        "pl",
    ),
    (
        "fsheo",
        "sfg2en",
        "fp2en",
        "pl",
    ),
)

TWO_SENTENCE_TAG_PAIRS: List[Tuple[Tuple[str, str], ...]] = [
    (
        ("Stundum", "aa"),
        (",", "pk"),
        ("held", "sfg1en"),
        ("ég", "fp1en"),
        (",", "pk"),
        ("er", "sfg3en"),
        ("einhver", "foken"),
        ("einhverju", "foheþ"),
        ("betri", "lkenvm"),
        ("en", "c"),
        ("ekkert", "fohen"),
        (".", "pl"),
    ),
    (
        ("Hvað", "fsheo"),
        ("heldur", "sfg2en"),
        ("þú", "fp2en"),
        ("?", "pl"),
    ),
]

SINGLE_SENTENCE_ICEPARSER_OUTPUT_OLD_TAGSET: List[str] = [
    "[AdvP Stundum aa ] , , [VP held sfg1en ] [NP ég fp1en ] , , [VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ] [CP en c ] [NP ekkert fohen ] ] . . \n"
]
SINGLE_SENTENCE_ICEPARSER_OUTPUT_MIM_GOLD: List[str] = [
    "[AdvP Stundum aa ] , pk [VP held sfg1en ] [NP ég fp1en ] , pk [VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ] [CP en c ] [NP ekkert fohen ] ] . pl \n"
]

TWO_SENTENCE_ICEPARSER_OUTPUT_OLD_TAGSET: List[str] = [
    "[AdvP Stundum aa ] , , [VP held sfg1en ] [NP ég fp1en ] , , [VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ] [CP en c ] [NP ekkert fohen ] ] . . \n",
    "[NPs [NP Hvað fshen ] [CP heldur c ] [NP þú fp2en ] ] ? ? \n",
]

TWO_SENTENCE_ICEPARSER_OUTPUT_MIM_GOLD: List[str] = [
    "[AdvP Stundum aa ] , pk [VP held sfg1en ] [NP ég fp1en ] , pk [VPb er sfg3en ] [NPs [NP einhver foken einhverju foheþ [AP betri lkenvm ] ] [CP en c ] [NP ekkert fohen ] ] . pl \n",
    "[NP Hvað fsheo ] [VP heldur sfg2en ] [NP þú fp2en ] ? pl \n",
]


SINGLE_SENTENCE_TOKEN_STRING_IN_A_LIST: List[str] = [
    " ".join(list(SINGLE_SENTENCE_TOKENS[0]))
]
TWO_SENTENCE_TOKEN_STRINGS_IN_A_LIST: List[str] = [
    " ".join(list(sentence)) for sentence in TWO_SENTENCE_TOKENS
]
SINGLE_SENTENCE_TOKEN_TAG_PAIRS_STRING_IN_A_LIST: List[str] = [
    " ".join([" ".join(pair) for pair in sentence])
    for sentence in SINGLE_SENTENCE_TAG_PAIRS
]
TWO_SENTENCE_TOKEN_TAG_PAIR_STRINGS_IN_A_LIST = [
    " ".join([" ".join(pair) for pair in sentence])
    for sentence in TWO_SENTENCE_TAG_PAIRS
]
