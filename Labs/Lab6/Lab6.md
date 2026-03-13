# Lab 06 — Collaborative Data Pipeline with Git 

## 1. Objective

In this laboratory session you will practice collaborative development using Git and GitHub.

You will work in pairs to build a small data processing pipeline while following a professional Git workflow that includes:

* Feature branches
* Pull requests
* Code review
* Merging contributions

The focus of this lab is **collaboration and workflow**, not complex programming.

---

## 2. Scenario

You are part of a small development team building a simple data analysis pipeline based on the Iris dataset.

Your task is to collaborate with your teammate to build a pipeline that:

1. Preprocesses the dataset
2. Trains a machine learning model
3. Evaluates the model performance

Each team member is responsible for a different part of the pipeline.

---

## 3. Team Roles

Work in **pairs**.

### Student A — Data Preprocessing

Responsible for preparing the dataset.

Script to implement:

`preprocessing.py`

---

### Student B — Model Training and Evaluation

Responsible for training and evaluating the model.

Scripts to implement:

`training.py`

`evaluation.py`

---

## 4. Repository Setup

### Step 1 — Create GitHub Repository (Student A)

- Create a repository named:

```
iris-collaboration-lab
```

- **Do not initialize with a README.**

### Step 2 — Clone Repository

- **Student A** clones the repo locally:

```
git clone <repository_url>
cd iris-collaboration-lab
```

- Create project structure:

```
iris-collaboration-lab
│
├── preprocessing.py
├── training.py
├── evaluation.py
├── requirements.txt
└── .gitignore
```

- `.gitignore` content:

```
# Python virtual environments
venv/
.venv/

# Python cache
__pycache__/
*.pyc

# Generated data and model artifacts
*.csv
*.pkl
*.png

# OS files
.DS_Store
Thumbs.db
```

- **Student A** adds **Student B** as a **collaborator** on GitHub.

- **Student B** clones the repository (no fork needed):

```
git clone <repository_url>
cd iris-collaboration-lab
```

---

## 5. Create Feature Branches

**Do not work on `main` branch.**

- **Student A**:

```
git checkout -b feature/data-preprocessing
```

- **Student B**:

```
git checkout -b feature/model-training
```

---

## 6. Implementation

Your goal is simply to make the pipeline work.
Focus on collaboration and Git workflow.

- **Student A:** implement `preprocessing.py`
- **Student B:** implement `training.py` and `evaluation.py`

---

## preprocessing.py

```python
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# Load dataset

def load_data():
    iris = load_iris()
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    return data


# Preprocess dataset

def preprocess_data(data):

    # Feature engineering
    data['sepal_petal_ratio'] = data['sepal length (cm)'] / data['petal length (cm)']

    scaler = StandardScaler()

    features = data.drop(columns=['target','sepal_petal_ratio'])

    data[features.columns] = scaler.fit_transform(features)

    data['target'] = data['target'].astype(int)

    return data


if __name__ == "__main__":

    data = load_data()

    data = preprocess_data(data)

    data.to_csv("cleaned_data.csv", index=False)

    print("Preprocessed data saved as cleaned_data.csv")
```

---

## training.py

```python
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from preprocessing import load_data, preprocess_data


def train_model(data):

    X = data.drop("target", axis=1)

    y = data["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)

    model.fit(X_train, y_train)

    joblib.dump(model, "iris_model.pkl")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy: {accuracy:.2f}")

    return model


if __name__ == "__main__":

    data = load_data()

    data = preprocess_data(data)

    train_model(data)
```

---

## evaluation.py

```python
import pandas as pd
import joblib
import seaborn as sns
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix


def evaluate_model(model, data):

    X = data.drop("target", axis=1)

    y = data["target"]

    predictions = model.predict(X)

    acc = accuracy_score(y, predictions)

    f1 = f1_score(y, predictions, average='weighted')

    cm = confusion_matrix(y, predictions)

    plt.figure(figsize=(8,6))

    sns.heatmap(cm, annot=True, cmap='Blues', fmt='d')

    plt.title("Confusion Matrix")

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.savefig("confusion_matrix.png")

    return acc, f1


if __name__ == "__main__":

    data = pd.read_csv("cleaned_data.csv")

    model = joblib.load("iris_model.pkl")

    acc, f1 = evaluate_model(model, data)

    print(f"Accuracy: {acc:.2f}")

    print(f"F1 Score: {f1:.2f}")
```

---

## 7. Pull Request Workflow (Clear Steps)

1. **Work on your feature branch**

- Student A: `feature/data-preprocessing`
- Student B: `feature/model-training`

2. **Commit your changes**

Example (Student A):

```
git add .
git commit -m "Added preprocessing pipeline"
```

Example (Student B):

```
git add .
git commit -m "Added model training and evaluation"
```

3. **Push your branch to GitHub**

```
git push origin feature/data-preprocessing  # Student A
```

```
git push origin feature/model-training     # Student B
```

4. **Create Pull Request (PR)**

- Each student creates a PR from their feature branch **to `main`**.
- The teammate reviews the PR.

5. **Merge Pull Request**

- After approval, merge the PR into `main`.
- Either the PR creator or the reviewer can merge.

---

## 8. Run the Full Pipeline

Install dependencies:

```
pip install pandas scikit-learn seaborn matplotlib joblib
```

Run scripts in order:

```
python preprocessing.py
python training.py
python evaluation.py
```

Expected outputs (not committed to repo):

* `cleaned_data.csv`
* `iris_model.pkl`
* `confusion_matrix.png`

---

## 9. Submission

Prepare a document named:

```
LAB06_REPORT.docx
```

Upload it to **your personal submission folder**.

Include screenshots:

1. Repository page on GitHub
2. Feature branches
3. Pull request creation
4. Pull request merge
5. Commit history (`git log --graph`)

---

## 10. Reflection Questions

Answer briefly:

1. Why should development not happen directly on `main`?
2. What problem do Pull Requests solve?
3. What could happen if multiple developers modify the same file at the same time?

---

