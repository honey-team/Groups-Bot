from datetime import datetime
from typing import Any, Literal
import disnake
from disnake.utils import MISSING

class Footer(disnake.Embed):
    def __init__(self, *, title: Any | None = None, type: None | Literal['rich'] | Literal['image'] | Literal['video'] | Literal['gifv'] | Literal['article'] | Literal['link'] = "rich", description: Any | None = None, url: Any | None = None, timestamp: datetime | None = None, colour: int | disnake.Colour | None = ..., color: int | disnake.Colour | None = ...) -> None:
        super().__init__(title=title, type=type, description=description, url=url, timestamp=timestamp, colour=colour, color=color)
        self.set_footer(
            text="Groups bot",
            icon_url="https://cdn.discordapp.com/attachments/1013814526010982462/1288785943238545418/image.png?ex=66f672f1&is=66f52171&hm=e0db78d214b9aef352a7f80ba42427b79c024abd1c1e1db2bf4bfd8c41aeaed0&"
        )

class Success(Footer):
    def __init__(self, *, title: Any | None = None, type: None | Literal['rich'] | Literal['image'] | Literal['video'] | Literal['gifv'] | Literal['article'] | Literal['link'] = "rich", description: Any | None = None, url: Any | None = None, timestamp: datetime | None = None, colour: int | disnake.Colour | None = ..., color: int | disnake.Colour | None = ...) -> None:
        super().__init__(
            title="Success",
            type=type,
            description=description,
            url=url,
            timestamp=datetime.now(),
            colour=disnake.Colour.green(),
            color=disnake.Colour.green()
        )

class Info(Footer):
    def __init__(self, *, title: Any | None = None, type: None | Literal['rich'] | Literal['image'] | Literal['video'] | Literal['gifv'] | Literal['article'] | Literal['link'] = "rich", description: Any | None = None, url: Any | None = None, timestamp: datetime | None = None, colour: int | disnake.Colour | None = ..., color: int | disnake.Colour | None = ...) -> None:
        super().__init__(
            title="Info",
            type=type,
            description=description,
            url=url,
            timestamp=datetime.now(),
            colour=disnake.Colour.orange(),
            color=disnake.Colour.orange()
        )

class Error(Footer):
    def __init__(self, *, title: Any | None = None, type: None | Literal['rich'] | Literal['image'] | Literal['video'] | Literal['gifv'] | Literal['article'] | Literal['link'] = "rich", description: Any | None = None, url: Any | None = None, timestamp: datetime | None = None, colour: int | disnake.Colour | None = ..., color: int | disnake.Colour | None = ...) -> None:
        super().__init__(
            title="Error",
            type=type,
            description=description,
            url=url,
            timestamp=datetime.now(),
            colour=disnake.Colour.red(),
            color=disnake.Colour.red()
        )
