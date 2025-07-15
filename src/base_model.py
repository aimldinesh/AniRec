from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Embedding,
    Dot,
    Flatten,
    Dense,
    Activation,
    BatchNormalization,
)
from utils.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

# Set up a logger instance for tracking events
logger = get_logger(__name__)


class BaseModel:
    def __init__(self, config_path):
        """
        Initialize BaseModel by loading configurations from a YAML file.

        Args:
        - config_path (str): Path to the configuration YAML file.
        """
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded configuration from config.yaml")
        except Exception as e:
            raise CustomException("Error loading configuration", e)

    def RecommenderNet(self, n_users, n_anime):
        """
        Constructs and compiles a collaborative filtering model using dot-product
        of user and item embeddings.

        Args:
        - n_users (int): Total number of unique users
        - n_anime (int): Total number of unique anime

        Returns:
        - Compiled Keras model
        """
        try:
            # Get embedding size from config
            embedding_size = self.config["model"]["embedding_size"]

            # User input layer
            user = Input(name="user", shape=[1])

            # User embedding layer
            user_embedding = Embedding(
                name="user_embedding", input_dim=n_users, output_dim=embedding_size
            )(user)

            # Anime input layer
            anime = Input(name="anime", shape=[1])

            # Anime embedding layer
            anime_embedding = Embedding(
                name="anime_embedding", input_dim=n_anime, output_dim=embedding_size
            )(anime)

            # Dot product of user and anime embeddings (shape becomes [batch_size, 1, 1])
            x = Dot(name="dot_product", normalize=True, axes=2)(
                [user_embedding, anime_embedding]
            )

            # Flatten the dot product result
            x = Flatten()(x)

            # Dense layer for prediction
            x = Dense(1, kernel_initializer="he_normal")(x)

            # Normalize and activate the output
            x = BatchNormalization()(x)
            x = Activation("sigmoid")(x)  # Predicts between 0 and 1

            # Create the final model
            model = Model(inputs=[user, anime], outputs=x)

            # Compile the model with configuration parameters
            model.compile(
                loss=self.config["model"]["loss"],
                optimizer=self.config["model"]["optimizer"],
                metrics=self.config["model"]["metrics"],
            )

            logger.info("Model created successfully....")
            return model

        except Exception as e:
            logger.error(f"Error occurred during model architecture creation: {e}")
            raise CustomException("Failed to create model", e)
