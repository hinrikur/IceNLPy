import subprocess
import shlex
import tomlkit
import json
import os
import logging
import logging.config

from typing import List

import icenlpy.utils as utils

from icenlpy import JAR_PATH, JAR_FOUND


# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# ice_nlp_path = utils.get_ice_nlp_path()
# logger.debug(f"ice_nlp_path: {ice_nlp_path}")
# jar_path = ice_nlp_path / "dist/IceNLPCore.jar"

# abs_path_to_icenlp_jar = os.path.join(ice_nlp_path, jar_path)

logger.debug(f"jar_path: {JAR_PATH}")


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
        run_iceparser(JAR_PATH, sent, legacy_tagger=legacy_tagger)
        for sent in input_text
    ]

    return parsed_sents
