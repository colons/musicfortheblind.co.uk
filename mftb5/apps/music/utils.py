from os import path
from random import random
import subprocess
from tempfile import gettempdir


def read_x_into_y(x, y):
    while True:
        data = x.read(1024 * 100)
        if not data:
            break
        y.write(data)


def scratchpad():
    return path.join(gettempdir(), str(random()))


def decode_flac(flacfile):
    filename = scratchpad()
    decode = subprocess.Popen(['flac', '-d', '-', '-o', filename],
                              stdin=subprocess.PIPE)
    read_x_into_y(flacfile, decode.stdin)
    return filename


def encode_vorbis(wavfile):
    filename = scratchpad()
    encode = subprocess.Popen(['oggenc', '-q', '8', '-o', filename, '-'],
                              stdin=subprocess.PIPE)
    read_x_into_y(wavfile, encode.stdin)
    return filename
