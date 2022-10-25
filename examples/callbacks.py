"""
MPyg321 callbacks example
Playing and pausing some music, triggering callbacks
You need to add a "sample.mp3" file in the working directory

In this example, you can replace MPyg321Player by MPyg123Player
according to the player you installed on your machine (mpg321/mpg123)
"""
from mpyg321.MPyg123Player import MPyg123Player

from time import sleep


class MyPlayer(MPyg123Player):
    """We create a class extending the basic player to implement callbacks"""

    def on_any_stop(self):
        """Callback when the music stops for any reason"""
        print("The music has stopped")

    def on_user_pause(self):
        """Callback when user pauses the music"""
        print("The music has paused")

    def on_user_resume(self):
        """Callback when user resumes the music"""
        print("The music has resumed")

    def on_user_stop(self):
        """Callback when user stops music"""
        print("The music has stopped (by user)")

    def on_music_end(self):
        """Callback when music ends"""
        print("The music has ended")

    def on_user_mute(self):
        """Callback when music is muted"""
        print("The music has been muted (continues playing)")

    def on_user_unmute(self):
        """Callback when music is unmuted"""
        print("Music has been unmuted")


def do_some_play_pause(player):
    """Does some play and pause"""
    player.play_song("sample.mp3")
    sleep(5)
    player.pause()
    sleep(3)
    player.resume()
    sleep(5)
    player.stop()
    sleep(2)
    player.play()
    sleep(2)
    player.mute()
    sleep(1)
    player.unmute()
    sleep(20)
    player.quit()


def main():
    """Do the magic"""
    player = MyPlayer(rva_mix=True)
    do_some_play_pause(player)


if __name__ == "__main__":
    main()
