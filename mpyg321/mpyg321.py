import pexpect
from threading import Thread


def is_installed(name):
    """Checks if a program is installed"""
    import os
    import subprocess


    devnull = open(os.devnull)
    try:
        subprocess.Popen([name, "--help"], stdout=devnull, stderr=devnull).communicate()
    except FileNotFoundError:
        print(name + " not installed.")
        return False
    return True


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
        if is_installed("mpg321"):
            player_command = "mpg321"
        elif is_installed("mpg123"):
            player_command = "mpg123"
        else:
            raise FileNotFoundError("No suitable program found. PLease install mpg321 or mpg123 and try again.")

        self.player = pexpect.spawn(player_command + " -R somerandomword", timeout=None)
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
