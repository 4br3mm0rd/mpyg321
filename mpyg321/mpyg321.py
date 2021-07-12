import pexpect
from threading import Thread

from pexpect import exceptions


mpg_outs = [
    {
        "mpg_code": "@P 0",
        "action": "music_stop",
        "description": """For mpg123, it corresponds to any stop
                        For mpg312 it corresponds to user stop only"""
    },
    {
        "mpg_code": "@P 1",
        "action": "user_pause",
        "description": "Music has been paused by the user."
    },
    {
        "mpg_code": "@P 2",
        "action": "user_start_or_resume",
        "description": "Music has been started resumed by the user."
    },
    {
        "mpg_code": "@P 3",
        "action": "end_of_song",
        "description": "Player has reached the end of the song."
    },
    {
        "mpg_code": "@E *",
        "action": "error",
        "description": "Player has encountered an error."
    }
]

mpg_codes = [v["mpg_code"] for v in mpg_outs]

mpg_errors = [
    {
        "message": "empty list name",
        "action": "generic_error"
    },
    {
        "message": "No track loaded!",
        "action": "generic_error"
    },
    {
        "message": "Error opening stream",
        "action": "file_error"
    },
    {
        "message": "failed to parse given eq file:",
        "action": "file_error"
    },
    {
        "message": "Corrupted file:",
        "action": "file_error"
    },
    {
        "message": "Unknown command:",
        "action": "command_error"
    },
    {
        "message": "Unfinished command:",
        "action": "command_error"
    },
    {
        "message": "Unknown command or no arguments:",
        "action": "argument_error"
    },
    {
        "message": "invalid arguments for",
        "action": "argument_error"
    },
    {
        "message": "Missing argument to",
        "action": "argument_error"
    },
    {
        "message": "failed to set eq:",
        "action": "eq_error"
    },
    {
        "message": "Error while seeking",
        "action": "seek_error"
    },
]

suitable_versions = ["mpg123", "mpg321"]


# # # Errors # # #
class MPyg321Error(RuntimeError):
    """Base class for any errors encountered by the player during runtime"""
    pass


class MPyg321FileError(MPyg321Error):
    """Errors encountered by the player related to files"""
    pass


class MPyg321CommandError(MPyg321Error):
    """Errors encountered by the player related to player commands"""
    pass


class MPyg321ArgumentError(MPyg321Error):
    """Errors encountered by the player related to arguments for commands"""
    pass


class MPyg321EQError(MPyg321Error):
    """Errors encountered by the player related to the equalizer"""
    pass


class MPyg321SeekError(MPyg321Error):
    """Errors encountered by the player related to the seek"""
    pass


class MPyg321WrongPlayerPathError(MPyg321Error):
    """Errors encountered when a wrong player path is provided in the
    constructor"""
    pass


class MPyg321NoPlayerFoundError(MPyg321Error):
    """Errors encountered when no suitable player is found"""
    pass


class PlayerStatus:
    INSTANCIATED = 0
    PLAYING = 1
    PAUSED = 2
    RESUMING = 3
    STOPPING = 4
    STOPPED = 5
    QUITTED = 6


class MPyg321Player:
    """Main class for mpg321 player management"""
    player = None
    player_version = "mpg123"
    status = None
    output_processor = None
    song_path = ""
    loop = False

    def __init__(self, player=None, audiodevice=None):
        """Builds the player and creates the callbacks"""
        self.set_player(player, audiodevice)
        self.output_processor = Thread(target=self.process_output)
        self.output_processor.daemon = True
        self.output_processor.start()

    def set_version_and_get_player(self, player):
        """Gets the player """
        version_process = None
        valid_player = None
        if player is not None:
            try:
                version_process = pexpect.spawn(str(player) + " --version")
                valid_player = str(player)
            except pexpect.exceptions.ExceptionPexpect:
                raise MPyg321WrongPlayerPathError(
                    """Invalid file path provided""")

        else:
            try:
                version_process = pexpect.spawn("mpg123 ---version")
                valid_player = "mpg123"
            except pexpect.exceptions.ExceptionPexpect:
                try:
                    version_process = pexpect.spawn("mpg321 --version")
                    valid_player = "mpg321"
                except pexpect.exceptions.ExceptionPexpect:
                    raise MPyg321NoPlayerFoundError(
                        """No suitable player found""")

        index = version_process.expect(suitable_versions)
        try:
            self.player_version = suitable_versions[index]
        except IndexError:
            raise MPyg321NoPlayerFoundError("""No suitable player found""")
        return valid_player

    def set_player(self, player, audiodevice):
        """Sets the player"""
        player = self.set_version_and_get_player(player)
        args = "--remote" if self.player_version == "mpg123" else "-R test"
        args += " --audiodevice " + audiodevice if audiodevice else ""
        self.player = pexpect.spawn(str(player) + " " + args)
        self.status = PlayerStatus.INSTANCIATED

    def process_output(self):
        """Parses the output"""
        while True:
            index = self.player.expect(mpg_codes)
            action = mpg_outs[index]["action"]
            if action == "music_stop":
                self.on_music_stop_int()
            if action == "user_pause":
                self.on_user_pause_int()
            if action == "user_start_or_resume":
                self.on_user_start_or_resume_int()
            if action == "end_of_song":
                self.on_end_of_song_int()
            if action == "error":
                self.on_error()

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
        if self.player_version == "mpg321":
            self.status = PlayerStatus.STOPPED
        else:
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
                    raise MPyg321Error(output)
                if action == "file_error":
                    raise MPyg321FileError(output)
                if action == "command_error":
                    raise MPyg321CommandError(output)
                if action == "argument_error":
                    raise MPyg321ArgumentError(output)
                if action == "eq_error":
                    raise MPyg321EQError
                if action == "seek_error":
                    raise MPyg321SeekError

        # Some other error occurred
        raise MPyg321Error(output)

    def set_song(self, path):
        """song_path setter"""
        self.song_path = path

    def set_loop(self, loop):
        """"loop setter"""
        self.loop = loop

    # # # Internal Callbacks # # #
    def on_music_stop_int(self):
        """Internal callback when user stops the music"""
        if self.player_version == "mpg123":
            if self.status == PlayerStatus.STOPPING:
                self.status = PlayerStatus.STOPPED
                self.on_user_stop_int()
            else:
                # If not stopped by the user, it is the end of the song
                # the on_any_stop function is called inside on_end_of_song_int
                self.on_end_of_song_int()
        else:
            self.on_user_stop_int()

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
