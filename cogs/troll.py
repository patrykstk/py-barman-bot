import discord
from discord.ext import commands
from discord import app_commands
from utils import log
import asyncio

class Troll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log('INFO', 'Troll cog loaded')

    @app_commands.command(name="rzut", description="Rzuca użytkownikiem między dwoma wybranymi kanałami głosowymi.")
    @app_commands.describe(
        member="Użytkownik do rzucania",
        channel_a="Pierwszy kanał głosowy",
        channel_b="Drugi kanał głosowy",
        times="Ile razy rzucić (domyślnie 5)",
        delay="Opóźnienie między rzutami w sekundach (domyślnie 1.0)"
    )
    async def rzut(
            self,
            interaction: discord.Interaction,
            member: discord.Member,
            channel_a: discord.VoiceChannel,
            channel_b: discord.VoiceChannel,
            times: app_commands.Range[int, 1, 10] = 5,
            delay: app_commands.Range[float, 0.5, 5.0] = 1.0
    ):
        log('INFO',
            f"Wywołano komendę rzut przez {interaction.user.display_name} dla: {member.display_name} | Kanały: {channel_a.name}, {channel_b.name} | {times} razy | co {delay}s")

        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Ta komenda może być używana tylko na serwerze.", ephemeral=True)
            return

        if not isinstance(channel_a, discord.VoiceChannel) or not isinstance(channel_b, discord.VoiceChannel):
            await interaction.response.send_message(
                "Musisz wybrać dwa kanały głosowe.", ephemeral=True
            )
            return

        if not member.voice or not member.voice.channel:
            await interaction.response.send_message(f"{member.display_name} nie jest na kanale głosowym.",
                                                    ephemeral=True)
            return

        if channel_a.id == channel_b.id:
            await interaction.response.send_message("Musisz wybrać dwa różne kanały głosowe!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=False)

        initial_channel = member.voice.channel
        log('INFO', f"Startowy kanał {member.display_name}: {initial_channel.name} (ID: {initial_channel.id})")

        current_channel = initial_channel

        try:
            for i in range(times):
                if current_channel.id == channel_a.id:
                    target_channel = channel_b
                else:
                    target_channel = channel_a

                log('INFO',
                    f"[{i + 1}/{times}] Przenoszę {member.display_name} do: {target_channel.name} (ID: {target_channel.id})")

                if not guild.me.guild_permissions.move_members:
                    await interaction.followup.send(
                        "Nie mam uprawnień do przenoszenia użytkowników. Upewnij się, że bot ma rolę z uprawnieniem 'Przenieś członków'.",
                        ephemeral=True)
                    return
                if not target_channel.permissions_for(guild.me).connect:
                    await interaction.followup.send(
                        f"Nie mam uprawnień do łączenia się z kanałem {target_channel.name}.", ephemeral=True)
                    return
                if not target_channel.permissions_for(member).connect:
                    await interaction.followup.send(
                        f"{member.display_name} nie ma uprawnień do łączenia się z kanałem {target_channel.name}.",
                        ephemeral=True)
                    return

                await member.move_to(target_channel, reason="Komenda /rzut")
                await asyncio.sleep(delay)

                member = guild.get_member(member.id)
                if not member.voice or not member.voice.channel:
                    await interaction.followup.send(
                        f"Użytkownik {member.display_name} opuścił kanał głosowy lub został przeniesiony ręcznie.",
                        ephemeral=True)
                    return
                current_channel = member.voice.channel

            await interaction.followup.send(
                f"Zakończono rzucanie użytkownika {member.display_name}. Rzucam go z powrotem na pierwotny kanał: {initial_channel.name}.")
            await member.move_to(initial_channel, reason="Zakończenie komendy /rzut - powrót do kanału początkowego")

        except discord.errors.Forbidden:
            await interaction.followup.send(
                f"Nie mam uprawnień do przenoszenia użytkownika {member.display_name} "
                "lub łączenia się z jednym z kanałów. Sprawdź moje uprawnienia lub uprawnienia kanałów.", ephemeral=True
            )
        except Exception as e:
            log('ERROR', f"Błąd podczas komendy /rzut: {e}")
            await interaction.followup.send(f"Wystąpił nieoczekiwany błąd: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Troll(bot))
