from .BasePlayer import BasePlayer
from .consts import PlayerStatus


class MPyg123Player(BasePlayer):
    """Player for legacy mpg321"""
    def __init__(self, player=None, audiodevice=None, performance_mode=True, custom_args="", rva_mix=False):
        self.suitable_versions = ["mpg123"]
        self.default_player = "mpg123"
        custom_args += " --rva-mix " if rva_mix else ""
        super().__init__(player, audiodevice, performance_mode, custom_args)
        if performance_mode:
            self.silence_mpyg_output()

    def process_output_ext(self, action):
        """Processes specific output for mpg123 player"""
        if action == "user_mute":
            self.on_user_mute()
        elif action == "user_unmute":
            self.on_user_unmute()

    def load_list(self, entry, filepath):
        """Load an entry in a list
        Parameters:
        entry (int): index of the song in the list - first is 0
        filepath: URL/Path to the list
        """
        self.player.sendline("LOADLIST {} {}".format(entry, filepath))
        self.status = PlayerStatus.PLAYING

    def silence_mpyg_output(self):
        """Improves performance by silencing the mpg123 process frame output"""
        self.player.sendline("SILENCE")

    def mute(self):
        """Mutes the player"""
        self.player.sendline("MUTE")

    def unmute(self):
        """Unmutes the player"""
        self.player.sendline("UNMUTE")

    def volume(self, percent):
        """Adjust player's volume"""
        self.player.sendline("VOLUME {}".format(percent))

    # # # Public Callbacks # # #
    def on_user_mute(self):
        """Callback when user mutes player"""
        pass

    def on_user_unmute(self):
        """Callback when user unmutes player"""
        pass
