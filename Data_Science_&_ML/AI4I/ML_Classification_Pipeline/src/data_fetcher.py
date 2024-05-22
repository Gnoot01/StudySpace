import os
import sqlite3
import polars as pl


class DataFetcher:
    def __init__(self, db_path: str = "data/calls.db"):
        """
        Initializes the object with data loaded from a SQLite database.

        Parameters:
        - db_path (str, optional): Path to the SQLite database file. Defaults to "data/calls.db".

        Attributes:
        - df (pl.DataFrame): A Polars DataFrame containing the data loaded from the database.
        - validation_scores (dict): Dictionary to store validation scores of models.
        - test_scores (dict): Dictionary to store test scores of models.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_db_path = os.path.join(script_dir, db_path)
        with sqlite3.connect(full_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM calls')
            column_names = [description[0]
                            for description in cursor.description]
            rows = cursor.fetchall()
            self.df = pl.DataFrame(rows, schema=column_names)

    def get_dataframe(self):
        return self.df
