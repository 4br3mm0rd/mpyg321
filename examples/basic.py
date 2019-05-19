"""
MPyG321 basic example
Playing and pausing some music
You need to add a "sample.mp3" file in the working directory
"""
from mpyg321.mpyg321 import MPyg321Player
from time import sleep


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
    player = MPyg321Player()
    do_some_play_pause(player)

if __name__ == "__main__":
    main()
