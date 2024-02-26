import subprocess
import shlex
import tomlkit
import json
import os
import logging

from icenlpy import JAR_PATH, JAR_FOUND

from typing import List, Union

import icenlpy.utils as utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ice_nlp_path = utils.get_ice_nlp_path()
# jar_path = ice_nlp_path / "dist/IceNLPCore.jar"

# abs_path_to_icenlp_jar = os.path.join(ice_nlp_path, jar_path)

logger.debug(f"jar_path: {JAR_PATH}")


def run_tokenizer(jar_path, input_text, legacy_tagger=False, java_args={}):
    """
    Runs the Tokenizer Java application with the given input text and JAR path.

    :param jar_path: Path to the IceNLPCore.jar file.
    :param input_text: Text to parse.
    :param output_format: The desired output format ('json' or 'xml').
    :return: The output from tokenizer.
    """
    logger.debug(f"Running Tokenizer with input: {input_text}")

    tokens = utils.call_icenlp_jar(
        jar_path, "tokenizer", input_text, java_args=java_args
    )
    logger.debug(f"Tokenizer output: {tokens}")

    return tokens


def tokenize(
    input_text: Union[List[str], str],
    args={"of": 2},
):
    """
    Parses the given text using IceParser and returns the output in the specified format.

    :param input_text: The text to parse. The standard format is a list of strings, where each string is a sentence.
    :param output_format: The desired output format ('json' or 'xml').
    :return: Parsed output from IceParser.
    """
    text = "\n".join(input_text) if isinstance(input_text, list) else input_text
    tokenized_text = run_tokenizer(JAR_PATH, text, java_args=args)
    # for each sentence, return a generator of tokens
    return (
        (token for token in sentence.split())
        for sentence in tokenized_text.strip().split("\n")
    )


def split_into_sentences(text: str) -> List[str]:
    """
    Splits the given text into sentences using IceNLP's sentence splitter.

    :param text: The text to split into sentences.
    :return: A list of sentences.
    """
    return (
        utils.call_icenlp_jar(JAR_PATH, "tokenizer", text, java_args={"of": 2})
        .strip()
        .split("\n")
    )
