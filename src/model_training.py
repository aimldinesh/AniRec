# === Import required libraries ===
import os
import joblib
import comet_ml
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    LearningRateScheduler,
    EarlyStopping,
)
from src.logger import get_logger
from src.custom_exception import CustomException
from src.base_model import BaseModel
from config.paths_config import *

# === Initialize logger ===
logger = get_logger(__name__)


# === Model Training Class ===
class ModelTraining:
    def __init__(self, data_path):
        self.data_path = data_path

        # Initialize Comet ML experiment
        self.experiment = comet_ml.Experiment(
            api_key="CTIjM1CkxEf1GwKMWtcEdVBNA",
            project_name="MLOPS-AniRec",
            workspace="aimldinesh",
        )
        logger.info("✅ Model Training & Comet ML initialized.")

    def load_data(self):
        """Load training and test data arrays and targets."""
        try:
            X_train_array = joblib.load(X_TRAIN_ARRAY)
            X_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_TEST)
            logger.info("📦 Loaded training and test data.")
            return X_train_array, X_test_array, y_train, y_test
        except Exception as e:
            raise CustomException("❌ Failed to load training/test data", e)

    def train_model(self):
        """Main method: trains model, logs metrics, evaluates and saves weights."""
        try:
            # Step 1: Load training/test data
            X_train_array, X_test_array, y_train, y_test = self.load_data()

            # Step 2: Load number of unique users and animes
            n_users = len(joblib.load(USER2USER_ENCODED))
            n_anime = len(joblib.load(ANIME2ANIME_ENCODED))

            # Step 3: Create model architecture
            base_model = BaseModel(config_path=CONFIG_PATH)
            model = base_model.RecommenderNet(n_users=n_users, n_anime=n_anime)

            # Step 4: Learning rate scheduler setup
            start_lr = 0.00001
            min_lr = 0.0001
            max_lr = 0.00005
            ramup_epochs = 5
            sustain_epochs = 0
            exp_decay = 0.8
            batch_size = 10000

            def lrfn(epoch):
                if epoch < ramup_epochs:
                    return (max_lr - start_lr) / ramup_epochs * epoch + start_lr
                elif epoch < ramup_epochs + sustain_epochs:
                    return max_lr
                else:
                    return (max_lr - min_lr) * exp_decay ** (
                        epoch - ramup_epochs - sustain_epochs
                    ) + min_lr

            lr_callback = LearningRateScheduler(lambda epoch: lrfn(epoch), verbose=0)

            # Step 5: Define callbacks
            model_checkpoint = ModelCheckpoint(
                filepath=CHECKPOINT_FILE_PATH,
                save_weights_only=True,
                monitor="val_loss",
                mode="min",
                save_best_only=True,
            )

            early_stopping = EarlyStopping(
                patience=3,
                monitor="val_loss",
                mode="min",
                restore_best_weights=True,
            )

            callbacks = [model_checkpoint, lr_callback, early_stopping]

            # Step 6: Ensure necessary directories exist
            os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH), exist_ok=True)
            os.makedirs(MODEL_DIR, exist_ok=True)
            os.makedirs(WEIGHTS_DIR, exist_ok=True)

            # Step 7: Train the model
            history = model.fit(
                x=X_train_array,
                y=y_train,
                batch_size=batch_size,
                epochs=20,
                verbose=1,
                validation_data=(X_test_array, y_test),
                callbacks=callbacks,
            )

            model.load_weights(CHECKPOINT_FILE_PATH)
            logger.info("✅ Model training completed successfully.")

            # Step 8: Log train/val loss to Comet ML
            for epoch in range(len(history.history["loss"])):
                self.experiment.log_metric(
                    "train_loss", history.history["loss"][epoch], step=epoch
                )
                self.experiment.log_metric(
                    "val_loss", history.history["val_loss"][epoch], step=epoch
                )

            # Step 9: Plot and log training vs validation loss
            try:
                plt.figure(figsize=(10, 6))
                plt.plot(history.history["loss"], label="Training Loss", marker="o")
                plt.plot(
                    history.history["val_loss"], label="Validation Loss", marker="x"
                )
                plt.title("Training vs Validation Loss")
                plt.xlabel("Epochs")
                plt.ylabel("Loss")
                plt.legend()
                plt.grid(True)

                loss_plot_path = os.path.join(MODEL_DIR, "loss_plot.png")
                plt.savefig(loss_plot_path)
                plt.close()

                self.experiment.log_image(loss_plot_path, name="Loss Curve")
                logger.info(f"📊 Loss plot saved at {loss_plot_path}")
            except Exception as e:
                logger.error("❌ Failed to generate/save loss plot.")

            # Step 10: Evaluate the model
            self.evaluate_model(model, X_test_array, y_test)

            # Step 11: Save model & embeddings
            self.save_model_weights(model)

        except Exception as e:
            logger.error(str(e))
            raise CustomException("🚨 Error during model training process", e)

    def evaluate_model(self, model, X_test_array, y_test):
        """Evaluate model performance and log results."""
        try:
            results = model.evaluate(X_test_array, y_test, verbose=1)
            for metric_name, metric_value in zip(model.metrics_names, results):
                logger.info(f"{metric_name}: {metric_value:.4f}")
                self.experiment.log_metric(f"eval_{metric_name}", metric_value)
            logger.info("✅ Model evaluation completed.")
        except Exception as e:
            logger.error("❌ Error during model evaluation.")
            raise CustomException("Evaluation failed", e)

    def extract_weights(self, layer_name, model):
        """Extract and normalize embedding weights for a given layer."""
        try:
            weight_layer = model.get_layer(layer_name)
            weights = weight_layer.get_weights()[0]
            weights = weights / np.linalg.norm(weights, axis=1).reshape((-1, 1))
            logger.info(f"📤 Extracted normalized weights for {layer_name}")
            return weights
        except Exception as e:
            raise CustomException("❌ Error during weight extraction", e)

    def save_model_weights(self, model):
        """Save trained model, embedding weights, and log to Comet ML."""
        try:
            model.save(MODEL_PATH)
            logger.info(f"💾 Model saved at {MODEL_PATH}")

            user_weights = self.extract_weights("user_embedding", model)
            anime_weights = self.extract_weights("anime_embedding", model)

            joblib.dump(user_weights, USER_WEIGHTS_PATH)
            joblib.dump(anime_weights, ANIME_WEIGHTS_PATH)

            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)
            self.experiment.log_asset(ANIME_WEIGHTS_PATH)

            logger.info("✅ User and Anime weights saved and logged to Comet ML.")
        except Exception as e:
            raise CustomException("❌ Error saving model/weights", e)


# === Entry Point ===
if __name__ == "__main__":
    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()
