import disnake, datetime, aiosqlite, json
from disnake import TextInputStyle
from services.database import Database
from services.config import Config
from services.embeds import *

class NewGroupModal(disnake.ui.Modal):
    def __init__(self, groups_category: disnake.CategoryChannel):
        self.groups_category = groups_category
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
                custom_id="topic",
                style=TextInputStyle.paragraph,
                max_length=200,
                required=False,
            ),
        ]
        super().__init__(
            title="New group",
            custom_id="new_group",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        channel = await self.groups_category.create_text_channel(
            name=inter.text_values["name"],
            topic=inter.text_values["topic"]
        )
        await channel.set_permissions(
            inter.guild.roles[0],
            read_messages=True
        )
        await channel.set_permissions(
            inter.author,
            read_messages=True,
            manage_permissions=True
        )
        # Response
        await inter.response.send_message(embed=Success(description="Created group <#{0}>".format(channel.id)))

class EditGroupModal(disnake.ui.Modal):
    def __init__(self, channel: disnake.TextChannel, old_values: dict):
        self.channel = channel
        self.old_values = old_values
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="example",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=25,
                value=old_values["name"]
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="topic",
                style=TextInputStyle.paragraph,
                max_length=200,
                required=False,
                value=old_values["topic"]
            ),
        ]
        super().__init__(
            title="Edit group",
            custom_id="edit_group",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        await self.channel.edit(
            name=inter.text_values["name"],
            topic=inter.text_values["topic"],
        )
        await self.channel.set_permissions(
            inter.guild.roles[0],
            read_messages=True
        )
        await self.channel.set_permissions(
            inter.author,
            read_messages=True,
            manage_permissions=True
        )
        # Response
        embed = Success(description="Edited group <#{0}>".format(self.channel.id))
        # Add fields
        for key, value in inter.text_values.items():
            embed.add_field(key, value)
        await inter.response.send_message(embed=embed)
