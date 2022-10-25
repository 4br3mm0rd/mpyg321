from .BasePlayer import BasePlayer


class MPyg321Player(BasePlayer):
    """Player for legacy mpg321"""
    def __init__(self, player=None, audiodevice=None, performance_mode=True, custom_args=""):
        self.suitable_versions = ["mpg321"]
        self.default_player = "mpg321"
        super().__init__(player, audiodevice, performance_mode, custom_args)


    def process_output_ext(self, action):
        """
        Processes specific output for mpg321 player
        It should contain the code for the mpg_out "end_of_song"
        We did not put it because the BaseClass implements a behavior
        which works for both versions
        """
        pass

    def volume(self, percent):
        """Adjust player's volume"""
        self.player.sendline("GAIN {}".format(percent))
