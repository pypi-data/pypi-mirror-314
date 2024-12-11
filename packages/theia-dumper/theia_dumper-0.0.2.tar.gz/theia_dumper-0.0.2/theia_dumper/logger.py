"""Logging stuff."""
import logging
import sys
import os
logging.basicConfig(format='%(levelname)s:%(message)s', level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout)
logger = logging.getLogger(__name__)
