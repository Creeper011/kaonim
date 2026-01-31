"""About bot command module"""

import discord
from discord.ext import commands
from discord import app_commands
from src.infrastructure.services.random_joke_service import RandomJokeService

class JokeCog(commands.Cog):
    """Cog for joke command who's show a random joke"""

    def __init__(self, bot: commands.Bot, joke_service: RandomJokeService) -> None:
        self.bot = bot
        self.joke_service = joke_service

    # pylint: disable=too-many-locals
    @app_commands.command(name="joke", description="get a random joke")
    async def joke_command(self, interaction: discord.Interaction, invisible: bool = False) -> None:
        """Gets info about bot"""
        await interaction.response.defer(thinking=True, ephemeral=invisible)
        
        message = self.joke_service.get_random_joke()
        await interaction.followup.send(message)
