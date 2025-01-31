# This is an initial test of logging to GCP. It does not work from DaplaLab yet.
import logging

import google.cloud.logging

from config.config import settings


# Initialize the Cloud Logging client
client = google.cloud.logging.Client(project=settings.gcp_project_id)
client.setup_logging()

logger = logging.getLogger("my_logger")
logger.warning("Test of python logging from DaplaLab, Arne")
