# Lab 4 — Containerization and Deployment

You must containerize this application and deploy it.

## Structure 

lab4-transaction-monitor-ui/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── data/
│   └── transactions.json
├── .env.example
└── README.md

## Requirements

1. Create a Dockerfile.
2. Build a Docker image.
3. Run the container locally.
4. Ensure transactions persist after container restart.
5. Push your image to Docker Hub.
6. Pull and run it inside your Yandex VM.
7. Make the application publicly accessible.

## Important

If data disappears after container restart, you have not configured persistence correctly.

The application must:

- Display a working web UI
- Store transactions permanently
- Run on port 8000
- Be accessible from the browser

## Deliverables

- Screenshot of working UI locally
- Screenshot showing persistence after restart
- Screenshot of Docker Hub repository
- Screenshot of running container in Yandex VM
- Reflection (300 words)