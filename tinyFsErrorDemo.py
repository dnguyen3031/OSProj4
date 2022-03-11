from libTinyFS import *
import time


# error codes:
# -1 = failed to open disk
# -2 = attempted to mount an already mounted disk
# -3 = disk not formatted to mount TinyFS
# -4 = no mounted file system
# -5 = attempted to close non-open file
# -6 = failed to read block
# -7 = failed to write block
# -8 = failed to create new block
# -9 = failed to find file
# -10 = eof

def run_error_test(expectederror, test_name, function, *args):
    print('\nRunning Error on: ' + test_name)
    result = function(*args)
    print('Result: ' + str(result))
    if result < 0:
        print("You have correctly returned an error! Expected: " + expectederror + " Error returned: " + str(result))
    return result


# todo: start error checking
#

run_error_test("-1", "accessing bad backing store", tfs_mkfs, "BACKING_STORE_NOT_REAL.bin", 0)
