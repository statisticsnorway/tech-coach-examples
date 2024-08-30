import logging

import google.cloud.logging
from dapla import AuthClient


credentials = AuthClient.fetch_google_credentials()
client = google.cloud.logging.Client(
    project="dev-tech-coach-6cc5", credentials=credentials
)

# This works in a google cloud shell
# client = google.cloud.logging.Client()
client.setup_logging()
logging.warning("Test of python logging from local PC, Arne")

logger = logging.getLogger(__name__)
logger.warning("Test of python logging from local PC, standard python logging, Arne")
