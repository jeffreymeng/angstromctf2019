import string
import sys

search = string.ascii_lowercase + '_'

def decrypt(result):
    char = ord(result)
    for c in search:
        for c2 in search:
            if ord(c) ^ ord(c2) == char:
                print('{} {}'.format(c, c2))

decrypt(sys.argv[1])
