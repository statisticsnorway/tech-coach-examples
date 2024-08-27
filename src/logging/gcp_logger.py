import logging

import google.cloud.logging
from dapla import AuthClient


credentials = AuthClient.fetch_google_credentials()

# Cloud Logging handler
client = google.cloud.logging.Client(project="tech-coach-p-ku", credentials=credentials)
# cloud_handler = CloudLoggingHandler(client)
client.setup_logging()

logging.warning("This is a test log messagage from python!")
