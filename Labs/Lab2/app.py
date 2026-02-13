import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Required environment variable (not provided)
app.secret_key = os.environ["APP_SECRET"]

@app.route("/")
def home():
    return "Application is running."

if __name__ == "__main__":
    # Port commonly used by other software
    app.run(host="0.0.0.0", port=5000)
