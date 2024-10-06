import typing # typing is literally the theme of this file

class GuildData(typing.TypedDict):
    guild_id: int
    category_id: int
    text_channels_limit: int
    text_channels_delay: int
    text_channels_prefix: str
    text_channels_user_limit: int
    text_channels_enabled: int
    ticket_category_id: int | None
    ticket_role_id: int | None