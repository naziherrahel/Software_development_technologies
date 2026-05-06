# Lab: Blue-Green and Canary Deployment with Docker Compose, Nginx, and Locust

Duration: 1.5 hours

In this lab, you will deploy two versions of the same application and control how user traffic reaches them.

The important idea here is simple: after CI/CD builds and prepares an application, deployment decides how the new version reaches real users.

Do not just run the command -- understand what changed.

## Learning Objectives

By the end of this lab, you should be able to:

- explain Blue-Green deployment
- switch traffic between two app versions
- perform rollback
- explain Canary deployment
- observe deployment behavior using Locust and logs

## Prerequisites

You need:

- Docker
- Docker Compose
- a browser
- basic terminal commands

You do not need cloud services, external accounts, Kubernetes, or any AI/ML tools.

## Project Architecture

The lab runs fully on your machine.

```text
Browser / Locust
       |
       v
     Nginx
       |
       +------> app_blue   (stable version)
       |
       +------> app_green  (new release)
```

Nginx is the reverse proxy. It receives user requests and decides where to send them.

The applications are small FastAPI services. Each response includes:

- version
- hostname
- timestamp
- request id
- random value
- short message

## Files You Will Use

```text
lab-deployment-strategies/
├── docker-compose.yml
├── app_blue/
├── app_green/
├── nginx/
│   ├── nginx.blue.conf
│   ├── nginx.green.conf
│   └── nginx.canary.conf
└── locust/
    └── locustfile.py
```

The three Nginx files are the main deployment controls:

- `nginx.blue.conf` sends 100% traffic to BLUE
- `nginx.green.conf` sends 100% traffic to GREEN
- `nginx.canary.conf` sends about 90% traffic to BLUE and 10% to GREEN

## Step 1: Start the System

Open a terminal in this folder:

```bash
cd lab-deployment-strategies
```

Start all services:

```bash
docker compose up -d --build
```

Check that the containers are running:

```bash
docker compose ps
```

At startup, Nginx uses the BLUE configuration. This means users are sent to the stable version first.

## Step 2: Check the Current Version

Open this URL:

```text
http://localhost:8080
```

Or use curl:

PowerShell:

```powershell
Invoke-RestMethod http://localhost:8080
```

Git Bash or Linux:

```bash
curl http://localhost:8080
```

You should see JSON similar to this:

```json
{
  "version": "blue",
  "hostname": "abc123",
  "timestamp": "2026-05-06T10:00:00+00:00",
  "request_id": "8f2a91c0",
  "random_value": 4821,
  "message": "Stable production version"
}
```

Notice the `version` field. In deployment work, this small detail matters because it tells us which version is actually serving users.

## Step 3: Blue-Green Deployment

In Blue-Green deployment:

- BLUE is the current stable version
- GREEN is the new version
- both versions run at the same time
- Nginx switches traffic between them

Right now, traffic goes to BLUE.

Switch traffic to GREEN:

```bash
docker compose cp nginx/nginx.green.conf nginx:/etc/nginx/conf.d/default.conf
docker compose exec nginx nginx -s reload
```

Now check the application again:

```bash
curl http://localhost:8080
```

You should now see:

```json
"version": "green"
```

The application containers were not rebuilt. Nginx changed where traffic goes.

That is the deployment action.

## Step 4: Rollback

Rollback means returning users to the previous working version.

Switch traffic back to BLUE:

```bash
docker compose cp nginx/nginx.blue.conf nginx:/etc/nginx/conf.d/default.conf
docker compose exec nginx nginx -s reload
```

Check again:

```bash
curl http://localhost:8080
```

You should see:

```json
"version": "blue"
```

The important idea here: rollback is fast because BLUE was still running. We did not need to rebuild or redeploy it.

## Step 5: Canary Deployment

In Canary deployment, we do not send all users to the new version immediately.

We send a small percentage to GREEN first, then watch what happens.

Switch Nginx to Canary mode:

```bash
docker compose cp nginx/nginx.canary.conf nginx:/etc/nginx/conf.d/default.conf
docker compose exec nginx nginx -s reload
```

The default split is:

```text
90% -> BLUE
10% -> GREEN
```

Run several requests and observe the mixed versions.

PowerShell:

```powershell
1..20 | ForEach-Object { (Invoke-RestMethod http://localhost:8080).version }
```

Git Bash or Linux:

```bash
for i in {1..20}; do curl -s http://localhost:8080; echo; done
```

Most responses should be BLUE. Some responses should be GREEN.

This is the point of Canary deployment: test the new release with limited user impact.

## Step 6: Observe with Locust

Locust is not the deployment strategy itself. We use it to create traffic so we can observe behavior during deployment.

Open Locust:

```text
http://localhost:8089
```

Start a load test with:

```text
Number of users: 20
Spawn rate: 2
Host: http://nginx
```

If the Host field is already filled in, keep it as it is.

Watch:

- request count
- response time
- failures
- how traffic behaves after switching Nginx config

You can also watch Nginx logs:

```bash
docker compose logs -f nginx
```

In the log output, look for:

- status code
- upstream address
- request time

The upstream address helps you see whether Nginx sent a request to BLUE or GREEN.

## Step 7: Simulate Failure in GREEN

Now we make GREEN unstable.

Open `docker-compose.yml` and find this part:

```yaml
app_green:
  environment:
    FAIL_RATE: "0.0"
```

Change it to:

```yaml
app_green:
  environment:
    FAIL_RATE: "0.3"
```

This means about 30% of GREEN requests return HTTP 500.

Restart only the GREEN service:

```bash
docker compose up -d --no-deps app_green
```

Keep Nginx in Canary mode:

```bash
docker compose cp nginx/nginx.canary.conf nginx:/etc/nginx/conf.d/default.conf
docker compose exec nginx nginx -s reload
```

Run Locust again and observe failures.

Because only about 10% of traffic goes to GREEN, the total failure rate should be much lower than 30%.

Now ask yourself:

```text
Would you continue rollout or rollback?
```

If the new version is failing, rollback to BLUE:

```bash
docker compose cp nginx/nginx.blue.conf nginx:/etc/nginx/conf.d/default.conf
docker compose exec nginx nginx -s reload
```

## Step 8: Decision Questions

Answer these questions in your submission:

1. Which strategy gives faster rollback?
2. Which strategy reduces user risk?
3. Why is monitoring important during deployment?
4. What would happen if we deployed GREEN to 100% immediately?
5. What is the role of Nginx here?

Use your own words. Short answers are fine, but they must show that you understood the deployment behavior.

## Submission Requirements

Submit:

- screenshot of BLUE response
- screenshot of GREEN response
- screenshot or terminal output showing Canary mixed responses
- screenshot of Locust running
- short answers to the reflection questions

## Cleanup

Stop and remove the lab containers:

```bash
docker compose down
```

If you changed `FAIL_RATE`, set it back to `"0.0"` before your next run.

## Useful Notes

If port `8080` or `8089` is already used on your machine, stop the other program first.

You can also run the lab on another port.

PowerShell example:

```powershell
$env:APP_PORT="8090"
docker compose up -d --build
```

Git Bash or Linux example:

```bash
APP_PORT=8090 docker compose up -d --build
```

Then open:

```text
http://localhost:8090
```

If you restart the Nginx container, it starts again in BLUE mode. This is intentional for the lab.

If `docker compose` does not work on your system, your Docker installation may be old. Try `docker-compose` with the same arguments, or update Docker Desktop / Docker Compose.
