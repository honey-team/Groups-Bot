class AdminCommandsInterface:
    def change_bot_lang(self, **kwargs):
        """
        / lang: "ru" | "en"
        """
    
    def change_temporary_text_channels_category(self, **kwargs):
        """
        / category_id: int

        Change category, where bot will creates temporary channels
        """
    
    def change_temporary_text_channels_prefix(self, **kwargs):
        """
        / prefix: str

        Change temporary channels prefix (prefix="$", channel_name="$hello_world")
        """
    
    def temporary_text_channels_enabled(self, **kwargs):
        """
        / enabled: bool

        Special roles may creates temporary channels
        """
    
    def change_temporary_channels_limit(self, **kwargs):
        """
        / limit: int
        """
    
    def change_user_temporary_channels_limit(self, **kwargs):
        """
        / limit: int
        """
    
    def change_temporary_channels_delay(self, **kwargs):
        """
        / delay: int

        Users can't create more than 1 channel in delay time
        """

    def delete_temporary_channel(self, **kwargs):
        """
        / channel: channel = current channel

        Admins can delete any temporary channel
        """

class MemberCommandsInterface:
    def ping(self, **kwargs):
        """
        /

        Gets bot's latency
        """

    # Temporary channels commands

    def create_temporary_channel(self, **kwargs):
        """
        / name: str, description: str, private: bool

        Creates a temporary channel in temporary channels category. If private, only accessed members
        """
    
    def delete_temporary_channel(self, **kwargs):
        """
        / channel: channel

        Only owners of temporary channel can delete temporary channel
        """
    
    def update_temporary_channel(self, **kwargs):
        """
        / channel: channel

        Only owners of temporary channel can update temporary channel
        """
    
    def hide_temporary_channel(self, **kwargs):
        """
        / channel: channel = current channel

        Hide channel for this member
        """
    
    def show_temporary_channel(self, **kwargs):
        """
        / channel_id: id

        Show channel for this member
        """
    
    def list(self, **kwargs):
        """
        /

        Gets list of non-private temporary channels (id and name)
        """
    
    def info(self, **kwargs):
        """
        / channel: channel = current channel

        Gets info about owners, members and description of temporary channel
        """

    # Commands for manage members

    def invite_member(self, **kwargs):
        """
        / channel: channel = current channel, member: member

        Only owners of temporary channel can invite members to their temporary channel
        (if the channel is private). Bot sends invitation to invited member
        """
    
    def remove_member(self, **kwargs):
        """
        / channel: channel = current channel, member: member

        Only owners of temporary channel can remove members from their temporary channel (if the channel is private)
        """

    def invite_owner(self, **kwargs):
        """
        / channel: channel = current channel, member: member

        Only owners of temporary channel can invite other owners
        """

    def leave(self, **kwargs):
        """
        / channel: channel = current channel

        Leaves temporary channel (if private). If owner leaves channel, and no other owners left, the channel will be deleted
        """