import polars as pl
from sklearn.preprocessing import StandardScaler


def scale(X_train: pl.DataFrame, X_validate: pl.DataFrame, X_test: pl.DataFrame):
    # Scale validation and test set with offsets from training set
    # Scaling features equal significance in training set, prevents dominance of a singular feature
    # Preserves same shape after.
    scaler = StandardScaler()
    numerical_columns = [
        col for col in X_train.columns if X_train[col].dtype in [pl.Float64, pl.Int64]]

    X_train_scaled = scaler.fit_transform(
        X_train.select(numerical_columns).to_numpy())
    X_validate_scaled = scaler.transform(
        X_validate.select(numerical_columns).to_numpy())
    X_test_scaled = scaler.transform(
        X_test.select(numerical_columns).to_numpy())

    X_train_scaled_df = pl.DataFrame(X_train_scaled, schema=numerical_columns)
    X_validate_scaled_df = pl.DataFrame(
        X_validate_scaled, schema=numerical_columns)
    X_test_scaled_df = pl.DataFrame(X_test_scaled, schema=numerical_columns)

    # Drop the original numerical columns
    X_train = X_train.drop(numerical_columns).hstack(X_train_scaled_df)
    X_validate = X_validate.drop(
        numerical_columns).hstack(X_validate_scaled_df)
    X_test = X_test.drop(numerical_columns).hstack(X_test_scaled_df)

    return X_train, X_validate, X_test
