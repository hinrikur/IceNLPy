import re
import logging

from typing import List, Union, TypeVar

TPhrase = TypeVar("TPhrase", bound="Phrase")

logger = logging.getLogger(__name__)


class TerminalNode:
    """A basic representation of a token-tag pair in the phrase structure"""

    def __init__(self, word: str, tag: str):
        self.word = word
        self.tag = tag

    def __str__(self):
        return f"{self.word} {self.tag}"

    def __repr__(self):
        return f"({self.word}, {self.tag})"


class Phrase:
    """A phrase in a parsed sentence"""

    def __init__(
        self: TPhrase,
        label: str,
        elements: Union[List[Union[TerminalNode, TPhrase]], None] = None,
    ):
        self.label = label
        self.elements = []
        if elements is not None:
            for element in elements:
                self.add_child(element)

    def add_child(self, child):
        if isinstance(child, Phrase) or isinstance(child, TerminalNode):
            self.elements.append(child)
        else:
            raise TypeError("Child must be either a Phrase or a TerminalNode")

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def __str__(self):
        return f"[{self.label} {' '.join(str(e) for e in self.elements)} ]"

    def __repr__(self):
        return self.__str__()


class IceNLPySentence:
    def __init__(self, input_data):
        if isinstance(input_data, str):
            self.phrases: List[Phrase] = self._parse_from_string(input_data)
        elif all(isinstance(p, Phrase) for p in input_data):
            self.phrases: List[Phrase] = input_data
        else:
            raise ValueError("Input must be a string or a list of Phrase objects")

    def _parse_from_string(self, input_str: str) -> List[Phrase]:
        """Finds all top level phrases in the sentence string"""
        phrases = re.findall(r"\[(\w+ [^\[\]]+(?:\[[^\[\]]+\][^\[\]]*)*)\]", input_str)
        logger.debug(
            f"Found {len(phrases)} top level phrases in input string: {input_str}"
        )
        return [self._parse_phrase(phrase) for phrase in phrases]

    def _parse_phrase(self, phrase_str: str) -> Phrase:
        label, content = phrase_str.split(maxsplit=1)
        phrase = Phrase(label)
        for match in re.finditer(r"\[(.*?)\]|\b(\S+)\s+(\S+)\b", content):
            logger.debug(f"Found match: {match.group(0)}")
            if match.group(1):
                child_phrase = self._parse_phrase(match.group(1))
                phrase.add_child(child_phrase)
            else:
                word, tag = match.group(2), match.group(3)
                phrase.add_child(TerminalNode(word, tag))
        return phrase

    def __str__(self):
        return " ".join(str(phrase) for phrase in self.phrases)

    def __repr__(self):
        return f"[{self.__str__()}]"
