from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from tensorflow.keras.regularizers import L2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from tensorflow.keras.activations import sigmoid
from preprocess import Preprocessor


def neural_network(config={
    "units": [40, 35, 28, 18, 8],
    "dropout": [0.2, 0.1, 0.1],
    "learning_rate": 0.01,
    "batch_size": 32,
    "epochs": 140,
    "patience": 2
}):
    preprocessor = Preprocessor()
    X_train, X_validate, X_test, y_train, y_validate, y_test = preprocessor.preprocess()

    ann = Sequential([
        Dense(units=config["units"][0], activation='relu', kernel_regularizer=L2(
            0.001), input_shape=(X_train.shape[1],)),
        # Normalize outputs from every prev layer, for stable distribution of activation values
        BatchNormalization(),
        Dense(units=config["units"][1], activation='relu',
              kernel_regularizer=L2(0.001)),
        BatchNormalization(),
        Dense(units=config["units"][2], activation='relu',
              kernel_regularizer=L2(0.001)),
        BatchNormalization(),
        Dropout(config["dropout"][0]),
        Dense(units=config["units"][3], activation='relu',
              kernel_regularizer=L2(0.001)),
        BatchNormalization(),
        Dropout(config["dropout"][1]),
        Dense(units=config["units"][4], activation='relu',
              kernel_regularizer=L2(0.001)),
        BatchNormalization(),
        Dropout(config["dropout"][2]),
        Dense(units=1, activation='linear'),
    ])

    # Avoid roundoff errors by using intermediate values. However, since output layer uses linear activation, result is not probability
    ann.compile(optimizer=Adam(learning_rate=config["learning_rate"]), loss=BinaryCrossentropy(
        from_logits=True), metrics=['accuracy'])
    ann.fit(X_train, y_train, batch_size=config["batch_size"], epochs=config["epochs"], callbacks=[
        EarlyStopping(monitor="val_loss", patience=config["patience"]),
        ModelCheckpoint("best_nn.keras", save_best_only=True)
    ])
    y_pred_validate = sigmoid(ann.predict(X_validate))
    y_pred_test = sigmoid(ann.predict(X_test))
    y_pred_validate = (y_pred_validate >= 0.5).numpy().astype(int)
    y_pred_test = (y_pred_test >= 0.5).numpy().astype(int)

    validation_scores = {
        "Accuracy": accuracy_score(y_pred_validate, y_validate),
        "Precision": precision_score(y_pred_validate, y_validate),
        "Recall": recall_score(y_pred_validate, y_validate),
        "F1": f1_score(y_pred_validate, y_validate)
    }

    test_scores = {
        "Accuracy": accuracy_score(y_pred_test, y_test),
        "Precision": precision_score(y_pred_test, y_test),
        "Recall": recall_score(y_pred_test, y_test),
        "F1": f1_score(y_pred_test, y_test)
    }

    ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(
        y_test, y_pred_test, labels=[0, 1])).plot()
    plt.title('Confusion Matrix on Test (ANN)')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    ann.summary()

    return validation_scores, test_scores
