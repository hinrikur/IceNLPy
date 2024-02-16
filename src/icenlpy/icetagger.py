import subprocess
import shlex
import tomlkit
import json
import os
import logging

from icenlpy import JAR_PATH, JAR_FOUND

from typing import List

import icenlpy.utils as utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ice_nlp_path = utils.get_ice_nlp_path()
# jar_path = ice_nlp_path / "dist/IceNLPCore.jar"

# abs_path_to_icenlp_jar = os.path.join(ice_nlp_path, jar_path)

logger.debug(f"jar_path: {JAR_PATH}")


def run_icetagger(jar_path, input_text, legacy_tagger=False, java_args={}):
    """
    Runs the IceParser Java application with the given input text and JAR path.

    :param jar_path: Path to the IceNLPCore.jar file.
    :param input_text: Text to parse.
    :param output_format: The desired output format ('json' or 'xml').
    :return: The output from IceParser.
    """

    tagged = utils.call_icenlp_jar(jar_path, "tagger", input_text, java_args=java_args)
    logger.debug(f"IceTagger output: {tagged}")

    logger.debug(f"IceTagger output: {tagged}")

    return tagged


def tag_text(input_text: List[str], legacy_tagger=True):
    """
    Parses the given text using IceParser and returns the output in the specified format.

    :param input_text: The text to parse.
    :param output_format: The desired output format ('json' or 'xml').
    :return: Parsed output from IceParser.
    """

    tagged_sents = [
        run_icetagger(JAR_PATH, sent, legacy_tagger=legacy_tagger)
        for sent in input_text
    ]
    return tagged_sents
