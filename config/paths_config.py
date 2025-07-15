import os

# ================================
# PATH CONFIGURATION FILE
# ================================

# -----------  DATA INGESTION -----------

# Directory to store raw/unprocessed input files
RAW_DIR = "artifacts/raw"

# Path to YAML config file for project-wide settings
CONFIG_PATH = "config/config.yaml"

# ----------- DATA PROCESSING -----------

# Directory where processed artifacts will be saved
PROCESSED_DIR = "artifacts/processed"

# Raw CSV file paths used for preprocessing
ANIMELIST_CSV = os.path.join(RAW_DIR, "animelist.csv")  # User-anime rating data
ANIME_CSV = os.path.join(RAW_DIR, "anime.csv")  # Anime metadata
ANIMESYNOPSIS_CSV = os.path.join(
    RAW_DIR, "anime_with_synopsis.csv"
)  # Anime synopsis data

# Processed training/testing data arrays
X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR, "X_train_array.pkl")  # Training features
X_TEST_ARRAY = os.path.join(PROCESSED_DIR, "X_test_array.pkl")  # Testing features
Y_TRAIN = os.path.join(PROCESSED_DIR, "y_train.pkl")  # Training labels
Y_TEST = os.path.join(PROCESSED_DIR, "y_test.pkl")  # Testing labels

# Processed cleaned dataframes
RATING_DF = os.path.join(
    PROCESSED_DIR, "rating_df.csv"
)  # Scaled & filtered rating data
DF = os.path.join(PROCESSED_DIR, "anime_df.csv")  # Cleaned anime metadata
SYNOPSIS_DF = os.path.join(PROCESSED_DIR, "synopsis_df.csv")  # Cleaned anime synopsis

# Mapping dictionaries for user and anime encodings (needed for embeddings)
USER2USER_ENCODED = os.path.join(
    PROCESSED_DIR, "user2user_encoded.pkl"
)  # Map user_id → encoded id
USER2USER_DECODED = os.path.join(
    PROCESSED_DIR, "user2user_decoded.pkl"
)  # Map encoded id → user_id
ANIME2ANIME_ENCODED = os.path.join(
    PROCESSED_DIR, "anim2anime_encoded.pkl"
)  # Map anime_id → encoded id
ANIME2ANIME_DECODED = os.path.join(
    PROCESSED_DIR, "anim2anime_decoded.pkl"
)  # Map encoded id → anime_id

# ----------- MODEL TRAINING -----------

# Directory to save final trained model
MODEL_DIR = "artifacts/model"

# Directory to store learned user/anime embedding weights
WEIGHTS_DIR = "artifacts/weights"

# Saved model file (Keras H5 format)
MODEL_PATH = os.path.join(MODEL_DIR, "model.h5")

# Extracted embedding weights
ANIME_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, "anime_weights.pkl")
USER_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, "user_weights.pkl")

# Best model weights checkpoint during training
CHECKPOINT_FILE_PATH = "artifacts/model_checkpoint/weights.weights.h5"
