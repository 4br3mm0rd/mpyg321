# mpyg321

mpyg321 is a simple python wrapper for mpg321 and mpg123. It allows you to easily play mp3 sounds in python, do basic operations on the music and implement callbacks for events like the end of a sound.

# Installation

mpyg321 requires the installation of mpg321 (or mpg123 depending on your usage) software for reading mp3. This section describes the installation of the library on MacOS, Linux and Windows. **For now, the library has only been tested on mac, but it should work on any platform.**

## MacOS

```
$ brew install mpg321
$ pip3 install mpyg321
```

## Linux

```
$ sudo apt-get install mpg321
$ pip3 install mpyg321
```

## Windows

For windows installation, download mpg321 on the website: [mpg321's website](https://www.mpg123.de/download.shtml). Make sure to rename the command to mpg321, and then run:

```
$ pip install mpyg321
```

# Usage

Usage is pretty straight forward, and all the functionnalities are easily shown in the examples folder.
```
from mpyg321.mpyg321 import MPyg321Player
player = MPyg321Player()
player.play_song("/path/to/some_mp3.mp3")
```

## Loops
In order to loop (replay the song when it ended), you can either set the loop mode when calling the `play_song` function:
```
player.play_song("/path/to/sample.mp3", loop=True)
```
or programmatically set the loop mode anywhere in the code:
```
player.play_song("/path/to/sample.mp3)
// Do some stuff ...
player.set_loop(True)
``` 
**Note:** when calling `player.set_loop(True)`, the loop mode will only be taken into account at the end of a song. If nothing is playing, this call will not replay the previous song. In order to replay the previous song, you should call: `player.play()`
