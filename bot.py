import discord
import os
# from warriorSelectView import WarriorView
from duel import run_duel
from tournament import run_tournament
from factionBattle import runFactionBattle
from dotenv import load_dotenv
import time

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

game_slash = discord.SlashCommandGroup("games", "Lost Action Figure Games")
tournament_slash = discord.SlashCommandGroup("tournament", "LAF Tournament")
duel_slash = discord.SlashCommandGroup("duel", "Start a Duel")
faction_battle_slash = discord.SlashCommandGroup("factionbattle", "Heroes vs. Villains!")

duel_running = False
signup_message = None
tournament_contestants = []
duelists = {}
duel_message = None
tournament_running = False
factionBattleContestants = []
factionSignupMessage = None


@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")


@bot.event
async def on_reaction_add(reaction, user):
    global duel_running, signup_message, duelists

    if reaction.emoji == "✅":
        if reaction.message.id != signup_message.id:
            return
        if user.name != "Lost Action Figure Bot":
            await signup_message.channel.send(f"A new challenger appears: {user.name}!")
            tournament_contestants.append(user.name)
    elif reaction.emoji == "🤺":
        if duelists.get(reaction.message.id) is None:
            return
        if user.name != "Lost Action Figure Bot":
            duel_running = True
            await run_duel(user.name,
                           (duelists.get(reaction.message.id))[0].author.name,
                           reaction.message.channel)
            duel_running = False
    elif reaction.emoji == "🤺":
        if duelists.get(reaction.message.id) is None:
            return
        if user.name != "Lost Action Figure Bot":
            duel_running = True
            await run_duel(duelists.get(reaction.message.id)[1],
                           (duelists.get(reaction.message.id)).author.name,
                           reaction.message.channel)
            duel_running = False
    elif reaction.emoji == "🆚":
        if reaction.message.id != factionSignupMessage.id:
            return
        if user.name != "Lost Action Figure Bot":
            factionBattleContestants.append(user)
            print(factionBattleContestants)
            await reaction.message.channel.send(f">>TESTING>> Added {user.mention} to the faction battle.")


@faction_battle_slash.command(name="signup", description="Faction Battle Signups!")
async def factionBattle(ctx):
    global factionSignupMessage
    await ctx.respond("Beginning the faction battle!")
    embed = discord.Embed(title=f"{ctx.author.name} has created the Lost Faction Battle signups!",
                          description="")
    embed.add_field(name="Click the 🆚 below to enter!",
                    value="")
    factionSignupMessage = await ctx.send(embed=embed)
    await factionSignupMessage.add_reaction("🆚")


@faction_battle_slash.command(name="start", description="Start the Faction Battle")
async def startFactionBattle(ctx):
    await ctx.respond("Starting the Lost Faction Battle!")

    # for testing large groups
    for i in range(29):
        factionBattleContestants.append(factionBattleContestants[0])

    if len(factionBattleContestants) < 4:
        await ctx.respond("Please wait for at least 4 players")
    else:
        await runFactionBattle(ctx, factionBattleContestants)
        factionBattleContestants.clear()


@tournament_slash.command(name="signup", description="LAF Tournament Signup")
async def signups(ctx):
    global signup_message, tournament_running
    if tournament_running:
        await ctx.respond("Please wait for the current tournament to finish.")
        return
    tournament_running = True
    await ctx.respond("Signups begin for the Lost Action Figure Tournament!")
    embed = discord.Embed(title=f"{ctx.author.name} has created the Lost Tournament! (Max 16 players)",
                          description="")
    embed.add_field(name="Click the ✅ below to enter!",
                    value="")
    signup_message = await ctx.send(embed=embed)
    await signup_message.add_reaction("✅")


