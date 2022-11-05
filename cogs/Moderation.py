import asyncio
import disnake
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        await ctx.send("Pulling from GitHub...")
        await asyncio.sleep(2)
        await self.bot.close()

def setup(bot):
    bot.add_cog(Moderation(bot))