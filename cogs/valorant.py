import discord
from discord.ext import commands
from discord import app_commands
import random
from utils import log

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log('INFO', 'Valorant cog loaded')

        self.valorant_agents = [
            "Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock",
            "Fade", "Gekko", "Harbor", "Iso", "Jett", "KAY/O", "Neon",
            "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Tejo", "Viper", "Vyze", "Yoru"
        ]

    @app_commands.command(name="agent-roulette", description="Losuje postać w Valorancie dla 1 do 5 graczy.")
    @app_commands.describe(
        player1="Pierwszy gracz",
        player2="Drugi gracz (opcjonalnie)",
        player3="Trzeci gracz (opcjonalnie)",
        player4="Czwarty gracz (opcjonalnie)",
        player5="Piąty gracz (opcjonalnie)"
    )
    async def agent_roulette(
        self,
        interaction: discord.Interaction,
        player1: discord.Member,
        player2: discord.Member = None,
        player3: discord.Member = None,
        player4: discord.Member = None,
        player5: discord.Member = None
    ):
        players = [p for p in [player1, player2, player3, player4, player5] if p is not None]

        if not players:
            await interaction.response.send_message("Musisz oznaczyć przynajmniej jednego gracza!", ephemeral=True)
            return

        if len(players) > 5:
            await interaction.response.send_message("Możesz oznaczyć maksymalnie 5 graczy!", ephemeral=True)
            return

        results = {}
        available_agents = list(self.valorant_agents)

        for player in players:
            if not available_agents:
                break
            chosen_agent = random.choice(available_agents)
            results[player.display_name] = chosen_agent
            available_agents.remove(chosen_agent)

        response_message = f'Spoko trzymaj(cie):\n'
        for player_name, agent in results.items():
            response_message += f'**{player_name}**: {agent}\n'

        await interaction.response.send_message(response_message)

async def setup(bot):
    await bot.add_cog(Valorant(bot))