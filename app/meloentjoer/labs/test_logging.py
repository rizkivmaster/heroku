import logging

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
logger.info("INFO")
logger.debug("DEBUG")
