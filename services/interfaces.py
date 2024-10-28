class AdminGroupsCommandsInterface:
    def set_groups_category(self):
        """
        / category: Category

        Change category, where bot will creates groups
        """
    
    def set_groups_enabled(self):
        """
        / enabled: bool
        """
    
    def set_groups_limit(self):
        """
        / limit: int
        """

    def del_group(self): # Vaiser не надо делать
        """
        / channel: channel = current channel
        """
    
    def guild_config(self):
        """
        Admins can see guild configurations
        """

class MemberGroupsCommandsInterface:
    def ping(self):
        """
        /

        Gets bot's latency
        """

    # Groups commands

    def new_group(self):
        """
        / name: str, description: str, private: bool

        Creates a temporary channel in temporary channels category. If private, only accessed members
        """
    
    def del_group(self):
        """
        / channel: channel

        Only owners of temporary channel can delete temporary channel
        """

    def edit_group(self):
        """
        / channel: channel

        Only owners of temporary channel can update temporary channel
        """
    
    def hide_group(self):
        """
        / channel: channel = current channel

        Hide channel for this member
        """
    
    def show_group(self):
        """
        / channel_id: id

        Show channel for this member
        """
    
    def groups_list(self):
        """
        / show_id: bool

        Gets list of groups (id and name)
        """
    
    def group_info(self):
        """
        / channel: channel = current channel

        Gets info about owners, members and description of group
        """

class AdminVoicesCommandsInterface:
    def set_join_to_create_channel(self):
        """
        / channel: VoiceChannel

        Change join-to-create-channel
        """
    
    def set_voices_enabled(self):
        """
        / enabled: bool

        Special roles may creates temporary channels
        """
    
    def set_voices_limit(self):
        """
        / limit: int
        """

class MemberVoicesCommandsInterface:
    def close_voice(self):
        """
        / channel: channel
        """
    
    def open_voice(self):
        """
        / channel: channel
        """
