# Clash-Bot

Discord bot to send League of Legends Clash updates to Discord.

## Project structure

```text
.
├── src/
│   ├── __init__.py
│   └── bot.py
├── main.py
├── Dockerfile
├── .dockerignore
├── Procfile
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

## Environment setup

1. Copy `.env.example` to `.env`.
2. Add your bot token to `DISCORD_TOKEN` in `.env`.
3. Keep `.env` private (it is ignored by git).

## Run

```bash
python3 main.py
```

## Test command

Use `/hello` in a channel where the bot has access. It should reply with a simple hello message.

Use `/clash` to fetch and post Clash schedule data.

## Deploy on Railway

1. Push this repo to GitHub.
2. In Railway: `New Project` -> `Deploy from GitHub repo`.
3. Add environment variables in Railway project settings:
   - `DISCORD_TOKEN`
   - `RIOT_API_KEY`
   - `RIOT_PLATFORM` (example: `euw1`)
4. In Discord Developer Portal -> your bot -> `Privileged Gateway Intents`, enable `MESSAGE CONTENT INTENT` (required by this bot's current message-command handler).
5. Deploy. Railway runs the worker using:
   - `Procfile`: `worker: python main.py`

## Local install

```bash
pip install -r requirements.txt
```

## Run with Docker

Build image:

```bash
docker build -t clash-bot:latest .
```

Run container:

```bash
docker run --rm --env-file .env clash-bot:latest
```

## GitHub Actions CI/CD to AWS EC2

Workflow file: `.github/workflows/ci-cd.yml`

- CI runs on every pull request and every push:
  - installs dependencies
  - compiles Python files
  - validates Docker image builds
- CD runs only on push to `main`:
  - SSH into your EC2 host
  - pulls latest `main`
  - rebuilds Docker image
  - restarts the bot container

Add these GitHub repository secrets before enabling deploy:

- `EC2_HOST`: Public IP or DNS of your EC2 instance.
- `EC2_USERNAME`: Linux user (usually `ec2-user` for Amazon Linux).
- `EC2_SSH_KEY`: Private SSH key content for your EC2 key pair.
- `EC2_APP_DIR`: Absolute path to your repo on EC2.

Prerequisites on EC2:

- Docker installed and running.
- Repo cloned at `EC2_APP_DIR`.
- A valid `.env` file present inside `EC2_APP_DIR`.
