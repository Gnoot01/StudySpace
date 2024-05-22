from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from preprocess import Preprocessor


def svm(config={"param_distributions": {"C": [0.5, 0.8, 1], "kernel": [
        "linear", "poly", "rbf", "sigmoid"], "degree": [2, 3, 4, 5]}, "n_iter": 1000, "cv": 10}) -> tuple:
    preprocessor = Preprocessor()
    X_train, X_validate, X_test, y_train, y_validate, y_test = preprocessor.preprocess()

    classifier = SVC()
    random_search = RandomizedSearchCV(
        classifier,
        param_distributions=config["param_distributions"],
        n_iter=config["n_iter"],
        cv=config["n_iter"],
        random_state=0,
        n_jobs=-1
    )
    random_search.fit(X_train, y_train.values.ravel())
    best_svm = random_search.best_estimator_
    y_pred_validate = best_svm.predict(X_validate)
    y_pred_test = best_svm.predict(X_test)
    print(f"Best params: {random_search.best_params_}")

    validation_scores = {"Accuracy": accuracy_score(y_pred_validate, y_validate), "Precision": precision_score(
        y_pred_validate, y_validate), "Recall": recall_score(y_pred_validate, y_validate), "F1": f1_score(y_pred_validate, y_validate)}
    test_scores = {"Accuracy": accuracy_score(y_pred_test, y_test), "Precision": precision_score(
        y_pred_test, y_test), "Recall": recall_score(y_pred_test, y_test), "F1": f1_score(y_pred_test, y_test)}
    ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,
                                                             y_pred_test, labels=[0, 1])).plot()
    plt.title('Confusion Matrix on Test (SVM)')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    return validation_scores, test_scores
