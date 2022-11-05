import asyncio
import disnake
from disnake.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="tracker", description="Fetches a player's tracker.gg overview.")
    async def tracker(self, ctx, member: disnake.Member = None, ):
        if member is None:
            member = ctx.author
        
        discord = str(member.id)
        document = await self.bot.accounts.find_one({"Discord": discord})

        if document is None:
            return await ctx.response.send_message(embed=disnake.Embed(
                title="Member not found!",
                description=f"<:alert:1038471201938489424> Could not find member: `{member}` in the database.\n> Try using `/acclink <RIOT ID>` to connect account.",
                colour=disnake.Colour.red()).set_footer(text="", icon_url=ctx.author.display_avatar)
            )

        riot_id = document["ID"]
        riot_id = riot_id.replace(" ", "%20")
        riot_id = riot_id.replace("#", "%23")

        return await ctx.response.send_message(f"**{member.mention}'s Overview:**\nhttps://tracker.gg/valorant/profile/riot/{riot_id}/overview")


    @commands.slash_command(name="acclink", description="Links your Discord account to your RIOT account.\n*WARNING: Case Sensitive*")
    async def acclink(self, ctx, riot_id: str):
        discord = str(ctx.author.id)
        document = await self.bot.accounts.find_one({"Discord": discord})

        if document is not None:
            await self.bot.accounts.delete_one({"Discord": discord})
        
        info = {
            "Discord": discord,
            "ID": riot_id
        }

        await self.bot.accounts.insert_one(info)

        return await ctx.response.send_message(embed=disnake.Embed(
            title="Success!",
            description=f"The account {ctx.author.mention} has been linked to the RIOT ID `{riot_id}`",
            colour=disnake.Colour.green()).set_footer(text="", icon_url=ctx.author.display_avatar)
        )

def setup(bot):
    bot.add_cog(Commands(bot))