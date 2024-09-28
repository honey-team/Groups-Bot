import disnake, datetime
from rich.console import Console
from disnake import TextInputStyle

console = Console()

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
            ),
        ]
        super().__init__(
            title="Create Temporary Channel",
            custom_id="create_temporary_channel",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        name: str = inter.text_values["name"]
        description: str = inter.text_values["description"] if inter.text_values["description"] else ''
        private = inter.text_values["private"]
        category_id: int | None = 1289124625711763466
        category = inter.guild.get_channel(category_id)
        everyone: disnake.Role = inter.guild.roles[0]

        if str(private) == '0':
            private = False
        else:
            private = True

        if category_id in [category.id for category in inter.guild.categories]:
            # Create channel
            await inter.guild.create_text_channel(
                name=name,
                topic=description,
                category=category,
                overwrites={
                    everyone : disnake.PermissionOverwrite(
                        read_messages=not private
                    ),
                    inter.author : disnake.PermissionOverwrite(
                        read_messages=True,
                        manage_permissions=True,
                        manage_channels=True,
                    ),
                }
            )
            # Send response
            embed = disnake.Embed(
                title="Success",
                description="Created text{0} channel: **{1}**".format(" private" if private else " "), # I used to .format becase when localization will be ready it will be useful
                color=disnake.Colour.orange(),
                timestamp=datetime.datetime.now(),
            )
            embed.set_footer(
                text="Groups bot",
                icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
            )
            await inter.response.send_message(
                embed=embed,
                ephemeral=private
            )

class UpdateTemporaryChannelInfoModal(disnake.ui.Modal):
    def __init__(self, old_values: dict, channel_id: int):
        self.channel_id = channel_id
        self.old_values = old_values
        
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="example",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=25,
                value=old_values["name"],
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="description",
                style=TextInputStyle.paragraph,
                max_length=200,
                value=old_values["description"],
                required=False,
            ),
            disnake.ui.TextInput(
                label="Private",
                placeholder="0 == false, 1 == true",
                custom_id="private",
                style=TextInputStyle.short,
                max_length=1,
                value=old_values["private"],
            ),
        ]
        super().__init__(
            title="Update Temporary Channel",
            custom_id="update_temporary_channel",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        prefix: str | None = ''
        name: str = inter.text_values["name"]
        description: str = inter.text_values["description"]
        private = inter.text_values["private"]
        everyone: disnake.Role = inter.guild.roles[0]

        if prefix:
            if prefix[0] == "^":
                name = prefix + name
            elif prefix[-1] == "$":
                name = name + prefix

        print(name, description, private)
        if str(private) == '0':
            private = False
        else:
            private = True

        channel: disnake.TextChannel = inter.guild.get_channel(self.channel_id)
        await channel.edit(name=name, topic=description)
        # Set permissions
        await channel.set_permissions(
            everyone,
            read_messages=not private
        )
        await channel.set_permissions(
            inter.author,
            read_messages=True,
            manage_permissions=True,
            manage_channels=True,
        )
        # Send response
        embed = disnake.Embed(
            title="Success",
            description="Updated text channel: **{0}**".format(name), # I used to .format becase when localization will be ready it will be useful
            color=disnake.Colour.green(),
            timestamp=datetime.datetime.now(),
        )
        if self.old_values["name"] != name:
            embed.add_field(
                name="Name",
                value="*new value:* **{0}**".format(name),
                inline=False,
            )
        if self.old_values["description"] != description:
            embed.add_field(
                name="Description",
                value="*new value:* **{0}**".format(description),
                inline=False,
            )
        if self.old_values["private"] != "1" if private else "0":
            embed.add_field(
                name="Private",
                value="*new value:* **{0}**".format("1" if private else "0"),
                inline=False,
            )
        embed.set_footer(
            text="Groups bot",
            icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
        )
        await inter.response.send_message(
            embed=embed,
            ephemeral=private
        )