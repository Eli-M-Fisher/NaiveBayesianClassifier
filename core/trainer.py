from core.logger import logger


class Trainer:
    def __init__(self, model):
        """
        Receives a model instance with a 'train' method.
        """
        self.model = model

    def train(self, train_df):
        """
        Trains the model using the provided training DataFrame.
        """
        if train_df is None or train_df.empty:
            logger.warning("Training data is empty or None. Training aborted.")
            raise ValueError("Cannot train model: training data is missing.")

        logger.info("Starting model training...")
        self.model.train(train_df)
        logger.info("Model training completed.")
