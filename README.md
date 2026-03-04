# Clash-Bot

Discord bot to send League of Legends Clash updates to Discord.

## Project structure

```text
.
├── src/
│   ├── __init__.py
│   └── bot.py
├── main.py
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
