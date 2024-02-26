import shlex
import subprocess
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

ICENLP_CLASS_MAP = {
    "tagger": "RunIceTagger",
    "parser": "RunIceParser",
    "tokenizer": "RunTokenizer",
}


def call_icenlp_jar(jar_path: str, target: str, input_text: str, java_args={}):
    jar_class_target = ICENLP_CLASS_MAP[target]
    # java_command = f"java -classpath {shlex.quote(jar_path)} is.iclt.icenlp.runner.{jar_class_target}"

    # logger.debug(f"Running {jar_class_target} with command: {java_command}")

    command = [
        "java",
        "-classpath",
        jar_path,
        f"is.iclt.icenlp.runner.{jar_class_target}",
    ]

    # Add arguments based on kwargs
    for arg, value in java_args.items():
        if value is True:
            # For boolean flags, just add the flag
            command.append(f"-{arg}")
        else:
            # For key-value pairs, add both the flag and its value
            command.extend([f"-{arg}", str(value)])

    logger.debug(
        f"Running {jar_class_target} with command: {' '.join(shlex.quote(part) for part in command)}"
    )

    process = subprocess.Popen(
        " ".join(command),
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
