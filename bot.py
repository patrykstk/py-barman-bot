import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils import log

load_dotenv()

COGS = ['interaction', 'valorant', 'troll']

class DiscordBot:
    def __init__(self, discord_token, guild_id=None):
        self.name = 'Krzychu'
        self.discord_token = discord_token
        self.guild_id = guild_id

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        log("INITIALIZATION", 'Starting discord bot..')

        @self.bot.event
        async def on_ready():
            log("INITIALIZATION", f'Logged in as {self.bot.user}.')
            await self.load_cogs()
            await self.sync_commands()
            log("INITIALIZATION", 'Bot is ready to work.')

            COMMANDS_LIST = []
            for cmd in self.bot.tree.get_commands():
                COMMANDS_LIST.append(cmd.name)

            log("INITIALIZATION", f'Commands found: /{", /".join(COMMANDS_LIST)}')

    async def load_cogs(self):
        log("INITIALIZATION", 'Trying to load cogs..')
        for cog_module in COGS:
            try:
                await self.bot.load_extension(f"cogs.{cog_module}")
                log("INITIALIZATION", f'Successfully loaded cog {cog_module}!')
            except commands.ExtensionAlreadyLoaded:
                log("WARNING", f'Cog {cog_module} was already loaded!')
            except commands.ExtensionNotFound:
                log("ERROR", f'Couldnt find cog {cog_module}!')
            except commands.NoEntryPointError:
                log("ERROR", f'Cog {cog_module} has no setup function!')
            except Exception as e:
                import traceback
                log("ERROR", f'Couldnt load cog {cog_module}. Error: {e}!')
                traceback.print_exc()

    async def sync_commands(self):
        try:
            if self.guild_id:
                guild = discord.Object(id=int(self.guild_id))
                self.bot.tree.copy_global_to(guild=guild)
                await self.bot.tree.sync(guild=guild)
                log("SYNCHRONIZATION", f'Synchronized commands for guild {self.guild_id}.')
            else:
                await self.bot.tree.sync()
                log("SYNCHRONIZATION", f'Synchronized global commands.')

        except Exception as e:
            import traceback
            log("ERROR", f'Couldnt synchronize commands with error {e}.')
            traceback.print_exc()

    def run_bot(self):
        if not self.discord_token:
            log("ERROR", 'Discord bot token not found.')
            return
        try:
            self.bot.run(self.discord_token)
        except discord.LoginFailure:
            log("ERROR", 'Wrong discord token.')
        except Exception as e:
            log("ERROR", 'An error occured: {e}')