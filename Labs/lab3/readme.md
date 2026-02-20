# Lab 3 — Cloud Deployment (Independent Task)

Topic: Cloud Computing & Virtualization  
Mode: Individual  

---

## Objective

You are required to deploy this API to a virtual machine in Yandex Cloud.

You must configure the infrastructure and the runtime environment yourself.

This repository contains only the application source code and dependency file.  
You are responsible for making it run in a cloud environment.

---

## What You Are Deploying

This API simulates a basic fraud detection service used by financial platforms.

When deployed successfully, the API documentation will be available at:

http://<your_public_ip>:8000/docs

The `/analyze` endpoint must be fully functional and accessible from your browser.

---

## Step 1 — Create Virtual Machine

Configuration requirements:

- OS: Ubuntu 22.04 or 24.04
- 2 vCPU
- 2 GB RAM minimum
- Public IPv4 address enabled
- SSH key authentication

After the VM is running, connect using SSH:

ssh -l <your_username> <public_ip>

You must successfully access your VM terminal.

---

## Step 2 — Server Preparation

Your server must be prepared to run a Python-based web API.

You must ensure:

- Required system packages are installed
- The project files are available on the VM
- Python dependencies are installed in an isolated environment

You must decide how to accomplish these tasks.

---

## Step 3 — Application Configuration

This repository includes a file:

.env.example

You must determine:

- Why this file exists
- How it should be used
- How to make the application read configuration values correctly

The application will not run correctly without proper configuration.

---

## Step 4 — Run the Application

The API must:

- Run on port 8000
- Be accessible from outside the VM
- Display interactive documentation at `/docs`

If the application fails, you must read the error messages carefully and resolve them.

---

## Step 5 — Network Configuration

If the API is not accessible from your browser:

You must investigate cloud network and security settings.

The application must be publicly reachable.

---

## Expected Result

When finished:

- The API runs on your VM
- The `/docs` page loads in your browser
- The `/analyze` endpoint processes requests successfully

---

## Deliverables

Submit:

1. Screenshot of VM configuration
2. Screenshot of successful SSH connection
3. Screenshot of `/docs` running in browser
4. Screenshot of successful `/analyze` request
5. List of commands you used (in order)
6. Reflection (300–400 words):
   - What errors occurred?
   - How did you resolve them?
   - What did you learn about cloud infrastructure?

---

## Important Notes

- Do not use Docker.
- Do not copy a complete solution from external sources.
- You are expected to investigate and troubleshoot independently.

This lab evaluates your ability to configure infrastructure and deploy software manually.
