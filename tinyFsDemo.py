from libTinyFS import *


def run_test(test_name, function, *args):
    print('Running: ' + test_name)
    result = function(*args)
    print('Result: ' + str(result))
    return result


# todo: start general behavior display
run_test('Make FS', tfs_mkfs, 'test_backing_store.bin', 10240)  # make fs
# mount fs
# open fs
# create file
# write file
# read byte
# read whole file
# seek
# read byte
# close file
# open file
# read file
# rename file
# close file
# open file
# read file
# close file
# open 2 new files
# list files
# delete file
# list files
# unmount fs

# todo: start error checking
#
