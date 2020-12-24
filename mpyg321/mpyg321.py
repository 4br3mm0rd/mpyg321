import pexpect
from threading import Thread


mpgouts = [
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

mpgcodes = [v["mpg_code"] for v in mpgouts]

mpg_errors = [
    {
        "message": "empty list name",
        "action": "generic_error"
    },
    {
        "message": "No track loaded!",
        "action": "generic_error"
    }
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

    def __init__(self):
        """Builds the player and creates the callbacks"""
        try:
            self.player = pexpect.spawn("mpg321 -R somerandomword",
                                        timeout=None)
        except pexpect.actions.ExceptionPexpect:
            try:
                self.player = pexpect.spawn("mpg123 -R somerandomword",
                                            timeout=None)
            except pexpect.actions.ExceptionPexpect:
                raise FileNotFoundError("""\
No suitable command found. Please install mpg321 or mpg123 and try again.""")

        self.status = PlayerStatus.INSTANCIATED
        self.output_processor = Thread(target=self.process_output)
        self.output_processor.daemon = True
        self.output_processor.start()

    def process_output(self):
        """Parses the output"""
        while True:
            index = self.player.expect(mpgcodes)
            action = mpgouts[index]["action"]
            if action == "user_stop":
                self.onAnyStop()
                self.onUserStop()
            if action == "user_pause":
                self.onAnyStop()
                self.onUserPause()
            if action == "user_resume":
                self.onUserResume()
            if action == "end_of_song":
                self.onAnyStop()
                self.onMusicEnd()
            if action == "error":
                self.handle_errors()

    def play_song(self, path):
        """Plays the song"""
        self.player.sendline("LOAD " + path)
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

    def handle_errors(self):
        """Handle errors encountered by the player"""
        output = self.player.readline().decode("utf-8")

        # Check error in list of errors
        for mpg_error in mpg_errors:
            if error["message"] in output:
                action = error["action"]
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

    # # # Callbacks # # #
    def onAnyStop(self):
        """Callback when the music stops for any reason"""
        pass

    def onUserPause(self):
        """Callback when user pauses the music"""
        pass

    def onUserResume(self):
        """Callback when user resumes the music"""
        pass

    def onUserStop(self):
        """Callback when user stops music"""
        pass

    def onMusicEnd(self):
        """Callback when music ends"""
        pass
