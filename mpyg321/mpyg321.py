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
    }
]

mpgcodes = [v["mpg_code"] for v in mpgouts]


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
