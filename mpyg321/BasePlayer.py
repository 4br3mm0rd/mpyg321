"""
Mpyg BasePlayer base class
This class contains all the functions that are common
both to mpg321 and mpg123.
All the players implement this base class and add their
specific feature.
"""
import pexpect
import subprocess
from threading import Thread
from .MpygError import *
from .consts import *


class BasePlayer:
    """Base class for players"""
    player = None
    status = None
    output_processor = None
    song_path = ""
    loop = False
    performance_mode = True
    suitable_versions = []        # mpg123 and/or mpg321 - set inside subclass
    default_player = None         # mpg123 or mpg321 - set inside subclass
    player_version = None         # defined inside check_player
    mpg_outs = []

    def __init__(self, player=None, audiodevice=None, performance_mode=True, custom_args=""):
        """Builds the player and creates the callbacks"""
        self.set_player(player, audiodevice, custom_args)
        self.output_processor = Thread(target=self.process_output)
        self.output_processor.daemon = True
        self.performance_mode = performance_mode
        self.output_processor.start()

    def check_player(self, player):
        """Gets the player"""
        try:
            cmd = str(player)
            output = subprocess.check_output([cmd, "--version"])
            for version in self.suitable_versions:
                if version in str(output):
                    self.player_version = version
            if self.player_version is None:
                raise MPygPlayerNotFoundError(
                    """No suitable player found: you might be using the wrong \
player (Mpyg321Player or Mpyg123Player)""")
        except subprocess.SubprocessError:
            raise MPygPlayerNotFoundError(
                """No suitable player found: you might need to install
                mpg123""")

    def set_player(self, player, audiodevice, custom_args):
        """Sets the player"""
        if player is None:
            player = self.default_player
        self.check_player(player)
        args = " " + custom_args if custom_args != "" else ""
        args += " --audiodevice " + audiodevice if audiodevice else ""
        args += " -R mpyg"
        self.player = pexpect.spawn(str(player) + " " + args)
        self.player.delaybeforesend = None
        self.status = PlayerStatus.INSTANCIATED
        # Setting extended mpg_outs for version specific behaviors
        self.mpg_outs = mpg_outs.copy()
        self.mpg_outs.extend(mpg_outs_ext[self.player_version])

    def process_output(self):
        """Parses the output"""
        mpg_codes = [v["mpg_code"] for v in self.mpg_outs]
        while True:
            index = self.player.expect(mpg_codes)
            action = self.mpg_outs[index]["action"]
            if action == "music_stop":
                self.on_music_stop_int()
            elif action == "user_pause":
                self.on_user_pause_int()
            elif action == "user_start_or_resume":
                self.on_user_start_or_resume_int()
            elif action == "end_of_song":
                self.on_end_of_song_int()
            elif action == "error":
                self.on_error()
            else:
                self.process_output_ext(action)

    def process_output_ext(self, action):
        """Processes the output for version specific behavior"""
        pass

    def play_song(self, path, loop=False):
        """Plays the song"""
        self.loop = loop
        self.set_song(path)
        self.play()

    def play(self):
        """Starts playing the song"""
        self.player.sendline("LOAD " + self.song_path)
        self.status = PlayerStatus.PLAYING

    def pause(self):
        """Pauses the player"""
        if self.status == PlayerStatus.PLAYING:
            self.player.sendline("PAUSE")
            self.status = PlayerStatus.PAUSED

    def resume(self):
        """Resume the player"""
        if self.status == PlayerStatus.PAUSED:
            self.player.sendline("PAUSE")
            self.on_user_resume()

    def stop(self):
        """Stops the player"""
        self.player.sendline("STOP")
        self.status = PlayerStatus.STOPPING

    def quit(self):
        """Quits the player"""
        self.player.sendline("QUIT")
        self.status = PlayerStatus.QUITTED

    def jump(self, pos):
        """Jump to position"""
        self.player.sendline("JUMP " + str(pos))

    def on_error(self):
        """Process errors encountered by the player"""
        output = self.player.readline().decode("utf-8")

        # Check error in list of errors
        for mpg_error in mpg_errors:
            if mpg_error["message"] in output:
                action = mpg_error["action"]
                if action == "generic_error":
                    raise MPygError(output)
                if action == "file_error":
                    raise MPygFileError(output)
                if action == "command_error":
                    raise MPygCommandError(output)
                if action == "argument_error":
                    raise MPygArgumentError(output)
                if action == "eq_error":
                    raise MPygEQError
                if action == "seek_error":
                    raise MPygSeekError

        # Some other error occurred
        raise MPygError(output)

    def set_song(self, path):
        """song_path setter"""
        self.song_path = path

    def set_loop(self, loop):
        """"loop setter"""
        self.loop = loop

    # # # Internal Callbacks # # #
    def on_music_stop_int(self):
        """Internal callback when the music is stopped"""
        if self.status == PlayerStatus.STOPPING:
            self.on_user_stop_int()
            self.status = PlayerStatus.STOPPED
        else:
            self.on_end_of_song_int()

    def on_user_stop_int(self):
        """Internal callback when the user stops the music."""
        self.on_any_stop()
        self.on_user_stop()

    def on_user_pause_int(self):
        """Internal callback when user pauses the music"""
        self.on_any_stop()
        self.on_user_pause()

    def on_user_start_or_resume_int(self):
        """Internal callback when user resumes the music"""
        self.status = PlayerStatus.PLAYING

    def on_end_of_song_int(self):
        """Internal callback when the song ends"""
        if(self.loop):
            self.play()
        else:
            # The music doesn't stop if it is looped
            self.on_any_stop()
        self.on_music_end()

    # # # Public Callbacks # # #
    def on_any_stop(self):
        """Callback when the music stops for any reason"""
        pass

    def on_user_pause(self):
        """Callback when user pauses the music"""
        pass

    def on_user_resume(self):
        """Callback when user resumes the music"""
        pass

    def on_user_stop(self):
        """Callback when user stops music"""
        pass
 
    def on_music_end(self):
        """Callback when music ends"""
        pass
