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
    
    @commands.slash_command(name="purge", description="Mass delete messages!")
    async def purge(self, ctx, messages: int):
        if messages <= 0:
            return await ctx.response.send_message(embed=disnake.Embed(
            description=f"**Please specify a positive number of messages.**",
            colour=disnake.Colour.red()
            ).set_footer(text=f"Executed by {ctx.author.name}", icon_url=ctx.author.display_avatar)
        )
            
        plurality = 's'
        if messages == 1:
            plurality = ''
            
        await ctx.channel.purge(limit=messages)
        return await ctx.response.send_message(embed=disnake.Embed(
            description=f"**Successfully purged {messages} message{plurality}!**",
            colour=disnake.Colour.green()
            ).set_footer(text=f"Executed by {ctx.author.name}", icon_url=ctx.author.display_avatar)
        )

def setup(bot):
    bot.add_cog(Moderation(bot))