import subprocess
import shlex
import tomlkit
import json
import os
import logging

from typing import List

import utils


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ice_nlp_path = utils.get_ice_nlp_path()
jar_path = ice_nlp_path / "dist/IceNLPCore.jar"

abs_path_to_icenlp_jar = os.path.join(ice_nlp_path, jar_path)


def run_iceparser(jar_path, input_text, legacy_tagger=False):
    """
    Runs the IceParser Java application with the given input text and JAR path.

    :param jar_path: Path to the IceNLPCore.jar file.
    :param input_text: Text to parse.
    :param output_format: The desired output format ('json' or 'xml').
    :return: The output from IceParser.
    """

    if legacy_tagger:
        tagged = utils.call_icenlp_jar(jar_path, "tagger", input_text)
        logger.debug(f"IceTagger output: {tagged}")
    else:
        tagged = input_text
        logger.debug(f"Tagged input: {tagged}")

    parsed_output = utils.call_icenlp_jar(jar_path, "parser", tagged)

    logger.debug(f"IceParser output: {parsed_output}")

    return parsed_output


def parse_text(input_text: List[str], legacy_tagger=False, rainbow=False):
    """
    Parses the given text using IceParser and returns the output in the specified format.

    :param input_text: The text to parse.
    :param output_format: The desired output format ('json' or 'xml').
    :return: Parsed output from IceParser.
    """

    parsed_sents = [
        run_iceparser(abs_path_to_icenlp_jar, sent, legacy_tagger=legacy_tagger)
        for sent in input_text
    ]

    return parsed_sents
