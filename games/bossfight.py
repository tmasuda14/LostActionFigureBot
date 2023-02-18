import discord
import time
import random


async def run_bossfight(ctx):
    # await ctx.send("in boss fight")
    bossName = "AKJuggernaut"
    intro_embed = discord.Embed(title=f"BOSS: {bossName}")

    bossHP = ("❤️ " * 10) + ("♡ " * 0)
    # p2_health_bar = ("❤️ " * p2hp) + ("♡ " * (10 - p2hp))

    intro_embed.add_field(name="",
                               value="**{}**\n[{}\n{}\n{}]".format(bossName, bossHP, bossHP, bossHP),
                               inline=False)

    await ctx.send(embed=intro_embed)