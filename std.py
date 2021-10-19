import sys

def std(file, lib):
    print('including std lib...')
    print(lib)
    stdFile = open(lib, 'r')
    lines = stdFile.readlines()

    for line in lines:
        file.write(line)
    file.write('\n')