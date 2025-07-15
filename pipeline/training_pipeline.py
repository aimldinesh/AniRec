# Import helper to read YAML configs
from utils.common_functions import read_yaml

# Import all paths used in the project
from config.paths_config import *

# Import core components of the pipeline
from src.data_processing import DataProcessor
from src.model_training import ModelTraining

import logging

logging.basicConfig(level=logging.INFO)


# Pipeline Execution
if __name__ == "__main__":
    try:
        logging.info("Starting Data Processing...")
        data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
        data_processor.run()

        logging.info("Starting Model Training...")
        model_trainer = ModelTraining(PROCESSED_DIR)
        model_trainer.train_model()

        logging.info("✅ Pipeline completed successfully!")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}")
