import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix, hstack, csc_matrix
from fastFM import als
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.linear_model import LinearRegression

def handle_missing_values(df, drop_threshold=0.3, fill_threshold=0.7, advanced_imputation=None):
    """
    Handles missing values in a DataFrame by dropping or imputing columns based on the percentage of NaN values.
    Includes options for KNN or Regression-based imputation for numerical features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        drop_threshold (float): Percentage of missing values above which columns are dropped (default: 0.7).
        fill_threshold (float): Percentage of missing values below which columns are imputed (default: 0.3).
        advanced_imputation (str or None): Type of advanced imputation for numerical features ('knn', 'regression', or None).

    Returns:
        pd.DataFrame: A DataFrame with missing values handled.
    """
    df_cleaned = df.copy()
    missing_percentages = df_cleaned.isna().mean()

    # Drop columns with missing values above the drop_threshold
    to_drop = missing_percentages[missing_percentages > drop_threshold].index
    df_cleaned = df_cleaned.drop(columns=to_drop)
    print(f"Dropped columns: {list(to_drop)}")

    # Handle remaining columns
    for column in df_cleaned.columns:
        missing_percentage = missing_percentages[column]
        if 0 < missing_percentage <= fill_threshold:
            if df_cleaned[column].dtype in ['float64', 'int64']:
                # Use mean or median based on skewness
                skewness = df_cleaned[column].skew()
                strategy = 'median' if abs(skewness) > 1 else 'mean'
                imputer = SimpleImputer(strategy=strategy)
                df_cleaned[column] = imputer.fit_transform(df_cleaned[[column]])
                print(f"Imputed column '{column}' using {imputer.strategy}.")
            else:
                # Use mode for categorical data
                imputer = SimpleImputer(strategy='most_frequent')
                df_cleaned[column] = imputer.fit_transform(df_cleaned[[column]]).ravel()
                print(f"Imputed column '{column}' using most_frequent strategy.")
        elif fill_threshold < missing_percentage <= drop_threshold:
            if df_cleaned[column].dtype in ['float64', 'int64'] and advanced_imputation:
                if advanced_imputation == "knn":
                    print(f"Imputing column '{column}' using KNNImputer.")
                    knn_imputer = KNNImputer(n_neighbors=5)
                    df_cleaned[column] = knn_imputer.fit_transform(df_cleaned[[column]])
                elif advanced_imputation == "regression":
                    print(f"Imputing column '{column}' using Regression Imputation.")
                    df_cleaned = _regression_imputation(df_cleaned, column)
            else:
                # Use mode for categorical data
                imputer = SimpleImputer(strategy='most_frequent')
                df_cleaned[column] = imputer.fit_transform(df_cleaned[[column]]).ravel()
                print(f"Imputed column '{column}' using most_frequent strategy.")

    return df_cleaned


def _regression_imputation(df, target_column):
    """
    Performs regression-based imputation for a column with missing values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the column to be imputed.
        target_column (str): The column to be imputed.

    Returns:
        pd.DataFrame: The DataFrame with the target column imputed.
    """
    # Separate rows with and without missing values in the target column
    missing_rows = df[df[target_column].isna()]
    complete_rows = df[~df[target_column].isna()]

    # Separate features and target
    X_complete = complete_rows.drop(columns=[target_column])
    y_complete = complete_rows[target_column]
    X_missing = missing_rows.drop(columns=[target_column])

    # Drop columns with NaNs in features
    X_complete = X_complete.dropna(axis=1)
    X_missing = X_missing[X_complete.columns]

    # If sufficient features are available for regression
    if not X_complete.empty and not X_missing.empty:
        # Train a regression model
        model = LinearRegression()
        model.fit(X_complete, y_complete)

        # Predict missing values
        predicted_values = model.predict(X_missing)
        df.loc[missing_rows.index, target_column] = predicted_values
        print(f"Regression imputed column '{target_column}' with {len(predicted_values)} values.")

    return df

def correlation_matrix(file, selected_columns):
    df = pd.read_csv(file).dropna()
    data = df[selected_columns]
    correlation_matrix = data.corr()

    # Plot the correlation matrix using seaborn
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix of Selected Features')
    plt.show()

def find_similar_items(model, dict_vectorizer, item_features, item_id, item_id_column, numerical_columns, categorical_columns, top_k=5):
    # Validate the item exists
    if item_id not in item_features[item_id_column].values:
        raise ValueError(f"Item ID {item_id} not found in the dataset.")

    # Combine categorical and numerical features
    categorical_features = dict_vectorizer.transform(item_features[categorical_columns].to_dict(orient="records"))
    numerical_features = csc_matrix(item_features[numerical_columns].values)

    # Concatenate features
    item_matrix = hstack([categorical_features, numerical_features])
    item_matrix = csc_matrix(item_matrix)  # Convert to CSC format

    # Derive item latent vectors
    item_latent_vectors = item_matrix @ model.V_.T

    # Find the index of the item
    item_index = item_features[item_features[item_id_column] == item_id].index[0]

    # Compute cosine similarity
    item_latent_vector = item_latent_vectors[item_index].reshape(1, -1)
    similarities = cosine_similarity(item_latent_vector, item_latent_vectors).flatten()

    # Retrieve top-k similar items
    similar_indices = similarities.argsort()[::-1][:top_k + 1]  # Include itself
    similar_items = [
        (item_features.iloc[i][item_id_column], similarities[i]) for i in similar_indices if i != item_index
    ]

    return similar_items[:top_k]


