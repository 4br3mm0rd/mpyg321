"""
MPyg321 callbacks example
Playing and pausing some music, triggering callbacks
You need to add a "sample.mp3" file in the working directory

In this example, you can replace MPyg321Player by MPyg123Player
according to the player you installed on your machine (mpg321/mpg123)
"""

from time import sleep

from mpyg321.MPyg321Player import MPyg321Player

player = MPyg321Player()


@player.on("any_stop")
def on_any_stop():
    """Callback when the music stops for any reason"""
    print("The music has stopped")


@player.on("user_pause")
def on_user_pause():
    """Callback when user pauses the music"""
    print("The music has paused")


def on_user_resume():
    """Callback when user resumes the music"""
    print("The music has resumed")


@player.on("user_stop")
def on_user_stop():
    """Callback when user stops music"""
    print("The music has stopped (by user)")


@player.on("music_end")
def on_music_end():
    """Callback when music ends"""
    print("The music has ended")


def do_some_play_pause(player):
    """Does some play and pause"""
    player.play_song("sample.mp3")
    sleep(5)
    player.pause()
    player.subscribe_event("user_resume", on_user_resume)
    sleep(3)
    player.resume()
    sleep(5)
    player.stop()
    sleep(2)
    player.play()
    sleep(20)
    player.quit()


def main():
    """Do the magic"""
    do_some_play_pause(player)


if __name__ == "__main__":
    main()
