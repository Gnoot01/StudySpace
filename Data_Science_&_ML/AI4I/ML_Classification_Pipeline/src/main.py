import plotly.graph_objects as go
from models.neural_network import neural_network
from models.voting_ensemble import voting_ensemble
from models.random_forest import random_forest
from models.bagging import bagging
from models.xgboost import xgboost
from models.catboost import catboost
from models.naive_bayes import nb
from models.svm import svm
from models.knn import knn
import argparse
import json


def main(config):
    models = {
        "knn": knn,
        "svm": svm,
        "nb": nb,
        "catboost": catboost,
        "xgboost": xgboost,
        "bagging": bagging,
        "random_forest": random_forest,
        "voting_ensemble": voting_ensemble,
        "neural_network": neural_network
    }
    validation_scores = {}
    test_scores = {}
    for model_str, model in models.items():
        print(f"Running {model_str.upper()} with config:", config[model_str])
        validation_scores[model_str], test_scores[model_str] = model(
            config[model_str])
        print(
            f"{model_str.upper()} Validation Score: {validation_scores[model_str]}")
        print(f"{model_str.upper()} Test Score: {test_scores[model_str]}\n")

    classifiers = list(test_scores.keys())
    accuracies = [test_scores[clf]["Accuracy"] for clf in classifiers]
    recalls = [test_scores[clf]["Recall"] for clf in classifiers]

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run ML models with configurations")
    parser.add_argument("--config", type=str, default="src/config.json",
                        help="Path to the configuration file")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    main(config)
