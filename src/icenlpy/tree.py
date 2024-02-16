import re
import logging
import string

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


class PunctuationNode(TerminalNode):
    """A specialized representation for punctuation in the phrase structure."""

    def __init__(self, punctuation: str, tag: str = "punct"):
        # Initialize the base class with the punctuation as both the word and tag
        super().__init__(punctuation, tag)

    def __repr__(self):
        # Adjust the representation to clearly indicate this is a punctuation node
        return f"PunctuationNode({self.word})"


class Phrase:
    """A phrase in a parsed sentence"""

    def __init__(
        self: TPhrase,
        label: str,
        elements: Union[List[Union[TerminalNode, TPhrase]], None] = None,
    ):
        self.label = label
        self.elements = []
        logger.debug(f"Creating phrase with label {label}")
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


TopLevelElement = Union[Phrase, PunctuationNode]


class IceNLPySentence:

    def __init__(self, input_data):
        if isinstance(input_data, str):
            self.top_level_elements: List[TopLevelElement] = self._parse_from_string(
                input_data.strip()
            )
        elif all(isinstance(p, Phrase) for p in input_data):
            self.top_level_elements: List[TopLevelElement] = input_data
        else:
            raise ValueError("Input must be a string or a list of Phrase objects")
        self.phrases = [el for el in self.top_level_elements if isinstance(el, Phrase)]

    def _parse_from_string(self, input_str: str) -> List[TopLevelElement]:
        stack = []
        found = []
        current_element = ""
        i = 0
        logger.debug(f"Parsing input string: {input_str}")
        while i < len(input_str):
            char = input_str[i]
            if char == "[":  # Start of a phrase
                current_element += char
                stack.append(char)
            elif char == "]":  # End of a phrase
                stack.pop()
                current_element += char
                if not stack:  # End of top-level phrase
                    found.append(self._parse_element(current_element))
                    current_element = ""
            elif not stack:
                # Check for ", ," pattern
                if (
                    char in string.punctuation
                    and i + 2 < len(input_str)
                    and input_str[i + 1] == " "
                    and input_str[i + 2] == char
                ):
                    if current_element:  # Add any pending phrase
                        found.append(self._parse_element(current_element))
                        current_element = ""
                    # Capture the pattern and advance the index
                    found.append(PunctuationNode(char, char))
                    i += 2  # Skip the next two characters
                # Check for ", pX" pattern
                elif (
                    char in string.punctuation
                    and i + 3 < len(input_str)
                    and input_str[i + 1] == " "
                    and input_str[i + 2] == "p"
                    and input_str[i + 3] in "lkga"
                ):
                    if current_element:
                        found.append(self._parse_element(current_element))
                        current_element = ""
                    # Capture the pattern and advance the index
                    found.append(PunctuationNode(char, input_str[i + 1 : i + 4]))
                    i += 3  # Skip the next three characters
            else:  # Accumulate characters
                current_element += char

            i += 1
        # Add any remaining element
        if current_element:
            logger.debug(f"Adding remaining element: {current_element}")
            found.append(self._parse_element(current_element))
        return found

    def _parse_element(self, element: str) -> TopLevelElement:
        logger.debug(f"Parsing element: '{element}'")
        if element.strip().startswith("["):
            return self._parse_phrase(element)
        else:
            return PunctuationNode(*element.split())

    def _parse_phrase(self, phrase_str: str) -> Phrase:
        phrase_stack = []
        current_element = ""
        current_label = ""
        elements = []

        label, content = phrase_str.split(maxsplit=1)
        phrase = Phrase(label.strip("["))
        content = content.strip("]")
        i = 0

        while i < len(content):
            char = content[i]

            if char == "[":
                if not phrase_stack:  # Start of a new element
                    current_label = i
                phrase_stack.append(char)
            elif char == "]":
                phrase_stack.pop()
                if not phrase_stack:  # End of a nested phrase
                    nested_phrase_str = content[current_label : i + 1]
                    elements.append(nested_phrase_str)
                    current_element = ""
            else:
                if not phrase_stack:  # Accumulating characters for a terminal node
                    current_element += char

            if not phrase_stack and (char == " " or i == len(content) - 1):
                # Handling a terminal node outside nested phrases
                if current_element.strip() and len(current_element.split()) == 2:
                    elements.append(current_element.strip())
                    current_element = ""

            i += 1

        # Process accumulated elements
        for element in elements:
            if element.startswith("["):
                phrase.add_child(self._parse_phrase(element[1:-1]))
            else:
                word, tag = element.split(maxsplit=1)
                phrase.add_child(TerminalNode(word, tag))

        return phrase

    def __str__(self):
        return " ".join(str(el) for el in self.top_level_elements)

    def __repr__(self):
        return f"[{self.__str__()}]"
