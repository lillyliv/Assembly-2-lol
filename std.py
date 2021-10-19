import sys

def std(file):
    print('including std lib...')
    stdFile = open('libs/std.asm', 'r')
    lines = stdFile.readlines()

    for line in lines:
        file.write(line)
    file.write('\n')
