import asyncio
import disnake
import traceback
from disnake.ext import commands, tasks

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(776506655646941217)
        welcome = disnake.Embed(
            title=f"Welcome to the server!", 
            description=f"**It's great to have you, {member.mention}!**\n> This is a server with the purpose of testing many bots, commands, and features.\n> Enjoy your stay!", 
            colour=disnake.Colour.teal())

        return await channel.send(embed=welcome)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(776506655646941217)
        goodbye = disnake.Embed(
            description=f"**{member.mention} has left the server.**", 
            colour=disnake.Colour.red())
            
        return await channel.send(embed=goodbye)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            command = str(error).split()[1][1:-1]
            if '!' in command or '?' in command:
                return
            await ctx.message.add_reaction('❌')

            return await ctx.send(embed=disnake.Embed(
                title="Command not found!",
                description=f"<:alert:1038471201938489424> The command `{command}` doesn't exist!",
                colour=disnake.Colour.red()).set_footer(text="", icon_url=ctx.author.display_avatar))

        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.add_reaction('❌')
            member = str(error).split()[1][1:-1]

            return await ctx.send(embed=disnake.Embed(
                title="Member not found!",
                description=f"<:alert:1038471201938489424> Could not find member: `{member}`",
                colour=disnake.Colour.red()).set_footer(text="", icon_url=ctx.author.display_avatar))
        elif isinstance(error, commands.MissingRequiredArgument):
            argument = str(error).split()[0]
            await ctx.message.add_reaction('❌')

            return await ctx.send(embed=disnake.Embed(
                title="Missing Argument!",
                description=f"<:alert:1038471201938489424> Please specify `{argument}`\n\n**Proper Usage:**\n```{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}```",
                colour=disnake.Colour.red()).set_footer(text="", icon_url=ctx.author.display_avatar))

        elif isinstance(error, commands.MissingRole):
            await ctx.message.add_reaction('❌')

            return await ctx.send(embed=disnake.Embed(
                title="Missing Roles!", 
                description="<:alert:1038471201938489424> You do not have the roles required to execute this command!",
                colour=disnake.Colour.red()).set_footer(text="", icon_url=ctx.author.display_avatar))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('❌')

            return await ctx.send(embed=disnake.Embed(
                title="Missing Permissions!",
                description=f"<:alert:1038471201938489424> You do not have the permissions to execute this command!",
                colour=disnake.Colour.red()).set_footer(text="", icon_url=ctx.author.display_avatar))

        elif isinstance(error, commands.NotOwner):
            await ctx.message.add_reaction('❌')
            
            return await ctx.send("<:alert:1038471201938489424> You do not own this bot!")

        else:
            channel = self.bot.get_channel(1038469906695458836)
            await channel.send(
                f"{ctx.author.name} caused an error.\n```py\n{''.join(traceback.format_exception(error, value=error, tb=None))}\n```")
            raise error


def setup(bot):
    bot.add_cog(Events(bot))