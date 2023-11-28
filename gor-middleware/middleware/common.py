import sys

"""
Logging to STDERR as STDOUT and STDIN used for data transfer
"""


def log(msg):
    try:
        msg = str(msg) + '\n'
    except:  # lgtm[py/conflicting-attributes]
        pass
    sys.stderr.write(msg)
    sys.stderr.flush()