@tournament_slash.command(name="start", description="LAF Tournament - Max 16 players")
async def start(ctx):
    global signup_message, tournament_contestants, tournament_running
    await ctx.respond("Last call! 3.. 2.. 1..")
    time.sleep(4)
    tournament_contestants.append("Ace")
    tournament_contestants.append("Hurk")
    tournament_contestants.append("Ray")
    tournament_contestants.append("Del EEET1")
    tournament_contestants.append("del eeet2")
    tournament_contestants.append("Del EEET3")
    tournament_contestants.append("del eeet4")
    tournament_contestants.append("Del EEET5")
    tournament_contestants.append("del eeet6")
    tournament_contestants.append("Del EEET7")
    tournament_contestants.append("del eeet8")
    tournament_contestants.append("Del EEET9")
    tournament_contestants.append("del eeet10")
    tournament_contestants.append("Del EEET11")
    tournament_contestants.append("del eeet12")
    tournament_contestants.append("Del EEET13")
    tournament_contestants.append("del eeet14")
    tournament_contestants.append("Del EEET15")
    tournament_contestants.append("del eeet16")

    if len(tournament_contestants) < 2:
        await ctx.respond("Please wait for more players.")
        return

    if tournament_running:
        await run_tournament(ctx, tournament_contestants)
        tournament_running = False
        tournament_contestants.clear()
    else:
        await ctx.respond("There is no tournament running.")


@duel_slash.command(name="any", description="Request a duel")
async def duel(ctx):
    global duel_running, duelists
    if duel_running:
        await ctx.respond("Sorry, please wait for the current duel to finish.")
    else:
        await ctx.respond(f"Beginning the Lost Duel!")
        embed = discord.Embed(title=f"{ctx.author.name} has requested a duel!",
                              description="Click 🤺  to accept the challenge!")
        duel_msg = await ctx.send(embed=embed)
        duelists[duel_msg.id] = (ctx, None)
        await duel_msg.add_reaction("🤺")


@duel_slash.command(name="user", description="Request a duel with a specific user")
async def duel(ctx, user: discord.User):
    global duel_running
    await ctx.respond(f"Beginning the Lost Duel!")
    duel_msg = await ctx.send(f"{ctx.author.name} wants to fight you, {user.mention}!")
    duelists[duel_msg.id] = (ctx, user)
    await duel_msg.add_reaction("🤺")


# class MyView(discord.ui.View):  # Create a class called MyView that subclasses discord.ui.View
#     @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary,
#                        emoji="😎")  # Create a button with the label "😎 Click me!" with color Blurple
#     async def button_callback(self, button, interaction):
#         await interaction.response.send_message(
#             "You clicked the button!")  # Send a message when the button is clicked


# @bot.command(name="bossfight")
# async def bossfight(ctx):
#     await ctx.respond(f"{ctx.author.name} has started a boss fight!")
#     # await run_bossfight(ctx)
#     # msg = await ctx.send("You have ten seconds to decide")
#     msg = await ctx.respond(f"You have until 6 seconds", view=MyView())
#
#     await msg.add_reaction("🤺")
#     now = time.time()
#     future = now + 6
#
#     while time.time() < future:
#         # do stuff
#         pass
#     await msg.clear_reactions()


bot.add_application_command(game_slash)
bot.add_application_command(tournament_slash)
bot.add_application_command(duel_slash)
bot.add_application_command(faction_battle_slash)

bot.run(os.getenv('TOKEN'))  # run the bot with the token


# @bot.command(name="varname")
# async def variable_name(ctx, user: discord.User):
#     await ctx.respond('Hello {}'.format(user.mention))


# @game_slash.command(name="dice", description="Roll dice against the Lost Troll")
# async def dice(ctx):
#     await ctx.respond("Roll!")
#
#
# @bot.slash_command(name="quest", description='Send a warrior on a quest to earn rewards')
# async def quest(ctx):
#     await ctx.respond("Let's quest! Select your warrior!", view=WarriorView())


# class MyModal(discord.ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#
#         self.add_item(discord.ui.InputText(label="Short Input"))
#         self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))
#
#     async def callback(self, interaction: discord.Interaction):
#         embed = discord.Embed(title="Modal Results")
#         embed.add_field(name="Short Input", value=self.children[0].value)
#         embed.add_field(name="Long Input", value=self.children[1].value)
#         await interaction.response.send_message(embeds=[embed])
#
#
# @bot.slash_command(name="modal")
# async def modal_slash(ctx: discord.ApplicationContext):
#     """Shows an example of a modal dialog being invoked from a slash command."""
#     modal = MyModal(title="Modal via Slash Command")
#     await ctx.send_modal(modal)
# @bot.slash_command(name="ping", description="Sends the bot's latency.")  # this decorator makes a slash command
# async def ping(ctx):  # a slash command will be created with the name "ping"
#     await ctx.respond(f"Pong! Latency is {bot.latency}")


# @bot.slash_command(name="hello", description="Say hello to the bot")
# async def hello(ctx):
#     await ctx.respond("Hey!")
