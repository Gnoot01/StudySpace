from data_fetcher import DataFetcher
from utils.scaling import scale
from utils.encoding import encode
from sklearn.model_selection import train_test_split
import polars as pl


class Preprocessor:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.df = self.fetcher.get_dataframe()

    def preprocess(self) -> tuple:
        # Modification
        self.df = self.df.with_columns(
            pl.col('Call Duration').abs().alias('Call Duration'))
        self.df = self.df.with_columns(
            pl.col('Financial Loss').abs().alias('Financial Loss'))
        self.df = self.df.with_columns(pl.col('Call Type').map_elements(
            lambda x: 'WhatsApp' if x == 'Whats App' else x, return_dtype=pl.String).alias('Call Type'))
        self.df = self.df.with_columns(pl.col(["Flagged by Carrier", "Is International",
                                       "Country Prefix", "Call Type", "Scam Call"]).cast(pl.String).cast(pl.Categorical))

        # Removing duplicates
        self.df = self.df.unique(keep="first")

        # Imputation
        self.df = self.df.with_columns(
            pl.col('Financial Loss').fill_null(
                self.df['Financial Loss'].mean()).alias('Financial Loss')
        )

        # Removing features with low correlation
        self.df = self.df.select(pl.all().exclude(
            ["ID", "Timestamp", "Device Battery"]))

        # Splitting into 64% train, 16% validation, 20% test set
        X_train_validate, X_test, y_train_validate, y_test = train_test_split(
            self.df.select(pl.all().exclude("Scam Call")),
            self.df.select(pl.col("Scam Call")),
            test_size=0.2,
            random_state=1
        )

        X_train, X_validate, y_train, y_validate = train_test_split(
            X_train_validate, y_train_validate, test_size=0.2, random_state=1
        )

        X_train, X_validate, X_test = scale(X_train, X_validate, X_test)
        X_train, X_validate, X_test, y_train, y_validate, y_test = encode(
            X_train, X_validate, X_test, y_train, y_validate, y_test,
            ["Is International", "Scam Call"],
            ["Flagged by Carrier", "Country Prefix", "Call Type"]
        )

        X_train = X_train.to_pandas()
        X_validate = X_validate.to_pandas()
        X_test = X_test.to_pandas()
        y_train = y_train.to_pandas()
        y_validate = y_validate.to_pandas()
        y_test = y_test.to_pandas()

        return X_train, X_validate, X_test, y_train, y_validate, y_test
