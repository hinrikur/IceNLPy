import sys
import logging
from pathlib import Path
from os.path import exists

logger = logging.getLogger(__name__)

try:
    package_dir = Path(__file__).parent
    ice_nlp_dir = package_dir / "resources/IceNLP/"
    jar_path = ice_nlp_dir / "dist/IceNLPCore.jar"
    jar_path = jar_path.resolve()
    assert exists(jar_path)
    JAR_PATH = str(jar_path)
    JAR_FOUND = True
    logger.debug(f"IceNLP JAR file is located at: {JAR_PATH}")
except Exception as e:
    logger.error(f"Failed to locate IceNLPCore.jar within the icenlpy package: {e}")
    JAR_PATH = None
    JAR_FOUND = False
