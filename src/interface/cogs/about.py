"""About bot command module"""

import time
import platform
import discord
from discord.ext import commands
from discord import app_commands
from discord.http import Route


class AboutBotCog(commands.Cog):
    """Cog for about command"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start_time = time.time()

    @staticmethod
    def _format_row(left, right, pad):
        """Formats two texts to a row"""
        left_text = f"{left[0]}: {left[1]}".ljust(pad)
        right_text = f"{right[0]}: {right[1]}"
        return f"{left_text}    {right_text}"

    # pylint: disable=too-many-locals
    @app_commands.command(name="about_bot", description="get info about bot")
    async def about_bot(self, interaction: discord.Interaction, invisible: bool = False) -> None:
        """Gets info about bot"""
        await interaction.response.defer(thinking=True, ephemeral=invisible)

        gw_ping = round(self.bot.latency * 1000)

        start = time.monotonic()
        await self.bot.http.request(Route("GET", "/gateway"))
        rest_ping = round((time.monotonic() - start) * 1000)

        bot_name = self.bot.user.name if self.bot.user else "Unknown"

        uptime = time.time() - self.start_time
        uptime_days = int(uptime // 86400)
        uptime_hours = int((uptime % 86400) // 3600)
        uptime_minutes = int((uptime % 3600) // 60)

        rows = [
            (("Name", bot_name), ("Servers", len(self.bot.guilds))),
            (
                ("Users", len(set(self.bot.get_all_members()))),
                ("Shards", self.bot.shard_count),
            ),
            (
                ("Shard ID", self.bot.shard_id),
                (
                    "Uptime",
                    f"{uptime_days}d {uptime_hours}h {uptime_minutes}m",
                ),
            ),
            (
                ("System", platform.system()),
                ("Python", platform.python_version()),
            ),
            (
                ("GW Ping", f"{gw_ping}ms"),
                ("REST Ping", f"{rest_ping}ms"),
            ),
        ]

        left_preview = [
            f"{left[0]}: {left[1]}"
            for left, _ in rows
        ]
        pad = max(len(text) for text in left_preview) + 2

        message_lines = [
            self._format_row(left, right, pad)
            for left, right in rows
        ]

        message = "📦 Bot info\n\n" + "\n".join(message_lines)

        await interaction.followup.send(message)
