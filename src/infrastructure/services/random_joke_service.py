""""Service to fetch random jokes"""

import ctypes

# pylint: disable=too-few-public-methods
class RandomJokeService():
    """Service to fetch random jokes."""

    def __init__(self) -> None:
        self.nim_lib = ctypes.CDLL('./lib/librandom_joke.so')
        self.nim_lib.getRandomJoke.restype = ctypes.c_char_p

    def get_random_joke(self) -> str:
        """Fetches a random joke from the native Nim library."""
        joke = self.nim_lib.getRandomJoke()
        return joke.decode('utf-8')
