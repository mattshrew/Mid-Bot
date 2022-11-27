import random
import time

import asyncio
import disnake
from disnake.ext import commands

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["un", "an", "anagram"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unscramble(self, ctx):
        with open("info/words.txt", "rt") as file:
            word_list = file.read().split('\n')
        
        unscrambled = random.choice(word_list).upper()

        word_temp = list(unscrambled)
        random.shuffle(word_temp)

        scrambled = ' '.join(word_temp)


        embed = disnake.Embed(
            title="Unscramble the Word",
            description=f"You have **20 seconds** to decipher the anagram.",
            colour=disnake.Colour.random()
        ).set_footer(text=f"Executed by {ctx.author}", icon_url=f"{ctx.author.display_avatar}")

        msg = await ctx.send(embed=embed)

        embed.description += f"\n\n**The word you must unscramble is:**\n{scrambled}"

        await asyncio.sleep(2)

        await msg.edit(embed=embed)

        start_time = time.perf_counter()

        def check(m):
            return m.channel == ctx.channel and m.content.upper() == unscrambled


        try:
            answer = await self.bot.wait_for('message', timeout=20, check=check)

        except asyncio.TimeoutError:
            return await ctx.send(embed=disnake.Embed(
                title="Unscramble!",
                description=f"**Failed!**\n> You were unable to guess the word within **20** seconds.\n> The word was `{unscrambled}`.",
                colour=disnake.Colour.red()
                ).set_footer(text=f"Executed by {ctx.author}", icon_url=f"{ctx.author.display_avatar}")
            )
        
        else:
            return await answer.reply(embed=disnake.Embed(
                title="Unscramble The Word",
                description=f"Congratulations {answer.author.mention}, you guessed the word in **{int((time.perf_counter() - start_time) * 100) / 100}** seconds!",
                colour=disnake.Colour.gold()
                ).set_footer(text=f"Executed by {ctx.author}", icon_url=f"{ctx.author.display_avatar}")
            )



    @commands.command(aliases=["typing", "type", "tt"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def typingtest(self, ctx, difficulty: str = None):
        if difficulty == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=disnake.Embed(
                title="Typing Test",
                description="Please specify a difficulty!\n\n**Syntax:**\n```!typingtest <difficulty>```\n**Difficulties:** Easy, Medium, Hard, Extreme",
                colour=disnake.Colour.red()
                ).set_footer(text="<> is a required argument, [] is an optional argument"), delete_after=15)

        difficulty = difficulty.lower()

        if difficulty not in ['easy', 'e', 'medium', 'med', 'm', 'hard', 'h', 'extreme', 'ext', 'e']:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=disnake.Embed(
                title="Typing Test",
                description="Please specify a valid difficulty!\n\n**Syntax:**\n```s!typingtest <difficulty```\n**Difficulties:** Easy, Medium, Hard, Extreme",
                colour=disnake.Colour.red()
                ).set_footer(text="<> is a required argument, [] is an optional argument"), delete_after=15)


        with open("info/sentences.txt", "rt") as file:
            sentence_list = file.read().split('\n')

        easy = [sentence for sentence in sentence_list if len(sentence) < 40]

        medium = [sentence for sentence in sentence_list if 40 <= len(sentence) < 75]

        hard = [sentence for sentence in sentence_list if 75 <= len(sentence) < 120]

        extreme = [sentence for sentence in sentence_list if 120 <= len(sentence)]

        timer = 15

        if difficulty in ["easy", "e"]:
            difficulty = 'Easy'
            sentence = random.choice(easy)

        elif difficulty in ["medium", "med", "m"]:
            difficulty = 'Medium'
            sentence = random.choice(medium)
            
        elif difficulty in ["hard", "h"]:
            difficulty = 'Hard'
            sentence = random.choice(hard)
            timer = round((60 / (375 / len(sentence))) / 5) * 5
            
        elif difficulty in ['extreme', 'ex', 'ext']:
            difficulty = 'Extreme'
            sentence = random.choice(extreme)
            timer = round((60 / (500 / len(sentence))) / 5) * 5

        display_sentence = sentence.replace(' ', u"\u2005")

        embed = disnake.Embed(
            title="Typing Test",
            description=f"Type the following sentence correctly within **{timer} seconds**!",
            color=disnake.Colour.gold()
        ).set_footer(text=f'Executed by {ctx.author} • Difficulty: Easy', icon_url=f'{ctx.author.display_avatar}')

        msg = await ctx.send(embed=embed)

        await asyncio.sleep(2)

        embed.description += f"\n\n{display_sentence}"

        await msg.edit(embed=embed)

        start_time = time.perf_counter()

        def check(m):
            return (m.channel == ctx.channel and m.content in sentence) or (m.channel == ctx.channel and m.author == ctx.author and m.content == display_sentence)


        try:
            answer = await self.bot.wait_for('message', timeout=timer, check=check)

        except asyncio.TimeoutError:
            return await ctx.send(embed=disnake.Embed(
                title="Typing Test",
                description=f"**Failed!** You were unable to type the given text within **{timer} seconds**.",
                color=disnake.Colour.red()
                ).set_footer(text=f'Executed by {ctx.author} • Difficulty: {difficulty}', icon_url=f'{ctx.author.display_avatar}')
            )

        else:
            if answer.content == display_sentence:
                return await ctx.send(embed=disnake.Embed(
                    title="Typing Test",
                    description=f"**Stop Cheating!** Do not copy and paste the text.",
                    color=disnake.Colour.dark_red()
                    ).set_footer(text=f'Executed by {ctx.author} • Difficulty: {difficulty}', icon_url=f'{ctx.author.display_avatar}')
                )
            
            return await ctx.send(embed=disnake.Embed(
                title="Typing Test",
                description=f"**Congratulations** {answer.author.mention}, you correctly typed the given text in **{int((time.perf_counter() - start_time) * 100) / 100} seconds**, at a rate of **{int(len(sentence.split()) / (time.perf_counter() - start_time) * 60)}** words per minute!",
                color=disnake.Colour.green()
                ).set_footer(text=f'Executed by {ctx.author} • Difficulty: {difficulty}', icon_url=f'{ctx.author.display_avatar}')
            )

def setup(bot):
    bot.add_cog(Games(bot))