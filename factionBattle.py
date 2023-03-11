import discord
import random
import time
from fbTournament import run_tournament
from phrases.massCasualty import mass_casualty_phrases

original_heroes = []
original_villains = []
game_winner = None


async def runFactionBattle(ctx, contestant_list):
    global original_heroes, original_villains, game_winner
    player_count = len(contestant_list)
    h_v = chunkify(contestant_list, 2)

    hero_list = h_v[0]
    villain_list = h_v[1]
    original_heroes = hero_list.copy()
    original_villains = villain_list.copy()
    await printPlayers(ctx, hero_list, villain_list)
    time.sleep(6)
    battle_round_embed = discord.Embed(title="Heroes vs. Villains!", description="")
    battle_round_embed.set_image(url="./src/LostLogo.jpeg")
    br_embed_msg = await ctx.send(embed=battle_round_embed)
    time.sleep(2)
    embed_count = 0
    while player_count > 1:
        if len(hero_list) == 0:
            if len(villain_list) <= 4:
                await printPlayers(ctx, hero_list, villain_list)
                time.sleep(5)
                players_remaining = len(villain_list)
                tourney_intro = discord.Embed(title="All Heroes have been defeated!",
                                              description=f"The remaining {players_remaining} players will fight 1v1, "
                                                          f"single elimination!")
                tourney_intro.add_field(name="", value="Beginning the Tournament of Villains...")
                await ctx.send(embed=tourney_intro)
                time.sleep(6)
                game_winner = await run_tournament(ctx, villain_list)
                await printWinner(ctx, [], original_villains)
                return
            else:
                # await printPlayers(ctx, hero_list, villain_list)
                players_killed = await singleTeamBattleRounds(ctx, villain_list, "villain")
                player_count -= players_killed

        elif len(villain_list) == 0:
            if len(hero_list) <= 4:
                await printPlayers(ctx, hero_list, villain_list)
                time.sleep(5)
                players_remaining = len(hero_list)
                tourney_intro = discord.Embed(title="All Villains have been defeated!",
                                              description=f"The remaining {players_remaining} players will fight 1v1, "
                                                          f"single elimination!")
                tourney_intro.add_field(name="", value="Beginning the Tournament of Heroes...")
                await ctx.send(embed=tourney_intro)
                time.sleep(6)
                game_winner = await run_tournament(ctx, hero_list)
                await printWinner(ctx, original_heroes, [])
                return
            else:
                players_killed = await singleTeamBattleRounds(ctx, hero_list, "hero")
                player_count -= players_killed

        elif player_count <= 4:
            await printPlayers(ctx, hero_list, villain_list)
            time.sleep(5)
            players_remaining = len(villain_list) + len(hero_list)
            tourney_intro = discord.Embed(title="Only a few challengers remain!",
                                          description=f"The remaining {players_remaining} players will fight 1v1, "
                                                      f"single elimination!")
            tourney_intro.add_field(name="", value="Beginning the Tournament of Legends...")

            await ctx.send(embed=tourney_intro)
            time.sleep(6)
            game_winner = await run_tournament(ctx, (hero_list + villain_list))
            if game_winner in original_heroes:
                await printWinner(ctx, original_heroes, [])
            else:
                await printWinner(ctx, [], original_villains)
            # await printWinner(ctx, hero_list, villain_list)

            return

        else:
            if embed_count >= 3:
                battle_round_embed = discord.Embed(title="", description="🩸")
                br_embed_msg = await ctx.send(embed=battle_round_embed)
                embed_count = 0
            players_killed = await battleRounds(hero_list, villain_list, br_embed_msg, battle_round_embed)
            player_count -= players_killed
            embed_count += 1


def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end


async def battleRounds(hero_list, villain_list, br_msg, br_embed):
    kill_count = 0
    match random.randint(1, 2):
        case 1:
            champion = random.choice(hero_list)
            number_of_kills = random.randint(1, 4)
            dead_players = ""
            for dead_player in range(number_of_kills):
                if len(villain_list) == 0:
                    break
                random.shuffle(villain_list)
                random_kill = villain_list.pop()
                dead_players += random_kill.name + ", "
                kill_count += 1
            dead_players = dead_players.rstrip(', ')
            if number_of_kills == 2:
                dead_players = replace_last(dead_players, ',', ' and ')
            elif number_of_kills > 2:
                dead_players = replace_last(dead_players, ',', ', and ')
            mass_casualty_phrase = random.choice(mass_casualty_phrases)
            br_embed.add_field(name="", value=f"🇭 **{champion.name}**{mass_casualty_phrase}~~{dead_players}~~!", inline=False)
            await br_msg.edit(embed=br_embed)
            time.sleep(3.5)
            return kill_count
        case 2:
            champion = random.choice(villain_list)
            number_of_kills = random.randint(1, 4)
            dead_players = ""
            for dead_player in range(number_of_kills):
                if len(hero_list) == 0:
                    break
                random.shuffle(hero_list)
                random_kill = hero_list.pop()

                dead_players += random_kill.name + ", "

                kill_count += 1
            dead_players = dead_players.rstrip(', ')
            if number_of_kills == 2:
                dead_players = replace_last(dead_players, ',', ' and ')
            elif number_of_kills > 2:
                dead_players = replace_last(dead_players, ',', ', and ')
            mass_casualty_phrase = random.choice(mass_casualty_phrases)
            br_embed.add_field(name="", value=f"🇻 **{champion.name}**{mass_casualty_phrase}~~{dead_players}~~!", inline=False)
            await br_msg.edit(embed=br_embed)
            time.sleep(3.5)
            return kill_count


