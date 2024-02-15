import shlex
import subprocess
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

ICENLP_CLASS_MAP = {
    "tagger": "RunIceTagger",
    "parser": "RunIceParser",
}


def call_icenlp_jar(jar_path: str, target: str, input_text: str):
    jar_class_target = ICENLP_CLASS_MAP[target]
    java_command = f"java -classpath {shlex.quote(jar_path)} is.iclt.icenlp.runner.{jar_class_target} "

    logger.debug(f"Running {jar_class_target} with command: {java_command}")

    process = subprocess.Popen(
        java_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )

    output, errors = process.communicate(input=input_text)

    if process.returncode != 0:
        logger.error(f"{jar_class_target} Error: {errors}")
        raise Exception(f"{jar_class_target} Error: {errors}")

    return output


def get_ice_nlp_path():
    """Get the path to the IceNLP directory."""
    # Assuming this function is in a file at the root of the icenlpy package
    package_dir = Path(__file__).parent.parent
    ice_nlp_dir = package_dir / "resources/IceNLP/"
    return ice_nlp_dir.resolve()
