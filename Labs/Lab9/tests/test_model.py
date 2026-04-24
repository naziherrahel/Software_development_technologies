import json
import os
from pathlib import Path

import joblib


OUTPUT_DIR = Path(os.getenv("MODEL_OUTPUT_DIR", "assets"))
MINIMUM_ACCURACY = float(os.getenv("MINIMUM_ACCURACY", "0.90"))


def load_metrics():
    metrics_path = OUTPUT_DIR / "metrics.json"
    return json.loads(metrics_path.read_text(encoding="utf-8"))


def test_expected_artifacts_exist():
    expected_files = [
        OUTPUT_DIR / "iris_model.joblib",
        OUTPUT_DIR / "metrics.json",
        OUTPUT_DIR / "metrics.txt",
        OUTPUT_DIR / "confusion_matrix.png",
    ]

    for file_path in expected_files:
        assert file_path.exists(), f"Missing expected file: {file_path}"


def test_model_can_be_loaded():
    model_path = OUTPUT_DIR / "iris_model.joblib"
    model = joblib.load(model_path)
    assert hasattr(model, "predict")


def test_model_accuracy_is_high_enough():
    metrics = load_metrics()
    assert metrics["accuracy"] >= MINIMUM_ACCURACY


def test_confusion_matrix_shape():
    metrics = load_metrics()
    matrix = metrics["confusion_matrix"]
    assert len(matrix) == 3
    assert all(len(row) == 3 for row in matrix)
