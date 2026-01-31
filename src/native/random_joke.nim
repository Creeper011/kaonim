import random, sequtils

randomize()

const jokes = [
    ""
]

proc getRandomJoke*(): cstring {.exportc, dynlib.} =
    let index = rand(jokes.len - 1)
    return jokes[index]