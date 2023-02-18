import discord


class WarriorView(discord.ui.View):
    @discord.ui.select(  # the decorator that lets you specify the properties of the select menu
        placeholder="Choose a warrior!",  # the placeholder text that will be displayed if nothing is selected
        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=1,  # the maximum number of values that can be selected by the users
        options=[  # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Ace",
                description="Some believe he is the chosen one who will lead the lost from the darkness."
            ),
            discord.SelectOption(
                label="Hitch",
                description="Ace's loyal compandroid with a knack for engineering gadgets and weapons"
            ),
            discord.SelectOption(
                label="Hurk",
                description="A battle-hardened army general and fearsome warrior known throughout the Wastement"
            ),
            discord.SelectOption(
                label="Flynn",
                description="Battlefield medic and science officer."
            ),
            discord.SelectOption(
                label="Chet",
                description="..."
            ),
            discord.SelectOption(
                label="Ray",
                description="A powerful alien super soldier from a future planet destroyed long ago."
            ),
            discord.SelectOption(
                label="Drek",
                description="Master archer and commander of the basement bug hoards"
            ),
            discord.SelectOption(
                label="Nox",
                description="A deadly bounty hunter fixated on completing his extensive collection of hero heads"
            ),
            discord.SelectOption(
                label="Kage",
                description="Went missing for decades only to return as a fearsome warlord fuelled by madness and "
                            "juice boxes "
            ),
            discord.SelectOption(
                label="Darkkon",
                description="Intergalactic warlord, conquerer of systems, hunter of heroes but feared by all."
            ),
            discord.SelectOption(
                label="Rot",
                description="A fallen hero brought back by dark sorcery"
            ),
            discord.SelectOption(
                label="Skorn",
                description="Possesses mysterious powers that bend the elements and other warriors to his will"
            )
        ]
    )
    async def select_callback(self, select, interaction):  # the function called when the user is done selecting options
        await interaction.response.send_message(f"Sending {select.values[0]} on a quest!")