import os
import discord
from discord.ext import commands
from discord import app_commands
from utils import log

class Interaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log('INFO', 'Interaction cog loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel_id_str = os.getenv("JOIN_CHANNEL_ID")
        if channel_id_str:
            try:
                channel_id = int(channel_id_str)
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(f'Siema {member.mention}!')
                else:
                    log('[ERROR]', f'Couldnt find channel id {channel_id}')

            except ValueError:
                log('[ERROR]', 'ENV:JOIN_CHANNEL_ID is not a number')
            except Exception as e:
                log('[ERROR]', 'Error in on_member_join()')

        else:
            log('[ERROR]', 'ENV:JOIN_CHANNEL_ID is not set')

    @app_commands.command(name="about", description="Wyświetla informacje o bocie.")
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'''Cześć! Jestem {self.bot.user.display_name}.''')

async def setup(bot):
    await bot.add_cog(Interaction(bot))