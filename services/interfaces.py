class AdminCommandsInterface:
    def set_groups_category(self, **kwargs):
        """
        / category: Category

        Change category, where bot will creates temporary channels
        """
    
    def set_groups_enabled(self, **kwargs):
        """
        / enabled: bool

        Special roles may creates temporary channels
        """
    
    def set_groups_limit(self, **kwargs):
        """
        / limit: int
        """

    def del_group(self, **kwargs): # Vaiser не надо делать
        """
        / channel: channel = current channel

        Admins can delete any temporary channel
        """
    
    def guild_config(self, **kwargs):
        """
        Admins can see guild configurations
        """

class MemberCommandsInterface:
    def ping(self, **kwargs):
        """
        /

        Gets bot's latency
        """

    # Groups commands

    def new_group(self, **kwargs):
        """
        / name: str, description: str, private: bool

        Creates a temporary channel in temporary channels category. If private, only accessed members
        """
    
    def del_group(self, **kwargs):
        """
        / channel: channel

        Only owners of temporary channel can delete temporary channel
        """

    def edit_group(self, **kwargs):
        """
        / channel: channel

        Only owners of temporary channel can update temporary channel
        """
    
    def hide_group(self, **kwargs):
        """
        / channel: channel = current channel

        Hide channel for this member
        """
    
    def show_group(self, **kwargs):
        """
        / channel_id: id

        Show channel for this member
        """
    
    def groups_list(self, **kwargs):
        """
        /

        Gets list of non-private temporary channels (id and name)
        """
    
    def group_info(self, **kwargs):
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

__all__ = (
    "AdminCommandsInterface",
    "MemberCommandsInterface"
)