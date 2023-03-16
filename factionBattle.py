import discord
import random
import time
import os
from fbTournament import run_tournament
from phrases.massCasualty import mass_casualty_phrases
from src.legendList import legends

original_heroes = []
original_villains = []
game_winner = None
# current_event_message = None
legend_list = legends


async def runFactionBattle(ctx, contestant_list, event_selections, current_event_msg):
    global original_heroes, original_villains, game_winner, legend_list
    player_count = len(contestant_list)
    h_v = chunkify(contestant_list, 2)
    hero_list = h_v[0]
    villain_list = h_v[1]
    original_heroes = hero_list.copy()
    original_villains = villain_list.copy()
    await printPlayers(ctx, hero_list, villain_list)
    time.sleep(6)

    battle_round_embed = discord.Embed(title="Heroes vs. Villains!", description="")
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

                # run Legend events here
                print(event_selections)

                for choice in event_selections:
                    choice.clear()
                players_killed = await runLegendEvent(ctx, hero_list, villain_list, current_event_msg, event_selections)
                player_count -= players_killed
                print(event_selections)

                # await calculateDeaths(ctx, hero_list, villain_list, event_selections)
                for choice in event_selections:
                    choice.clear()
                time.sleep(3)
                battle_round_embed = discord.Embed(title="", description="The battle continues...")
                br_embed_msg = await ctx.send(embed=battle_round_embed)
                embed_count = 0
            else:
                players_killed = await battleRounds(hero_list, villain_list, br_embed_msg, battle_round_embed)
                player_count -= players_killed
                embed_count += 1
    if player_count < 1:
        await ctx.send("...Everyone DIED?!")

# async def calculateDeaths(ctx, hero_list, villain_list, event_selections):
    # await ctx.send(event_selections)
    # kill_choice =


async def runLegendEvent(ctx, hero_list, villain_list, current_event_msg, event_selections):
    global legend_list
    # legend_list = legends
    if len(legend_list) == 0:
        return 0
    random.shuffle(legend_list)
    legend = legend_list.pop()
    y = legend.get("img_src")
    j = legend.get("embed_file_name")
    file = discord.File(f"{y}", filename=f"{j}")
    z = legend.get("embed_quote")
    legend_embed = discord.Embed(title="A Legend approaches...", description=f"{z}")
    legend_embed.set_image(url=f"attachment://{j}")

    legend_intro_msg = await ctx.send(embed=legend_embed, file=file)

    b = legend.get("embed_value")
    legend_embed2 = discord.Embed(title="", description=f"{b}")

    legend_msg = await ctx.send(embed=legend_embed2, delete_after=10)
    x = legend.get("embed_emoji1")
    await legend_msg.add_reaction(f"{x}")
    a = legend.get("embed_emoji2")
    await legend_msg.add_reaction(f"{a}")
    c = legend.get("embed_emoji3")
    await legend_msg.add_reaction(f"{c}")

    time.sleep(10)
    dead_players_len = 0
    death_choice = random.choice([0, 1, 2])
    player_choice = legend.get("embed_choices")[death_choice]
    legend_results_embed = discord.Embed(title=f"The players who {player_choice}", description="")
    dead_players = event_selections[death_choice]
    # await ctx.send(event_selections)
    # await ctx.send(dead_players)
    time.sleep(1)
    if dead_players:
        # dead_players_len = len(dead_players)
        dead_player_string = "Dead warriors: "
        for player in dead_players:
            dead_players_len += 1
            if player in hero_list:
                hero_list.remove(player)
            elif player in villain_list:
                villain_list.remove(player)
            dead_player_string += player.name + ", "
        dead_player_string = dead_player_string.rstrip(', ')
        legend_results_embed.add_field(name="", value=f"~~{dead_player_string}~~")
    else:
        legend_results_embed.add_field(name="", value="Nobody died!")
    await ctx.send(embed=legend_results_embed)

    print(dead_players_len)
    return dead_players_len


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
            br_embed.add_field(name="", value=f"🅷 | **{champion.name}**{mass_casualty_phrase}~~{dead_players}~~!", inline=False)
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
            br_embed.add_field(name="", value=f"🆅 | **{champion.name}**{mass_casualty_phrase}~~{dead_players}~~!", inline=False)
            await br_msg.edit(embed=br_embed)
            time.sleep(3.5)
            return kill_count


async def singleTeamBattleRounds(ctx, warrior_list, emoji_name):
    battle_round_embed = discord.Embed(title="", description="The battle continues...")
    br_embed_msg = await ctx.send(embed=battle_round_embed)
    kill_count = 0
    if emoji_name == "hero":
        emoji = "🅷"
    else:
        emoji = "🆅"
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
        battle_round_embed.add_field(name="", value=f"{emoji} | {champion.name}{mass_casualty_phrase}~~{dead_players}~~!", inline=False)
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
    file = discord.File("./src/LostLogo.jpeg", filename="LostLogo.jpeg")
    contestants_embed.set_thumbnail(url="attachment://LostLogo.jpeg")
    contestants_embed.add_field(name="**Heroes**", value="", inline=False)

    if len(hero_list) == 0:
        contestants_embed.add_field(name="", value="DEFEATED!", inline=False)
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
        contestants_embed.add_field(name="", value="DEFEATED!", inline=False)
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
    await ctx.send(file=file, embed=contestants_embed)


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
