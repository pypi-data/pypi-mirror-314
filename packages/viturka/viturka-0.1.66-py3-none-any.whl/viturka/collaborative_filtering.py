import pandas as pd
from surprise import SVDpp, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split

class SVDPPModel:
    def __init__(self, n_epochs=20, lr_all=0.005, reg_all=0.02):
        """
        Initialize the SVD++ model with specified hyperparameters.

        :param n_epochs: Number of epochs for training.
        :param lr_all: Learning rate for all parameters.
        :param reg_all: Regularization term for all parameters.
        """
        self.model = SVDpp(n_epochs=n_epochs, lr_all=lr_all, reg_all=reg_all)

    def preprocess_data(self, csv_path, user_col, item_col, rating_col):
        """
        Preprocess the data to prepare it for training.

        :param csv_path: Path to the CSV file.
        :param user_col: Name of the user ID column.
        :param item_col: Name of the item ID column.
        :param rating_col: Name of the rating column.
        :return: Surprise Dataset object.
        """
        # Load the CSV file
        data = pd.read_csv(csv_path)

        # Ensure required columns are present
        if not all(col in data.columns for col in [user_col, item_col, rating_col]):
            raise ValueError("CSV file must contain user, item, and rating columns.")

        # Rename columns for Surprise compatibility
        data = data[[user_col, item_col, rating_col]]
        data.columns = ['userID', 'itemID', 'rating']

        # Define the reader for Surprise
        reader = Reader(rating_scale=(data['rating'].min(), data['rating'].max()))

        # Load the data into Surprise format
        dataset = Dataset.load_from_df(data[['userID', 'itemID', 'rating']], reader)
        return dataset

    def train_model(self, dataset):
        """
        Train the SVD++ model using the training set.

        :param dataset: Surprise Dataset object.
        """
        # Split the dataset into training and test sets
        trainset, testset = train_test_split(dataset, test_size=0.2)

        # Train the model on the training set
        self.model.fit(trainset)

        # Store the test set for evaluation
        self.testset = testset

    def evaluate_model(self):
        """
        Evaluate the trained model on the test set.

        :return: Dictionary of evaluation metrics.
        """
        if not hasattr(self, 'testset'):
            raise ValueError("Model must be trained before evaluation.")

        # Predict ratings for the test set
        predictions = self.model.test(self.testset)

        # Calculate evaluation metrics
        metrics = {
            'RMSE': accuracy.rmse(predictions, verbose=False),
            'MAE': accuracy.mae(predictions, verbose=False)
        }
        return metrics

# Example usage
if __name__ == "__main__":
    # Initialize the model
    svdpp_model = SVDPPModel(n_epochs=20, lr_all=0.005, reg_all=0.02)

    # Preprocess the dataset
    dataset = svdpp_model.preprocess_data(
        csv_path="ratings.csv",
        user_col="user_id",
        item_col="item_id",
        rating_col="rating"
    )

    # Train the model
    svdpp_model.train_model(dataset)

    # Evaluate the model
    metrics = svdpp_model.evaluate_model()
    print("Evaluation Metrics:", metrics)
