from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from preprocess import Preprocessor


def catboost(config={"param_distributions": {}}) -> tuple:
    # Training ensemble of predictors sequentially, learning from predecessor in diff methods
    preprocessor = Preprocessor()
    X_train, X_validate, X_test, y_train, y_validate, y_test = preprocessor.preprocess()

    classifier = CatBoostClassifier(config["param_distributions"])
    classifier.fit(X_train, y_train.values.ravel())
    y_pred_validate = classifier.predict(X_validate)
    y_pred_test = classifier.predict(X_test)

    validation_scores = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
        y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
    test_scores = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
        y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
    ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                             y_pred_test, labels=[0, 1])).plot()
    plt.title('Confusion Matrix on Test (Catboost)')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    return validation_scores, test_scores
