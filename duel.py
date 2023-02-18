import discord
import time
import random
import math


async def run_duel(player1, player2, ctx):
    # file = discord.File("./src/knives.png", filename="knives.png")
    embed = discord.Embed(title="Lost Duel")
    embed.add_field(name="", value="{} vs {}".format(player1, player2))
    # embed.set_image(url="attachment://knives.png")
    # await ctx.send(embed=embed, file=file)
    await ctx.send(embed=embed)
    p1hp = 10
    p2hp = 10

    while p1hp > 0 or p2hp > 0:

        embed_indv_match = discord.Embed()
        p1_attack = random.randint(1, 4)
        p2_attack = random.randint(1, 4)
        p1_announcement = "hit"
        p2_announcement = "hit"
        rand_val = random.randint(1, 10)

        if rand_val >= 9:
            crit = True
        else:
            crit = False
        if crit:
            if p1_attack > p2_attack:
                p1_announcement = "CRITICALLY HIT"
                p2_announcement = "hit"
                p1_attack += 2
            else:
                p2_announcement = "CRITICALLY HIT"
                p1_announcement = "hit"
                p2_attack += 2

        p1hp -= p2_attack
        p2hp -= p1_attack

        if p1hp < 0:
            p1hp = 0
        if p2hp < 0:
            p2hp = 0

        p1_health_bar = ("❤️ " * p1hp) + ("♡ " * (10 - p1hp))
        p2_health_bar = ("❤️ " * p2hp) + ("♡ " * (10 - p2hp))

        # embed_indv_match.add_field(name="",
        #                            value="**{}** {} **{}** for **{}** damage!"
        #                                  "\n**{}** {} **{}** for **{}** damage!".format(
        #                                    player1,
        #                                    p1_announcement,
        #                                    player2,
        #                                    p1_attack,
        #                                    player2,
        #                                    p2_announcement,
        #                                    player1,
        #                                    p2_attack),
        #                            inline=False)
        # embed_indv_match.add_field(name="".format(),
        #                            value="=================\n**{}**\n[{}]\n\n\n**{}**\n[{}] ".format(player1,
        #                                                                                   p1_health_bar,
        #                                                                                   player2,
        #                                                                                   p2_health_bar),
        #                            inline=False)
        embed_indv_match.add_field(name="",
                                   value="**{}** gets {} for **{}** damage!\n[{}]\n"
                                         "**{}** gets {} for **{}** damage!\n[{}]".format(player1,
                                                                                          p1_announcement,
                                                                                          p2_attack,
                                                                                          p1_health_bar,
                                                                                          player2,
                                                                                          p2_announcement,
                                                                                          p1_attack,
                                                                                          p2_health_bar),
                                   inline=False)
        await ctx.send(embed=embed_indv_match)

        if p2hp == 0 or p1hp == 0:
            break
        else:
            time.sleep(4)

    winner = ""
    if p1hp == 0 and p2hp == 0:
        p1_attack = random.randint(1, 4)
        p2_attack = random.randint(1, 4)
        while p1_attack == p2_attack:
            p1_attack = random.randint(1, 4)
            p2_attack = random.randint(1, 4)

        if p1_attack > p2_attack:
            winner = player1
        else:
            winner = player2
        embed_sudden_death = discord.Embed(title="Sudden Death!")
        embed_sudden_death.add_field(name="", value="{} hit for {}, {} hit for {}!".format(
            player1, p1_attack, player2, p2_attack
        ))
        await ctx.send(embed=embed_sudden_death)
        time.sleep(2.5)
    else:
        if p1hp == 0:
            winner = player2
        elif p2hp == 0:
            winner = player1
        else:
            print("error shouldn't get here?")
    embed_final = discord.Embed(title="{} wins!".format(winner))
    await ctx.send(embed=embed_final)