async def singleTeamBattleRounds(ctx, warrior_list, emoji_name):
    battle_round_embed = discord.Embed(title="", description="🩸")
    br_embed_msg = await ctx.send(embed=battle_round_embed)
    kill_count = 0
    if emoji_name == "hero":
        emoji = "🇭"
    else:
        emoji = "🇻"
    while len(warrior_list) > 4:
        random.shuffle(warrior_list)
        champion = warrior_list[0]
        number_of_kills = random.randint(1, 3)
        dead_players = ""
        for dead_player in range(number_of_kills):
            if len(warrior_list) <= 1:
                break
            random_kill = warrior_list.pop()
            dead_players += random_kill.name + ", "
            kill_count += 1
        dead_players = dead_players.rstrip(', ')
        if number_of_kills == 2:
            dead_players = replace_last(dead_players, ',', ' and ')
        elif number_of_kills > 2:
            dead_players = replace_last(dead_players, ',', ', and ')
        mass_casualty_phrase = random.choice(mass_casualty_phrases)
        battle_round_embed.add_field(name="", value=f"{emoji} {champion.name}{mass_casualty_phrase}~~{dead_players}~~!", inline=False)
        await br_embed_msg.edit(embed=battle_round_embed)
        time.sleep(3.5)
    # time.sleep(3)
    return kill_count


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


async def printPlayers(ctx, hero_list, villain_list):
    hero_names = ""
    hero_count = 0
    contestants_embed = discord.Embed(title="Contestant List:", description="")
    contestants_embed.add_field(name="**Heroes**", value="", inline=False)

    if len(hero_list) == 0:
        contestants_embed.add_field(name="DEFEATED!", value="", inline=False)
    else:
        for player in hero_list:
            hero_names += player.mention + ", "
            hero_count += 1
            if hero_count == 20:
                hero_names = hero_names.rstrip(', ')
                contestants_embed.add_field(name="", value=f"{hero_names}", inline=False)
                hero_names = ""
                hero_count = 0
        if hero_count != 0:
            hero_names = hero_names.rstrip(', ')
            contestants_embed.add_field(name="", value=f"{hero_names}", inline=False)

    villain_names = ""
    villain_count = 0
    contestants_embed.add_field(name="**Villains**", value="", inline=False)

    if len(villain_list) == 0:
        contestants_embed.add_field(name="DEFEATED!", value="", inline=False)
    else:
        for player in villain_list:
            villain_names += player.mention + ", "
            villain_count += 1
            if villain_count == 20:
                villain_names = villain_names.rstrip(', ')
                contestants_embed.add_field(name="", value=f"{villain_names}", inline=False)
                villain_names = ""
                villain_count = 0
        if villain_count != 0:
            villain_names = villain_names.rstrip(', ')
            contestants_embed.add_field(name="", value=f"{villain_names}", inline=False)
    # await ctx.send(embed=contestants_embed2)
    await ctx.send(embed=contestants_embed)


async def printWinner(ctx, hero_list, villain_list):
    global original_heroes, original_villains
    if len(hero_list) == 0:
        winner_embed = discord.Embed(title=f"**VILLAINS win the Faction Battle!**", description="")
        villain_names = ""
        villain_count = 0
        for player in original_villains:
            villain_names += player.mention + ", "
            villain_count += 1
            if villain_count == 20:
                villain_names = villain_names.rstrip(', ')
                winner_embed.add_field(name="", value=f"{villain_names}", inline=False)
                villain_names = ""
                villain_count = 0
        if villain_count != 0:
            villain_names = villain_names.rstrip(', ')
            winner_embed.add_field(name="", value=f"{villain_names}", inline=False)
        winner = villain_list[0].mention

        winner_embed.add_field(name="", value=f"MVP: {winner}")
        await ctx.send(embed=winner_embed)
    else:
        winner_embed = discord.Embed(title=f"**HEROES win the Faction Battle!**", description="")
        hero_names = ""
        hero_count = 0
        for player in original_heroes:
            hero_names += player.mention + ", "
            hero_count += 1
            if hero_count == 20:
                hero_names = hero_names.rstrip(', ')
                winner_embed.add_field(name="", value=f"{hero_names}", inline=False)
                hero_names = ""
                hero_count = 0
        if hero_count != 0:
            hero_names = hero_names.rstrip(', ')
            winner_embed.add_field(name="", value=f"{hero_names}", inline=False)
        winner = hero_list[0].mention

        winner_embed.add_field(name="", value=f"MVP: {winner}")
        await ctx.send(embed=winner_embed)
    await ctx.send(f"**{winner}**")


async def runTournamentOf(combatant_list):
    print(combatant_list)
