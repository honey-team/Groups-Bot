import disnake
from disnake import TextInputStyle

class GetTemporaryChannelInfoModal(disnake.ui.Modal):
    def __init__(self):
        # Детали модального окна и его компонентов
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="example",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Lorem ipsum dolor sit amet.",
                custom_id="description",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.StringSelect(
                placeholder="Choose variant",
                min_values=1,
                max_values=1,
                options=[
                    disnake.SelectOption(
                        label="Private",
                        emoji=":lock:",
                        description="You and accessed peoples can see this channel"
                    ),
                    disnake.SelectOption(
                        label="Public",
                        emoji=":unlock:",
                        description="Everyone can see this channel"
                    ),
                ]
            )
        ]
        super().__init__(
            title="Create Tag",
            custom_id="create_tag",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        return inter.text_values