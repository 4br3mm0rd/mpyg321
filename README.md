[![Downloads](https://pepy.tech/badge/mpyg321)](https://pepy.tech/project/mpyg321)
[![Downloads](https://pepy.tech/badge/mpyg321/month)](https://pepy.tech/project/mpyg321)
[![Downloads](https://pepy.tech/badge/mpyg321/week)](https://pepy.tech/project/mpyg321)

# mpyg321

mpyg321 is a simple python wrapper for mpg321 and mpg123. It allows you to easily play mp3 sounds in python, do basic operations on the music and implement callbacks for events like the end of a sound.

# Installation

mpyg321 requires the installation of mpg123 (or mpg321 depending on your usage) software for reading mp3. This section describes the installation of the library on MacOS, Linux and Windows.

We recommend using mpg123 since the project is more up to date. However, you can also use this library with mpg321 (using the `MPyg321Player` class)

## MacOS

```
$ brew install mpg123 # or mpg321
$ pip3 install mpyg321
```

## Linux

```
$ sudo apt-get update
$ sudo apt-get install mpg123 # or mpg321
$ pip3 install mpyg321
```

## Windows

For windows installation, download mpg123 on the website: [mpg123's website](https://www.mpg123.de/download.shtml), and then run:

```
$ pip install mpyg321
```

# Usage

Usage is pretty straight forward, and all the functionnalities are easily shown in the examples folder.

```
from mpyg321.MPyg123Player import MPyg123Player # or MPyg321Player if you installed mpg321
player = MPyg123Player()
player.play_song("/path/to/some_mp3.mp3")
```

## Calbacks and Events

### Callbacks

You can implement callbacks for several events such as: end of song, user paused the music, ...
All the callbacks can be found inside the code of the `BasePlayer` class and the `MPyg123Player` class.
Most of the callbacks are implemented in the `callbacks.py` example file.

### Events

Starting **from version 2.2.0**, you can now subscribe to events using decorators and/or the `subscribe_event` function.
Here is an example usage. You can find more details in the `events.py` example file.

```
player = MPyg123Player()

@player.on(MPyg321Events.ANY_STOP)
def callback(context):
    print("Any stop event occured")

# or
def my_func(context):
    print("Other event subscribed")

player.subscribe_event(MPyg321Events.ANY_STOP, my_func)
```

Here is an exhaustive list of the available events and their compatibilities with the different players (MPyg123 and MPyg321):
|Event|Description|MPyg123Player|MPyg321Player|
|------|------|:---------:|:-------:|
|USER_STOP|When you stop the music (call `player.stop`)|X|X|
|USER_PAUSE|When you pause the music (call `player.pause`)|X|X|
|USER_RESUME|When you resume the music (call `player.resume`)|X|X|
|ANY_STOP|When any stop occures (pause, stop, end of music)|X|X|
|MUSIC_END|When the music ends|X|X|
|ERROR|When an error occurs (The error info is within the context using the class `MPyg321ErrorContext`)|X|X|
|USER_MUTE|When you mute the player|X|-|
|USER_MUTE|When you unmute the player|X|-|

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
