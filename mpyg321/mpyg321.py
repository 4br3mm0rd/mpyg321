import pexpect
from threading import Thread


mpg_outs = [
    {
        "mpg_code": "@P 0",
        "action": "user_stop",
        "description": "Music has been stopped by the user."
    },
    {
        "mpg_code": "@P 1",
        "action": "user_pause",
        "description": "Music has been paused by the user."
    },
    {
        "mpg_code": "@P 2",
        "action": "user_resume",
        "description": "Music has been resumed by the user."
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


# # # Errors # # #
class MPyg321PlayerError(RuntimeError):
    """Base class for any errors encountered by the player during runtime"""
    pass


class MPyg321PlayerFileError(MPyg321PlayerError):
    """Errors encountered by the player related to files"""
    pass


class MPyg321PlayerCommandError(MPyg321PlayerError):
    """Errors encountered by the player related to player commands"""
    pass


class MPyg321PlayerArgumentError(MPyg321PlayerError):
    """Errors encountered by the player related to arguments for commands"""
    pass


class MPyg321PlayerEQError(MPyg321PlayerError):
    """Errors encountered by the player related to the equalizer"""
    pass


class MPyg321PlayerSeekError(MPyg321PlayerError):
    """Errors encountered by the player related to the seek"""
    pass


class PlayerStatus:
    INSTANCIATED = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3
    QUITTED = 4


class MPyg321Player:
    """Main class for mpg321 player management"""
    player = None
    status = None
    output_processor = None
    song_path = ""
    loop = False

    def __init__(self):
        """Builds the player and creates the callbacks"""
        try:
            self.player = pexpect.spawn("mpg321 -R somerandomword",
                                        timeout=None)
        except pexpect.exceptions.ExceptionPexpect:
            try:
                self.player = pexpect.spawn("mpg123 -R somerandomword",
                                            timeout=None)
            except pexpect.exceptions.ExceptionPexpect:
                raise FileNotFoundError("""\
No suitable command found. Please install mpg321 or mpg123 and try again.""")

        self.status = PlayerStatus.INSTANCIATED
        self.output_processor = Thread(target=self.process_output)
        self.output_processor.daemon = True
        self.output_processor.start()

    def process_output(self):
        """Parses the output"""
        while True:
            index = self.player.expect(mpg_codes)
            action = mpg_outs[index]["action"]
            if action == "user_stop":
                self.on_user_stop_int()
            if action == "user_pause":
                self.on_user_pause_int()
            if action == "user_resume":
                self.on_user_resume_int()
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
            self.status = PlayerStatus.PLAYING

    def stop(self):
        """Stops the player"""
        self.player.sendline("STOP")
        self.status = PlayerStatus.STOPPED

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
                    raise MPyg321PlayerError(output)
                if action == "file_error":
                    raise MPyg321PlayerFileError(output)
                if action == "command_error":
                    raise MPyg321PlayerCommandError(output)
                if action == "argument_error":
                    raise MPyg321PlayerArgumentError(output)
                if action == "eq_error":
                    raise MPyg321PlayerEQError
                if action == "seek_error":
                    raise MPyg321PlayerSeekError

        # Some other error occurred
        raise MPyg321PlayerError(output)

    def set_song(self, path):
        """song_path setter"""
        self.song_path = path

    def set_loop(self, loop):
        """"loop setter"""
        self.loop = loop

    # # # Internal Callbacks # # #
    def on_user_stop_int(self):
        """Internal callback when user stops the music"""
        self.on_any_stop()
        self.on_user_stop()

    def on_user_pause_int(self):
        """Internal callback when user pauses the music"""
        self.on_any_stop()
        self.on_user_pause()

    def on_user_resume_int(self):
        """Internal callback when user resumes the music"""
        self.on_user_resume()

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
