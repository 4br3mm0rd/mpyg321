"""
MPyG321 callbacks example
Playing and pausing some music, triggering callbacks
You need to add a "sample.mp3" file in the working directory
"""
from mpyg321.mpyg321 import MPyg321Player
from time import sleep


class MyPlayer(MPyg321Player):
    """We create a class extending the basic player to implement callbacks"""

    def onAnyStop(self):
        """Callback when the music stops for any reason"""
        print("The music has stopped")

    def onUserPause(self):
        """Callback when user pauses the music"""
        print("The music has paused")

    def onUserResume(self):
        """Callback when user resumes the music"""
        print("The music has resumed")

    def onUserStop(self):
        """Callback when user stops music"""
        print("The music has stopped (by user)")

    def onMusicEnd(self):
        """Callback when music ends"""
        print("The music has ended")


def do_some_play_pause(player):
    """Does some play and pause"""
    player.play_song("sample.mp3")
    sleep(5)
    player.pause()
    sleep(3)
    player.resume()
    sleep(5)
    player.stop()
    player.quit()


def main():
    """Do the magic"""
    player = MyPlayer()
    do_some_play_pause(player)


if __name__ == "__main__":
    main()
