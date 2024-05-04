"""
MPyg321 callbacks example
Playing and pausing some music, triggering callbacks
You need to add a "sample.mp3" file in the working directory

In this example, you can replace MPyg321Player by MPyg123Player
according to the player you installed on your machine (mpg321/mpg123)
"""

from time import sleep

from mpyg321.consts import MPyg321Events
from mpyg321.MPyg123Player import MPyg123Player

player = MPyg123Player()


@player.on(MPyg321Events.ANY_STOP)
def on_any_stop(context):
    """Callback when the music stops for any reason"""
    print("The music has stopped")
    print(context)


@player.on(MPyg321Events.USER_PAUSE)
def on_user_pause(context):
    """Callback when user pauses the music"""
    print("The music has paused")
    print(context)


def on_user_resume(context):
    """Callback when user resumes the music"""
    print("The music has resumed")
    print(context)


@player.on(MPyg321Events.USER_STOP)
def on_user_stop(context):
    """Callback when user stops music"""
    print("The music has stopped (by user)")
    print(context)


@player.on(MPyg321Events.MUSIC_END)
def on_music_end(context):
    """Callback when music ends"""
    print("The music has ended")
    print(context)


def do_some_play_pause(player):
    """Does some play and pause"""
    player.play_song("sample.mp3")
    sleep(5)
    player.pause()
    player.subscribe_event(MPyg321Events.USER_RESUME, on_user_resume)
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
