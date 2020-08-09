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


def do_some_jumps(player):
    """Does some jumps"""
    player.play_song("sample.mp3")
    sleep(3)
    print("Jumping to MPEG frame 200...")
    player.jump(200)
    sleep(3)
    print("Jumping to 1 second...")
    player.jump("1s")
    sleep(3)
    print("Jumping forward 20 MPEG frames...")
    player.jump("+20")
    sleep(3)
    print("Jumping back 1 second...")
    player.jump("-1s")
    sleep(3)
    player.stop()


def main():
    """Do the magic"""
    player = MPyg321Player()
    do_some_play_pause(player)
    do_some_jumps(player)
    player.quit()


if __name__ == "__main__":
    main()
