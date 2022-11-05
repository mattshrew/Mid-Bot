import os
import datetime
import asyncio

import disnake
from disnake.ext import commands
from dotenv import load_dotenv


from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGO = os.getenv('MONGO_URL')


class MidBot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activity = disnake.Game(name="VALORANT", created_at=datetime.datetime.now())
        self.cluster = None
        self.accounts = None

        print("Class Established.")

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
    
    def load_cogs(self):
        print("Loading Cogs...")

        self.load_extension('jishaku')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} loaded!")
        print("Cogs are loaded...")
    
    def load_database(self):
        print("Establishing database...")

        self.cluster = AsyncIOMotorClient(MONGO)
        self.riot = bot.cluster["RIOT"]
        self.accounts = bot.riot["Accounts"]

        print("Database established succesfully!")

intents = disnake.Intents.all()

bot = MidBot(
    command_prefix=['!'],
    case_insensitive=True,
    intents=intents,
    owner_ids=[
        672173302373941256
    ],
    strip_after_prefix=True
)


bot.load_cogs()
bot.load_database()
bot.run(TOKEN)