def train_model(
    file,
    target_column,
    numerical_columns,
    categorical_columns,
    item_id_column,
    n_iter=100,
    rank=8,
    init_stdev=0.01,
    step_size=0.01,
    l2_reg_w=0.001,
    l2_reg_V=0.001,
    test_size=0.2,
    vectorizer=None,
):
    """
    Train a factorization machine (FM) model on any dataset.

    Args:
        file (str): Path to the CSV file containing the dataset.
        target_column (str): Name of the target column.
        numerical_columns (list): List of numerical feature columns.
        categorical_columns (list): List of categorical feature columns.
        item_id_column (str): Name of the column that uniquely identifies items.
        n_iter (int): Number of iterations for the FM model.
        rank (int): Rank of factorization.
        init_stdev (float): Standard deviation for initialization.
        step_size (float): Learning rate.
        l2_reg_w (float): Regularization parameter for weights.
        l2_reg_V (float): Regularization parameter for latent factors.
        test_size (float): Fraction of the dataset to be used as test data.
        vectorizer (DictVectorizer): Pre-trained vectorizer to transfer-train.

    Returns:
        tuple: Trained FM model, train/test data, vectorizer, target scaler, and original dataset.
    """
    # Load the dataset from CSV
    df = pd.read_csv(file)

    # Validate required columns
    required_columns = set([target_column, item_id_column] + numerical_columns + categorical_columns)
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {missing_columns}")

    # Ensure categorical columns are strings
    df[categorical_columns] = df[categorical_columns].astype(str)

    # Ensure numerical columns are floats
    df[numerical_columns] = df[numerical_columns].astype(float)

    # Process the target variable
    y = df[target_column].astype(float)
    scaler_target = MinMaxScaler()
    y_scaled = scaler_target.fit_transform(y.values.reshape(-1, 1)).flatten()

    # Scale numerical features
    scaler = MinMaxScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    # Encode categorical features using provided or new vectorizer
    if vectorizer is None:
        vectorizer = DictVectorizer(sparse=True)
        categorical_features = vectorizer.fit_transform(df[categorical_columns].to_dict(orient="records"))
    else:
        # Extract existing vocabulary
        old_vocab = set(vectorizer.feature_names_)

        # Fit a temporary vectorizer on the new data to get new vocabulary
        temp_vectorizer = DictVectorizer(sparse=True)
        temp_vectorizer.fit(df[categorical_columns].to_dict(orient="records"))
        new_vocab = set(temp_vectorizer.feature_names_)

        # Combine the old and new vocabularies
        combined_vocab = old_vocab.union(new_vocab)

        # Create a new vectorizer with the combined vocabulary
        combined_vectorizer = DictVectorizer(sparse=True)
        combined_vectorizer.fit([{key: 0 for key in combined_vocab}])

        # Transform the dataset with the combined vectorizer
        vectorizer = combined_vectorizer
        categorical_features = vectorizer.transform(df[categorical_columns].to_dict(orient="records"))

    # Combine numerical and categorical features
    numerical_features = csr_matrix(df[numerical_columns].values)
    X = hstack([categorical_features, numerical_features])
    X = MaxAbsScaler().fit_transform(X)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=test_size, random_state=42)

    # Train the FM model
    model = als.FMRegression(
        n_iter=n_iter,
        init_stdev=init_stdev,
        l2_reg_w=l2_reg_w,
        l2_reg_V=l2_reg_V,
        rank=rank,
    )
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_test, vectorizer, scaler_target, df


def evaluate_model(model, X_test, y_test, scaler_target):
    """
    Evaluate the FM model using mean squared error.

    Args:
        model: Trained FM model.
        X_test: Test feature matrix.
        y_test: Test target values.
        scaler_target: Scaler used to scale the target variable.

    Returns:
        tuple: Predicted values and mean squared error.
    """
    # Predict and inverse transform
    pred_scaled = model.predict(X_test)
    pred = scaler_target.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
    y_test = scaler_target.inverse_transform(y_test.reshape(-1, 1)).flatten()

    # Filter valid predictions
    valid_indices = ~np.isnan(y_test) & ~np.isnan(pred)
    y_test, pred = y_test[valid_indices], pred[valid_indices]

    # Compute MSE
    mse = mean_squared_error(y_test, pred)
    return pred, mse
