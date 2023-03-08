import discord
import time
import random
from phrases.battlePhrases import battle_phrases

this_round = []
next_round = []
sleepTime = 2.5
players = []
specialRound = []
matchColors = [0x4e6a82, 0x7d7452, 0x741b52, 0x824e63, 0x4e5f82, 0x6da9ab]


async def run_tournament(ctx, contestants: list):
    global this_round, next_round, sleepTime, players
    players = contestants.copy()

    print(players)
    print("printed initial players above, and updated players below")

    round_num = 1
    next_round = contestants
    match_num = 1
    cur_winner = None
    running = True

    while running:
        cur_winner = None
        embed_intro = discord.Embed(title=f"====== ROUND {round_num} ======", color=0x31802f)
        await ctx.send(embed=embed_intro)
        time.sleep(0.5)
        this_round = next_round
        next_round = []
        print("in while running")
        print(this_round)
        if len(this_round) == 3:
            this_round.append("The Sad Troll")
        if len(this_round) % 2 != 0:
            this_round.append("The Sad Troll")
        matchColor = (matchColors[(5 + round_num) % 6])
        while len(this_round) > 1:
            player1 = this_round.pop()
            player2 = this_round.pop()
            winner = None
            p1hp = 6
            p2hp = 6

            if player1 == 'The Sad Troll':
                embed_match = discord.Embed(title=f"⚔️  **{player1}** 🆚 **{player2.name}**  ⚔️ \n",
                                            description=f"",
                                            color=matchColor)
                embed_match.add_field(name="", value="ㅤ", inline=False)
                embed_match.add_field(name=f"{player2.name} easily defeated the {player1}",
                                      value="",
                                      inline=False)
                next_round.append(player2)
                match_num += 1
                await ctx.send(embed=embed_match)
                time.sleep(3)
            elif player2 == 'The Sad Troll':
                embed_match = discord.Embed(title=f"⚔️  **{player1.name}** 🆚 **{player2}**  ⚔️ \n",
                                            description=f"",
                                            color=matchColor)
                embed_match.add_field(name="", value="ㅤ", inline=False)
                embed_match.add_field(name=f"{player1.name} easily defeated the {player2}",
                                      value="",
                                      inline=False)
                next_round.append(player1)
                match_num += 1
                await ctx.send(embed=embed_match)
                time.sleep(3)
            else:
                embed_match = discord.Embed(title=f"⚔️  **{player1.name}** 🆚 **{player2.name}**  ⚔️ \n",
                                            description=f"",
                                            color=matchColor)
                embed_match.add_field(name="", value="ㅤ", inline=False)
                msg = await ctx.send(embed=embed_match)
                time.sleep(3)

                while p1hp > 0 or p2hp > 0:
                    p1_attack = random.randint(1, 6)
                    p2_attack = random.randint(1, 6)

                    p1hp -= p2_attack
                    p2hp -= p1_attack

                    if p1hp < 0:
                        p1hp = 0
                    if p2hp < 0:
                        p2hp = 0
                    p1_health_bar = ("❤️ " * p1hp) + ("♡ " * (6 - p1hp))
                    p2_health_bar = ("❤️ " * p2hp) + ("♡ " * (6 - p2hp))

                    p1_attack_phrase = random.choice(battle_phrases)
                    p2_attack_phrase = random.choice(battle_phrases)

                    embed_match.add_field(name=f"",
                                          value=f"**{player1.name}** {p1_attack_phrase}\n[{p1_health_bar}] **(-{p2_attack})**",
                                          inline=False)
                    await msg.edit(embed=embed_match)
                    time.sleep(3.125)
                    embed_match.add_field(name=f"",
                                          value=f"**{player2.name}** {p2_attack_phrase}\n[{p2_health_bar}] **(-{p1_attack})**",
                                          inline=False)
                    await msg.edit(embed=embed_match)
                    time.sleep(3.125)

                    if p2hp == 0 or p1hp == 0:
                        break
                if p1hp == 0 and p2hp == 0:
                    p1_attack = random.randint(1, 6)
                    p2_attack = random.randint(1, 6)
                    while p1_attack == p2_attack:
                        p1_attack = random.randint(1, 6)
                        p2_attack = random.randint(1, 6)
                    if p1_attack > p2_attack:
                        winner = player1
                    else:
                        time.sleep(1.5)
                        winner = player2
                    embed_match.add_field(name="**Sudden Death!**", value="👀", inline=False)
                    await msg.edit(embed=embed_match)
                    time.sleep(3.5)
                    embed_match.add_field(name="",
                                          value=f"**{player1.name}** dealt {p1_attack} damage,"
                                                f" **{player2.name}** dealt {p2_attack} damage!",
                                          inline=False)
                    await msg.edit(embed=embed_match)
                    time.sleep(3)
                else:
                    if p1hp == 0:
                        winner = player2
                    elif p2hp == 0:
                        winner = player1
                    else:
                        print("Tournament Runtime Error.")
                embed_match.add_field(name="", value="", inline=False)
                embed_match.add_field(name=f"**{winner.name}** wins the match!", value="", inline=False)
                await msg.edit(embed=embed_match)
                cur_winner = winner
                next_round.append(winner)
                print("next round building:")
                print(next_round)
                if len(next_round) == 1 and len(this_round) == 0:
                    running = False
                match_num += 1
                time.sleep(sleepTime)
        round_num += 1

    embed = discord.Embed(title=f"{cur_winner.name} is CHAMPION!!!", description="🗡️ 👑 🛡️", color=0x00ff00)
    await ctx.send(embed=embed)
