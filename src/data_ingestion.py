# Import necessary libraries
import os
import pandas as pd
from google.cloud import storage

# Custom modules for logging and exceptions
from src.logger import get_logger
from src.custom_exception import CustomException

# Project paths and utility functions
from config.paths_config import *
from utils.common_functions import read_yaml

# Initialize logger
logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        # Load config for data ingestion
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_names"]

        # Create raw data directory if it doesn't exist
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("Data Ingestion Started....")

    def download_csv_from_gcp(self):
        """
        Downloads specified CSV files from a GCP bucket into the RAW_DIR.
        For animelist.csv (large file), only 5 million rows are downloaded.
        """
        try:
            # Create GCP storage client and get the bucket
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            # Loop through each file to download
            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)

                # Special handling for large file
                if file_name == "animelist.csv":
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    # Read and save only 5M rows to reduce memory
                    data = pd.read_csv(file_path, nrows=5000000)
                    data.to_csv(file_path, index=False)
                    logger.info("Large file detected. Only downloading 5M rows.")
                else:
                    # Download smaller files normally
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)
                    logger.info(
                        "Downloading smaller files: anime & anime_with_synopsis"
                    )

        except Exception as e:
            logger.error("Error while downloading data from GCP")
            # Raise custom exception for traceability
            raise CustomException("Failed to download data", e)

    def run(self):
        """
        Entry point for data ingestion process.
        """
        try:
            logger.info("Starting Data Ingestion Process....")
            self.download_csv_from_gcp()
            logger.info("Data Ingestion Completed...")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        finally:
            logger.info("Data Ingestion DONE...")


# Execute when script is run directly
if __name__ == "__main__":
    # Read config file and initiate ingestion process
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
