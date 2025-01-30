import logging

import google.cloud.logging


# Initialize the Cloud Logging client
client = google.cloud.logging.Client(project="tech-coach-p-ku")
client.setup_logging()

logger = logging.getLogger("my_logger")
logger.warning("Test of python logging from DaplaLab, Arne")
