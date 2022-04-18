"""
This file is here for backwards compatibility with previous versions
So that users can use: from mpyg321.mpyg321 import MPyg321Player
Newer version would be: from mpyg321.MPyg321Player import Mpyg321Player
"""
from .MPyg123Player import MPyg123Player
from .MPyg321Player import MPyg321Player
