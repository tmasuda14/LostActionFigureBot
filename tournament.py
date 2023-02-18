import discord
import time
import random
from phrases.battlePhrases import battle_phrases

this_round = []
next_round = []
sleepTime = 6.25
players = []
specialRound = []
matchColors = [0x4e6a82, 0x7d7452, 0x741b52, 0x824e63, 0x4e5f82, 0x6da9ab]


async def run_tournament(ctx, contestants: list):
    global this_round, next_round, sleepTime, players
    # contestants.append("del bud2")
    players = contestants.copy()

    print(players)
    print("printed players")

    # if len(contestants) <= 2:

    # contestants.append("Hurk")
    # contestants.append("Ray")
    # contestants.append("Ace")

    # contestants.append("Del EEET1")
    # contestants.append("del eeet2")
    # contestants.append("Del EEET3")
    # contestants.append("del eeet4")
    # contestants.append("Del EEET5")
    # contestants.append("del eeet6")
    # contestants.append("Del EEET7")
    # contestants.append("del eeet8")
    # contestants.append("Del EEET9")
    # contestants.append("del eeet10")
    # contestants.append("Del EEET11")
    # contestants.append("del eeet12")
    # contestants.append("Del EEET13")
    # contestants.append("del eeet14")
    # contestants.append("Del EEET15")
    # contestants.append("del eeet16")
    # contestants.append("Del EEET17")
    # contestants.append("del eeet18")
    # contestants.append("Del EEET19")
    # contestants.append("del eeet20")
    # contestants.append("Del EEET21")
    # contestants.append("del eeet22")
    # contestants.append("Del EEET23")
    # contestants.append("del eeet24")
    # contestants.append("Del EEET25")
    # contestants.append("del eeet26")
    # contestants.append("Del EEET27")
    # contestants.append("del eeet28")
    # contestants.append("Del EEET29")

    if len(contestants) == 2:
        contestants.append("Ace")
        contestants.append("Hurk")
    elif len(contestants) == 3:
        contestants.append("Ace")
    elif len(contestants) != 4:
        match (len(contestants) % 8):
            case 7:
                contestants.append("Ace")
            case 6:
                contestants.append("Ace")
                contestants.append("Hurk")
            case 5:
                contestants.append("Ace")
                contestants.append("Hurk")
                contestants.append("Chet")
            case 4:
                contestants.append("Ace")
                contestants.append("Hurk")
                contestants.append("Chet")
                contestants.append("Flynn")
            case 3:
                contestants.append("Ace")
                contestants.append("Hurk")
                contestants.append("Chet")
                contestants.append("Flynn")
                contestants.append("Hitch")
            case 2:
                contestants.append("Ace")
                contestants.append("Hurk")
                contestants.append("Chet")
                contestants.append("Flynn")
                contestants.append("Hitch")
                contestants.append("Ray")
            case 1:
                contestants.append("Ace")
                contestants.append("Hurk")
                contestants.append("Chet")
                contestants.append("Flynn")
                contestants.append("Hitch")
                contestants.append("Ray")
                contestants.append("AKJ Bot")
            case 0:
                pass
    if len(contestants) % 2 != 0:
        contestants.append("The Sad Troll")
    random.shuffle(contestants)
    print(contestants)
    if len(contestants) > 20:
        sleepTime = 5.0
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
        matchColor = (matchColors[(5 + round_num) % 6])
        print(f"match num: {match_num}\n matchColor: {matchColor}")
        while len(this_round) > 1:
            player1 = this_round.pop()
            player2 = this_round.pop()
            winner = None
            p1hp = 6
            p2hp = 6
            embed_match = discord.Embed(title=f"⚔️ **{player1}** 🆚 **{player2}** ⚔️",
                                        description=f"",
                                        color=matchColor)
            if player1 == 'The Sad Troll':
                embed_match.add_field(name=f"{player2} easily defeated the {player1}",
                                      value="",
                                      inline=False)
                next_round.append(player2)
                match_num += 1
                await ctx.send(embed=embed_match)
                time.sleep(4)
            elif player2 == 'The Sad Troll':
                embed_match.add_field(name=f"{player1} easily defeated the {player2}",
                                      value="",
                                      inline=False)
                next_round.append(player1)
                match_num += 1
                await ctx.send(embed=embed_match)
                time.sleep(4)
            else:
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
                    embed_match.add_field(name=f"**{player1}**{p1_attack_phrase}",
                                          value=f"[{p1_health_bar}] **(-{p2_attack})**\n",
                                          inline=False)
                    embed_match.add_field(name=f"**{player2}**{p2_attack_phrase}",
                                          value=f"[{p2_health_bar}] **(-{p1_attack})**\n\n",
                                          inline=False)
                    # embed_match.add_field(name="", value="ㅤ", inline=False)
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
                        time.sleep(2.5)
                        winner = player2
                        suddenDeath = True
                    # embed_sudden_death = discord.Embed(title="Sudden Death!")
                    # await ctx.send(embed=embed_sudden_death)
                    embed_match.add_field(name="**Sudden Death!**",
                                          value=f"**{player1}** dealt {p1_attack} damage, **{player2}** dealt {p2_attack} damage!")

                else:
                    if p1hp == 0:
                        winner = player2
                    elif p2hp == 0:
                        winner = player1
                    else:
                        print("Tournament Runtime Error.")
                #
                # if winner in players:
                embed_match.add_field(name=f"{winner} wins match {match_num}!",
                                      value="",
                                      inline=False)
                # else:
                #     embed_match.add_field(name=f"{winner} wins match {match_num}!",
                #                           value="",
                #                           inline=False)
                await ctx.send(embed=embed_match)
                cur_winner = winner
                next_round.append(winner)
                print("next round building:")
                print(next_round)
                if len(next_round) == 1 and len(this_round) == 0:
                    running = False
                match_num += 1
                time.sleep(sleepTime)
        round_num += 1
    print(players)
    print("printed players")
    print(cur_winner)
    print("printed cur_winner")
    if cur_winner not in players:
        winner = None
        p1_health = 10
        p2_health = 10
        p1 = players.pop(random.randrange(len(players)))
        p2 = players.pop(random.randrange(len(players)))
        print(p1, p2)
        print("printed p1,p2")
        embed_ind_match_intro = discord.Embed(title="Bonus Round",
                                              description=f"{cur_winner} summons **{p1}** and **{p2}**"
                                                          " from the grave to fight to the death!",
                                              color=0x19b5a5)
        await ctx.send(embed=embed_ind_match_intro)
        time.sleep(3)
        while p1_health > 0 or p2_health > 0:
            embed_ind_match = discord.Embed(title="", description=f"", color=0x19b5a5)
            p1_attack = random.randint(1, 6)
            p2_attack = random.randint(1, 6)

            p1_health -= p2_attack
            p2_health -= p1_attack

            if p1_health < 0:
                p1_health = 0
            if p2_health < 0:
                p2_health = 0

            p1_health_bar = ("❤️ " * p1_health) + ("♡ " * (10 - p1_health))
            p2_health_bar = ("❤️ " * p2_health) + ("♡ " * (10 - p2_health))

            p1_attack_phrase = random.choice(battle_phrases)
            p2_attack_phrase = random.choice(battle_phrases)

            embed_ind_match.add_field(name=f"**{p1}**{p1_attack_phrase}",
                                      value=f"[{p1_health_bar}] **(-{p2_attack})**\n",
                                      inline=False)
            embed_ind_match.add_field(name=f"**{p2}**{p2_attack_phrase}",
                                      value=f"[{p2_health_bar}] **(-{p1_attack})**\n\n",
                                      inline=False)
            await ctx.send(embed=embed_ind_match)
            time.sleep(3)
            if p1_health == 0 or p2_health == 0:
                break
        if p1_health == 0 and p2_health == 0:
            p1_attack = random.randint(1, 6)
            p2_attack = random.randint(1, 6)
            while p1_attack == p2_attack:
                p1_attack = random.randint(1, 6)
                p2_attack = random.randint(1, 6)
            if p1_attack > p2_attack:
                winner = p1
            else:
                time.sleep(1.5)
                winner = p2
                embed_match = discord.Embed()
                embed_match.add_field(name="Sudden Death!", value=f"**{p1}** dealt {p1_attack} damage, **{p2}** dealt {p2_attack} damage!")
                await ctx.send(embed=embed_match)
                time.sleep(3)
        else:
            if p1_health == 0:
                winner = p2
            elif p2_health == 0:
                winner = p1
            else:
                print("Tournament Error.")
        embed = discord.Embed(title="CHAMPION!!!", description="🗡️ 👑 🛡️", color=0x00ff00)
        embed.add_field(name=f"{winner} wins the tournament!", value="", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="CHAMPION!!!", description="🗡️ 👑 🛡️", color=0x00ff00)
        embed.add_field(name=f"{cur_winner} wins the tournament!", value="", inline=False)
        await ctx.send(embed=embed)
