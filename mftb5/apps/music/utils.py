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


def pipe_file_through_command(the_file, command):
    decode = subprocess.Popen(command, stdin=subprocess.PIPE)
    read_x_into_y(the_file, decode.stdin)


def scratchpad():
    return path.join(gettempdir(), str(random()))


def decode_flac(flacfile):
    filename = scratchpad()
    pipe_file_through_command(flacfile, ['flac', '-d', '-', '-o', filename])
    return filename


def decode_mp3(mp3file):
    filename = scratchpad()
    pipe_file_through_command(mp3file, [
        'ffmpeg', '-i', '-', '-f', 'wav', '-acodec', 'pcm_s16le', filename])
    return filename


def encode_vorbis(wavfile):
    filename = scratchpad()
    pipe_file_through_command(wavfile,
                              ['oggenc', '-q', '6', '-o', filename, '-'])
    return filename


def is_stranger(request):
    return not request.session.get('playlist')
