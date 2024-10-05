import disnake, datetime, aiosqlite, json
from disnake import TextInputStyle
from services.database import Database
from services.config import Config
from services.embeds import *

class GetTemporaryChannelInfoModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="example",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=25,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="description",
                style=TextInputStyle.paragraph,
                max_length=200,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Private",
                placeholder="0 == false, 1 == true",
                custom_id="private",
                style=TextInputStyle.short,
                max_length=1,
                value=0,
            ),
        ]
        super().__init__(
            title="Create Temporary Channel",
            custom_id="create_temporary_channel",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        DB_PATH = Config["paths"]["database"]

        async with aiosqlite.connect(DB_PATH) as db:
            guild_configs = await Database.Guilds.get_config(db, inter.guild_id)
            # Set channel values
            name: str = inter.text_values["name"]
            description: str = inter.text_values["description"] if inter.text_values["description"] else ''
            private = int(inter.text_values["private"])
            category_id: int = guild_configs["category_id"]
            # Set useful variables
            category: disnake.CategoryChannel | None = None # In this category bot will creates group
            everyone: disnake.Role = inter.guild.roles[0]

            if category := inter.guild.get_channel(category_id):
                channel = await inter.guild.create_text_channel(
                    name=name,
                    topic=description,
                    category=category
                )
                await channel.set_permissions(
                    everyone,
                    view_channel=not private,
                    send_messages=not private
                )
                await channel.set_permissions(
                    inter.author,
                    manage_channels=True,
                    manage_permissions=True
                )

                await db.execute("INSERT OR REPLACE INTO temp_channels VALUES (?, ?, ?, ?, ?)",
                    (
                        channel.id, # channel_id
                        inter.guild_id, # guild_id
                        json.dumps([inter.author.id]), # members
                        json.dumps([inter.author.id]), # owners
                        int(private) # private
                    )
                )
                user_config = await Database.Users.get_config(db, inter.author.id)
                await db.execute("INSERT INTO users (temp_channels_count, last_temp_channel_created) VALUES (?, ?)",
                    (
                        user_config["temp_channels_count"] + 1,
                        datetime.now()
                    )
                )
                await db.commit()

                await inter.response.send_message(embed=Success(description="Created group <#{0}>".format(channel.id)))
            else:
                await inter.response.send_message(embed=Error(description="Unknown category <#{0}>".format(category_id)))

class EditTemporaryChannelInfoModal(disnake.ui.Modal):
    def __init__(self, channel: disnake.TextChannel):
        self.channel = channel
        
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="example",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=25,
                value=self.channel.name,

            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="description",
                style=TextInputStyle.paragraph,
                max_length=200,
                value=self.channel.topic,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Private",
                placeholder="0 == false, 1 == true",
                custom_id="private",
                style=TextInputStyle.short,
                max_length=1,
            ),
        ]
        super().__init__(
            title="Edit group",
            custom_id="update_temporary_channel",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        DB_PATH = Config["paths"]["database"]
        # Get configs
        async with aiosqlite.connect(DB_PATH) as db:
            self.group_config = await Database.TempChannels.get_config(db, self.channel.id)
            self.guild_config = await Database.Guilds.get_config(db, inter.guild_id)
        
        name = inter.text_values["name"]
        description = inter.text_values["description"]
        private = bool(int(inter.text_values["private"]))

        everyone: disnake.Role = inter.guild.roles[0]

        # Edit channel
        await self.channel.edit(
            name=name,
            topic=description
        )
        # Set permissions
        await self.channel.set_permissions(
            everyone,
            read_messages=not private
        )
        await self.channel.set_permissions(
            inter.author,
            read_messages=True,
            manage_permissions=True,
            manage_channels=True,
        )
        # Send response
        await inter.response.send_message(
            embed=Success(description="Edited group: **{0}**".format(name)), # I used to .format becase when localization will be ready it will be useful),
            ephemeral=private
        )