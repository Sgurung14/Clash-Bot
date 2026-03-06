import os
from typing import Any

import discord
import requests
from dotenv import load_dotenv


load_dotenv()

RIOT_PLATFORM = os.getenv("RIOT_PLATFORM", "euw1")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def _to_unix_ms(value: int) -> int:
    return int(value / 1000)


def _pretty_name(tournament: dict[str, Any]) -> str:
    primary = tournament.get("nameKey", "clash").replace("_", " ").title()
    secondary = tournament.get("nameKeySecondary", "").replace("_", " ").title()
    if secondary:
        return f"{primary} {secondary}"
    return primary


def get_clash_data() -> list[dict[str, Any]]:
    if not RIOT_API_KEY:
        raise RuntimeError("Missing RIOT_API_KEY in .env.")

    url = f"https://{RIOT_PLATFORM}.api.riotgames.com/lol/clash/v1/tournaments"
    response = requests.get(url, headers={"X-Riot-Token": RIOT_API_KEY}, timeout=15)
    response.raise_for_status()
    return response.json()


def build_clash_embed(clash_data: list[dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(
        title="Clash Weekend Queue",
        description="Assemble the squad, lock in on time, and chase the trophy.",
        color=discord.Color.red(),
    )

    schedules: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    for tournament in clash_data:
        for schedule in tournament.get("schedule", []):
            schedules.append((schedule.get("startTime", 0), tournament, schedule))

    schedules.sort(key=lambda item: item[0])

    if not schedules:
        embed.add_field(
            name="No Upcoming Windows",
            value="No Clash schedule is currently available from Riot API.",
            inline=False,
        )
        return embed

    for _, tournament, schedule in schedules:
        registration = _to_unix_ms(schedule["registrationTime"])
        start = _to_unix_ms(schedule["startTime"])
        cancelled = schedule.get("cancelled", False)
        status = "Cancelled" if cancelled else "Open Soon"
        icon = "❌" if cancelled else "🔥"

        value = (
            f"Status: **{status}**\n"
            f"Registration: <t:{registration}:F> (<t:{registration}:R>)\n"
            f"Bracket Starts: <t:{start}:F> (<t:{start}:R>)"
        )

        embed.add_field(
            name=f"{icon} {_pretty_name(tournament)}",
            value=value,
            inline=False,
        )

    embed.set_footer(text=f"Region: {RIOT_PLATFORM.upper()} • Command: /clash")
    return embed


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith("/hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("/clash"):
        try:
            clash_data = get_clash_data()
            embed = build_clash_embed(clash_data)
            await message.channel.send(embed=embed)
        except Exception as exc:
            await message.channel.send(f"Could not fetch Clash data: {exc}")


def run_bot() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Missing DISCORD_TOKEN in .env.")
    client.run(token)
