from disnake import TextInputStyle
from services import embeds
import disnake

class NewGroupModal(disnake.ui.Modal):
    def __init__(self, groups_category: disnake.CategoryChannel, ephemeral: bool = False):
        self.ephemeral = ephemeral
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
        if not inter.text_values["name"] in [channel.name for channel in self.groups_category.text_channels]:
            channel = await self.groups_category.create_text_channel(
                name=inter.text_values["name"],
                topic=inter.text_values["topic"],
                overwrites=self.groups_category.overwrites
            )
            await channel.set_permissions(
                inter.author,
                read_messages=True,
                manage_permissions=True
            )
            # Response
            await inter.response.send_message(embed=embeds.Success(description="Created group <#{0}>".format(channel.id)), ephemeral=self.ephemeral)
        else:
            await inter.response.send_message(embed=embeds.Error(description="A group by that name already exists"), ephemeral=self.ephemeral)

class EditGroupModal(disnake.ui.Modal):
    def __init__(self, channel: disnake.TextChannel):
        self.channel = channel
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="example",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=25,
                value=self.channel.name
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="topic",
                style=TextInputStyle.paragraph,
                max_length=200,
                required=False,
                value=self.channel.topic
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
            inter.author,
            read_messages=True,
            manage_permissions=True
        )
        # Response
        embed = embeds.Success(description="Edited group <#{0}>".format(self.channel.id))
        # Add fields
        for key, value in inter.text_values.items():
            embed.add_field(key, value)
        await inter.response.send_message(embed=embed)
