# Lab 05 — Git Fundamentals and Branching Model


---

# 1. Objectives

By the end of this laboratory session, students should be able to:

* Initialize and manage a local Git repository
* Distinguish between working directory, staging area, and repository
* Create and manage branches
* Perform merges and resolve merge conflicts
* Visualize commit history using graphical log representation
* Connect a local repository to a remote GitHub repository

---

# 2. Scenario

You are part of a small development team working on a Python-based command-line application named:

student_portal

The goal of this lab is to simulate feature development using proper branching and merging strategies.

---

# 3. Part I — Repository Initialization

## Step 1 — Create Project Structure

1. Create a new directory named:

student_portal

2. Inside the directory, create a Python file named:

app.py

Add the following content:

```python
"""Simple Student Portal Application"""


def main():
    print("Student Portal System")


if __name__ == "__main__":
    main()
```

3. Open Git Bash inside the project directory.

4. Initialize a Git repository:

```
git init
```

5. Stage and commit the initial version of the project.

---

## Required Screenshots

* Output of `git status` before staging
* Output of `git log --oneline` after first commit

---

# 4. Part II — Understanding the Staging Area 

1. Modify `app.py` by adding a new function:

```python

def login(username):
    print(f"User {username} logged in.")
```

2. Modify the file again (for example, change the printed message).

3. Run:

```
git status
```

4. Stage the file.

5. Modify the file once more after staging.

6. Run `git status` again and observe the difference.

7. Commit the staged changes.

---

## Required Screenshots

* `git status` after modifying the file post-staging
* `git log --oneline`

---

# 5. Part III — Branching Workflow 

## Step 1 — Create a Feature Branch

Create and switch to a new branch named:

feature-authentication

```
git checkout -b feature-authentication
```

## Step 2 — Implement Feature

1. Extend `app.py` by adding another function:

```python

def logout(username):
    print(f"User {username} logged out.")
```

2. Stage and commit the changes with a meaningful commit message.

---

## Required Screenshots

* Output of `git branch`
* Output of `git log --oneline --graph --all`

---

# 6. Part IV — Simulating Parallel Development 

1. Switch back to the main branch:

```
git checkout main
```

2. Modify the same section of `app.py` differently (for example, change the output message inside `login`).

3. Stage and commit the change.

---

# 7. Part V — Merge and Conflict Resolution 

1. Merge the feature branch into main:

```
git merge feature-authentication
```

2. If a merge conflict occurs:

   * Inspect the conflict markers inside `app.py`
   * Manually resolve the conflict
   * Stage the resolved file
   * Commit the merge

---

## Required Screenshots

* Conflict markers shown in the file
* Final output of `git log --oneline --graph --all`

---

# 8. Part VI — Remote Repository Integration 

## Step 1 — Create Repository on GitHub

Create a new repository on GitHub named:

student_portal

Do not initialize it with a README file.

## Step 2 — Connect Local Repository to Remote

```
git remote add origin <repository-url>
git branch -M main
git push -u origin main
```

---

## Required Screenshots

* GitHub repository page after successful push
* Branch view on GitHub

---

# 9. Conceptual Questions

Create a Markdown file named:

LAB05_REPORT.md

Answer the following questions in your own words:

1. What does HEAD represent?
2. Under what conditions does a merge conflict occur?
3. What is the difference between `git clone` and `git pull`?

---

# 10. Submission Requirements

Push the following to your GitHub repository:

* All project files
* LAB05_REPORT.md
* A directory named `screenshots/` containing all required screenshots

Expected structure:

student_portal/
│
├── app.py
├── LAB05_REPORT.md
├── screenshots/
│   ├── status_before_stage.png
│   ├── log_graph.png
│   └── ...

---

# 11. Evaluation Criteria

* Correct use of branching and merging
* Successful conflict resolution
* Clarity and correctness of conceptual answers
* Clean and organized repository structure

---

# 12. Preparation for Next Session

The next laboratory session will examine Git internals, including:

* Structure of the `.git` directory
* Object storage model
* Commit hashes and references

A solid understanding of today’s concepts is required for the next session.

---

