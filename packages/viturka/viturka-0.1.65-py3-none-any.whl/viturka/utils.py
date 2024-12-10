import pandas as pd

def combine_dat_files_general(ratings_file, users_file, items_file, output_file,
                              ratings_columns, users_columns, items_columns,
                              user_id_col, item_id_col):
    """
    Combines ratings, users, and items .dat files into a single CSV file with customizable column names.

    Parameters:
    - ratings_file (str): Path to the ratings file.
    - users_file (str): Path to the users file.
    - items_file (str): Path to the items file.
    - output_file (str): Path to save the combined CSV file.
    - ratings_columns (list of str): Column names for the ratings dataset.
    - users_columns (list of str): Column names for the users dataset.
    - items_columns (list of str): Column names for the items dataset.
    - user_id_col (str): Name of the column in all datasets that represents the user ID.
    - item_id_col (str): Name of the column in all datasets that represents the item ID.

    Returns:
    - None
    """
    try:
        # Load ratings file
        ratings = pd.read_csv(
            ratings_file,
            delimiter="::",
            header=None,
            names=ratings_columns,
            engine="python"
        )

        # Load users file
        users = pd.read_csv(
            users_file,
            delimiter="::",
            header=None,
            names=users_columns,
            engine="python"
        )

        # Load items file
        items = pd.read_csv(
            items_file,
            delimiter="::",
            header=None,
            names=items_columns,
            engine="python"
        )

        # Merge datasets: ratings + users
        ratings_users = pd.merge(ratings, users, on=user_id_col)

        # Merge the result with items
        combined_data = pd.merge(ratings_users, items, on=item_id_col)

        # Save the combined data to a CSV file
        combined_data.to_csv(output_file, index=False)

        print(f"Combined dataset saved to: {output_file}")
    except Exception as e:
        print(f"Error combining datasets: {e}")
