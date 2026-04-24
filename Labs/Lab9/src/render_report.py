import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render the HTML report from CI-generated artifacts."
    )
    parser.add_argument("--template", required=True, help="Path to the HTML template.")
    parser.add_argument("--metrics", required=True, help="Path to metrics.json.")
    parser.add_argument("--metrics-text", required=True, help="Path to metrics.txt.")
    parser.add_argument("--matrix", required=True, help="Path to confusion matrix image.")
    parser.add_argument("--output", required=True, help="Path to the final index.html file.")
    return parser.parse_args()


def render_report(template_path, metrics_path, metrics_text_path, matrix_path, output_path):
    template = Path(template_path).read_text(encoding="utf-8")
    metrics = json.loads(Path(metrics_path).read_text(encoding="utf-8"))

    if "{{accuracy}}" not in template:
        raise ValueError("The HTML template must contain the {{accuracy}} placeholder.")

    output_file = Path(output_path)
    site_dir = output_file.parent
    site_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(matrix_path, site_dir / "confusion_matrix.png")
    shutil.copy2(metrics_path, site_dir / "metrics.json")
    shutil.copy2(metrics_text_path, site_dir / "metrics.txt")

    replacements = {
        "{{model_name}}": metrics["model_name"],
        "{{dataset_name}}": metrics["dataset_name"],
        "{{accuracy}}": metrics["accuracy_display"],
        "{{train_samples}}": str(metrics["train_samples"]),
        "{{test_samples}}": str(metrics["test_samples"]),
        "{{generated_at}}": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "{{pipeline_run}}": os.getenv("PIPELINE_RUN_NUMBER", "local"),
        "{{commit_sha}}": os.getenv("COMMIT_SHA", "local")[:7],
    }

    report_html = template
    for placeholder, value in replacements.items():
        report_html = report_html.replace(placeholder, value)

    if "{{" in report_html or "}}" in report_html:
        raise ValueError("The rendered report still contains unreplaced placeholders.")

    output_file.write_text(report_html, encoding="utf-8")


if __name__ == "__main__":
    args = parse_args()
    render_report(
        template_path=args.template,
        metrics_path=args.metrics,
        metrics_text_path=args.metrics_text,
        matrix_path=args.matrix,
        output_path=args.output,
    )
