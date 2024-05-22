import polars as pl
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


def encode(X_train: pl.DataFrame, X_validate: pl.DataFrame, X_test: pl.DataFrame, y_train: pl.DataFrame, y_validate: pl.DataFrame, y_test: pl.DataFrame, binary_cols: list, multi_cols: list):
    ohe = OneHotEncoder()

    # Label encode binary columns
    for col in binary_cols:
        if col in X_train.columns:
            le_x = LabelEncoder()
            X_train = X_train.with_columns(
                pl.Series(col, le_x.fit_transform(X_train[col].to_list())))
            X_validate = X_validate.with_columns(
                pl.Series(col, le_x.transform(X_validate[col].to_list())))
            X_test = X_test.with_columns(
                pl.Series(col, le_x.transform(X_test[col].to_list())))
        if col in y_train.columns:
            le_y = LabelEncoder()
            y_train = y_train.with_columns(
                pl.Series(col, le_y.fit_transform(y_train[col].to_list())))
            y_validate = y_validate.with_columns(
                pl.Series(col, le_y.transform(y_validate[col].to_list())))
            y_test = y_test.with_columns(
                pl.Series(col, le_y.transform(y_test[col].to_list())))

    # One-hot encode multi-class columns
    for col in multi_cols:
        # Reshape input data to 2D array
        train_reshape = X_train[col].to_numpy().reshape(-1, 1)
        validate_reshape = X_validate[col].to_numpy().reshape(-1, 1)
        test_reshape = X_test[col].to_numpy().reshape(-1, 1)

        # Perform one-hot encoding
        train_encoded = ohe.fit_transform(train_reshape)
        validate_encoded = ohe.transform(validate_reshape)
        test_encoded = ohe.transform(test_reshape)

        # Convert sparse matrices to dense arrays
        train_encoded_dense = train_encoded.toarray()
        validate_encoded_dense = validate_encoded.toarray()
        test_encoded_dense = test_encoded.toarray()

        # Create DataFrames from the dense arrays
        train_encoded_df = pl.DataFrame(train_encoded_dense, schema=[
                                        f"{col}_{category}" for category in ohe.categories_[0]])
        validate_encoded_df = pl.DataFrame(validate_encoded_dense, schema=[
                                           f"{col}_{category}" for category in ohe.categories_[0]])
        test_encoded_df = pl.DataFrame(test_encoded_dense, schema=[
                                       f"{col}_{category}" for category in ohe.categories_[0]])

        # Drop original column and concatenate the new one-hot encoded columns
        X_train = X_train.drop(col).hstack(train_encoded_df)
        X_validate = X_validate.drop(col).hstack(validate_encoded_df)
        X_test = X_test.drop(col).hstack(test_encoded_df)

    return X_train, X_validate, X_test, y_train, y_validate, y_test
