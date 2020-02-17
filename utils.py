import os


def is_pure_abc(s):
    charr = [',', '.', '-', ' ']
    for ch in s:
        c = ord(ch)  # ascii
        if (c > 122 or c < 48) and (ch not in charr):
            return False
    return True
