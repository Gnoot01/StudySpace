import sqlite3
import numpy as np
import matplotlib.pyplot as mplt
import plotly.graph_objects as go
import pandas as pd
import polars as pl
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from tensorflow.keras.regularizers import L1, L2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.nn import sigmoid
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay


class MLP:
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
        self.validation_scores = {}
        self.test_scores = {}

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
        X_train_validate, X_test, y_train_validate, y_test = train_test_split(self.df.select(pl.all(
        ).exclude("Scam Call")), self.df.select(pl.col("Scam Call")), test_size=0.2, random_state=1)

        X_train, X_validate, y_train, y_validate = train_test_split(
            X_train_validate, y_train_validate, test_size=0.2, random_state=1)

        X_train, X_validate, X_test = self.scale(X_train, X_validate, X_test)
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.encode(X_train, X_validate, X_test, y_train, y_validate, y_test, [
                                                                               "Is International", "Scam Call"], ["Flagged by Carrier", "Country Prefix", "Call Type"])
        X_train = X_train.to_pandas()
        X_validate = X_validate.to_pandas()
        X_test = X_test.to_pandas()
        y_train = y_train.to_pandas()
        y_validate = y_validate.to_pandas()
        y_test = y_test.to_pandas()
        return X_train, X_validate, X_test, y_train, y_validate, y_test

    def scale(self, X_train: pl.DataFrame, X_validate: pl.DataFrame, X_test: pl.DataFrame) -> tuple:
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

        X_train_scaled_df = pl.DataFrame(
            X_train_scaled, schema=numerical_columns)
        X_validate_scaled_df = pl.DataFrame(
            X_validate_scaled, schema=numerical_columns)
        X_test_scaled_df = pl.DataFrame(
            X_test_scaled, schema=numerical_columns)

        # Drop the original numerical columns
        X_train = X_train.drop(numerical_columns).hstack(X_train_scaled_df)
        X_validate = X_validate.drop(
            numerical_columns).hstack(X_validate_scaled_df)
        X_test = X_test.drop(numerical_columns).hstack(X_test_scaled_df)
        return X_train, X_validate, X_test

    def encode(self, X_train: pl.DataFrame, X_validate: pl.DataFrame, X_test: pl.DataFrame, y_train: pl.DataFrame, y_validate: pl.DataFrame, y_test: pl.DataFrame, binary_cols: list, multi_cols: list) -> tuple:
        ohe = OneHotEncoder()

        # Label encode binary columns
        for col in binary_cols:
            if col in X_train.columns:
                le_x = LabelEncoder()
                X_train = X_train.with_columns(
                    pl.Series(col, le_x.fit_transform(X_train[col].to_list()))
                )
                X_validate = X_validate.with_columns(
                    pl.Series(col, le_x.transform(X_validate[col].to_list()))
                )
                X_test = X_test.with_columns(
                    pl.Series(col, le_x.transform(X_test[col].to_list()))
                )
            if col in y_train.columns:
                le_y = LabelEncoder()
                y_train = y_train.with_columns(
                    pl.Series(col, le_y.fit_transform(y_train[col].to_list()))
                )
                y_validate = y_validate.with_columns(
                    pl.Series(col, le_y.transform(y_validate[col].to_list()))
                )
                y_test = y_test.with_columns(
                    pl.Series(col, le_y.transform(y_test[col].to_list()))
                )

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

    def knn(self) -> None:
        # Need to feature engineer (scale), as knn is based on distance
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = KNeighborsClassifier()
        random_search = RandomizedSearchCV(
            classifier,
            param_distributions={'n_neighbors': list(
                range(1, 10)), 'p': [1, 2]},
            n_iter=1000,
            cv=10,
            random_state=0,
            n_jobs=-1
        )
        random_search.fit(X_train, y_train)
        best_knn = random_search.best_estimator_
        y_pred_validate = best_knn.predict(X_validate)
        y_pred_test = best_knn.predict(X_test)
        print(f"Best params: {random_search.best_params_}")

        self.validation_scores["KNN"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["KNN"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (KNN)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def svm(self) -> None:
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = SVC()
        random_search = RandomizedSearchCV(
            classifier,
            param_distributions={'C': [0.5, 0.8, 1], 'kernel': [
                "linear", "poly", "rbf", "sigmoid"], 'degree': [2, 3, 4, 5]},
            n_iter=1000,
            cv=10,
            random_state=0,
            n_jobs=-1
        )
        random_search.fit(X_train, y_train)
        best_svm = random_search.best_estimator_
        y_pred_validate = best_svm.predict(X_validate)
        y_pred_test = best_svm.predict(X_test)
        print(f"Best params: {random_search.best_params_}")

        self.validation_scores["SVM"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["SVM"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (SVM)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def nb(self) -> None:
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = GaussianNB()
        random_search = RandomizedSearchCV(
            classifier,
            param_distributions={'var_smoothing': np.logspace(0, -9, num=100)},
            n_iter=1000,
            cv=10,
            random_state=0,
            n_jobs=-1
        )
        random_search.fit(X_train, y_train)
        best_nb = random_search.best_estimator_
        y_pred_validate = best_nb.predict(X_validate)
        y_pred_test = best_nb.predict(X_test)
        print(f"Best params: {random_search.best_params_}")

        self.validation_scores["Naive Bayes"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["Naive Bayes"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (Naive Bayes)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def catboost(self) -> None:
        # Training ensemble of predictors sequentially, learning from predecessor in diff methods
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = CatBoostClassifier()
        classifier.fit(X_train, y_train)
        y_pred_validate = classifier.predict(X_validate)
        y_pred_test = classifier.predict(X_test)

        self.validation_scores["Catboost"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["Catboost"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (Catboost)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def xgboost(self) -> None:
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = XGBClassifier()
        classifier.fit(X_train, y_train)
        y_pred_validate = classifier.predict(X_validate)
        y_pred_test = classifier.predict(X_test)

        self.validation_scores["XGboost"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["XGboost"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (XGboost)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def bagging(self) -> None:
        # Bagged trees
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = BaggingClassifier()
        random_search = RandomizedSearchCV(
            classifier,
            param_distributions={'n_estimators': list(range(10, 50, 5)),
                                 'max_samples': [0.2, 0.5, 0.8],
                                 'max_features': [0.2, 0.5, 0.8],
                                 'bootstrap': [True, False]},
            n_iter=1000,
            cv=10,
            random_state=0,
            n_jobs=-1
        )
        random_search.fit(X_train, y_train)
        best_bag = random_search.best_estimator_
        y_pred_validate = best_bag.predict(X_validate)
        y_pred_test = best_bag.predict(X_test)
        print(f"Best params: {random_search.best_params_}")

        self.validation_scores["Bagging"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["Bagging"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (Bagging)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def random_forest(self) -> None:
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = RandomForestClassifier()
        random_search = RandomizedSearchCV(
            classifier,
            param_distributions={'n_estimators': list(range(10, 150, 10)),
                                 'max_depth': list(range(15, 25, 2)),
                                 'min_samples_split': list(range(2, 10, 2)),
                                 'min_samples_leaf':  list(range(2, 10, 2)),
                                 'max_features': [0.2, 0.5, 0.7]},
            n_iter=1000,
            cv=10,
            random_state=0,
            n_jobs=-1
        )
        random_search.fit(X_train, y_train)
        best_rf = random_search.best_estimator_
        y_pred_validate = best_rf.predict(X_validate)
        y_pred_test = best_rf.predict(X_test)
        print(f"Best params: {random_search.best_params_}")

        self.validation_scores["Random Forest"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["Random Forest"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (Random Forest)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def voting_ensemble(self) -> None:
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()
        classifier = VotingClassifier(estimators=[i for i in ([
            ('knn', KNeighborsClassifier()),
            ('rf', RandomForestClassifier()),
            ('svm', SVC()),
        ])])
        random_search = RandomizedSearchCV(
            classifier,
            param_distributions={'voting': [
                'hard', 'soft'], 'flatten_transform': ['auto', True, False]},
            n_iter=1000,
            cv=10,
            random_state=0,
            n_jobs=-1
        )
        random_search.fit(X_train, y_train)
        best_voting_ensemble = random_search.best_estimator_
        y_pred_validate = best_voting_ensemble.predict(X_validate)
        y_pred_test = best_voting_ensemble.predict(X_test)
        print(f"Best params: {random_search.best_params_}")

        self.validation_scores["Voting Ensemble"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["Voting Ensemble"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (Voting Ensemble)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

    def neural_network(self) -> None:
        X_train, X_validate, X_test, y_train, y_validate, y_test = self.preprocess()

        ann = Sequential([
            Dense(units=40, activation='relu', kernel_regularizer=L2(
                0.001), input_shape=(X_train.shape[1],)),
            # Normalize outputs from every prev layer, for stable distribution of activation values
            BatchNormalization(),
            Dense(units=35, activation='relu', kernel_regularizer=L2(0.001)),
            BatchNormalization(),
            Dense(units=28, activation='relu', kernel_regularizer=L2(0.001)),
            BatchNormalization(),
            Dropout(0.2),
            Dense(units=18, activation='relu', kernel_regularizer=L2(0.001)),
            BatchNormalization(),
            Dropout(0.1),
            Dense(units=8, activation='relu', kernel_regularizer=L2(0.001)),
            BatchNormalization(),
            Dropout(0.1),
            Dense(units=1, activation='linear'),
        ])
        # Avoid roundoff errors by using intermediate values. However, since output layer uses linear activation, result is not probability
        ann.compile(optimizer=Adam(learning_rate=0.01), loss=BinaryCrossentropy(
            from_logits=True), metrics=['accuracy'])
        ann.fit(X_train, y_train, batch_size=32, epochs=140, callbacks=[EarlyStopping(
            monitor="val_loss", patience=2), ModelCheckpoint("best_nn.keras", save_best_only=True)])
        y_pred_validate = sigmoid(ann.predict(X_validate))
        y_pred_test = sigmoid(ann.predict(X_test))
        y_pred_validate = (y_pred_validate >= 0.5)._numpy().astype(int)
        y_pred_test = (y_pred_test >= 0.5)._numpy().astype(int)
        self.validation_scores["ANN"] = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
            y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
        self.test_scores["ANN"] = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
            y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
        ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                                 y_pred_test, labels=[0, 1])).plot()
        mplt.title('Confusion Matrix on Test (ANN)')
        mplt.xlabel('Predicted')
        mplt.ylabel('True')
        mplt.show()

        ann.summary()

    def analyze_results(self):
        self.knn()
        self.svm()
        self.nb()
        self.catboost()
        self.xgboost()
        self.bagging()
        self.random_forest()
        self.voting_ensemble()
        self.neural_network()

        print(f"Validation scores:\n{self.validation_scores}")
        print(f"Test scores:\n{self.test_scores}")

        classifiers = list(self.test_scores.keys())
        accuracies = [self.test_scores[clf]["Accuracy"] for clf in classifiers]
        recalls = [self.test_scores[clf]["Recall"] for clf in classifiers]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=classifiers,
            y=accuracies,
            name='Accuracy',
            marker_color='indigo'
        ))
        fig.add_trace(go.Bar(
            x=classifiers,
            y=recalls,
            name='Recall',
            marker_color='lightblue'
        ))
        fig.update_layout(
            title='Classifier Performance (Accuracy & Recall)',
            xaxis=dict(title='Classifier'),
            yaxis=dict(title='Score'),
            barmode='group',
            legend=dict(x=0.01, y=0.99)
        )
        fig.show()


mlp = MLP()
mlp.analyze_results()
