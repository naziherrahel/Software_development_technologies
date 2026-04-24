import argparse
import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a Random Forest model on the Iris dataset."
    )
    parser.add_argument(
        "--output-dir",
        default="assets",
        help="Directory where the model, metrics, and confusion matrix are saved.",
    )
    return parser.parse_args()


def train_model(output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=1,
        stratify=iris.target,
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = model.score(x_test, y_test)
    matrix = confusion_matrix(y_test, predictions)

    model_path = output_path / "iris_model.joblib"
    image_path = output_path / "confusion_matrix.png"
    metrics_json_path = output_path / "metrics.json"
    metrics_text_path = output_path / "metrics.txt"

    joblib.dump(model, model_path)

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=iris.target_names,
    )
    figure, axis = plt.subplots(figsize=(6, 4.5))
    display.plot(ax=axis, cmap=plt.cm.Blues, colorbar=False)
    axis.set_title("Random Forest on Iris")
    figure.tight_layout()
    figure.savefig(image_path)
    plt.close(figure)

    metrics = {
        "model_name": "Random Forest Classifier",
        "dataset_name": "Iris",
        "accuracy": round(float(accuracy), 4),
        "accuracy_display": f"{accuracy:.2f}",
        "train_samples": len(x_train),
        "test_samples": len(x_test),
        "confusion_matrix": matrix.tolist(),
        "class_names": iris.target_names.tolist(),
    }

    metrics_json_path.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )
    metrics_text_path.write_text(
        "\n".join(
            [
                f"Model: {metrics['model_name']}",
                f"Dataset: {metrics['dataset_name']}",
                f"Accuracy: {metrics['accuracy_display']}",
                f"Train samples: {metrics['train_samples']}",
                f"Test samples: {metrics['test_samples']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Model saved to {model_path}")
    print(f"Accuracy: {metrics['accuracy_display']}")


if __name__ == "__main__":
    args = parse_args()
    train_model(args.output_dir)
