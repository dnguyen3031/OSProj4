#! /usr/bin/env python3

from libTinyFS import *
import time


def run_test(test_name, function, *args):
    print('\nRunning: ' + test_name)
    result = function(*args)
    print('Result: ' + str(result))
    if 256 > result > 0:
        print('Decoded Result: ' + bytearray([result]).decode("utf-8"))
    return result


def print_whole_file(filename, FD):
    out = []
    tfs_seek(FD, 0)
    for i in range(len(sample_data)):
        out += [tfs_readByte(FD)]
    print("\nContents of " + filename + ":\n" + bytearray(out).decode("utf-8"))


# Test Behavior #
run_test('Make FS', tfs_mkfs, 'test_backing_store.bin', 10240)  # make fs
run_test('Mount FS', tfs_mount, "test_backing_store.bin")  # mount fs
FDTest = run_test('Open FS', tfs_openFile, "test.txt")  # open file

# write file
sample_data = "This is some sample data to write in a virtual file!".encode("utf-8")
run_test('Write Data to test.txt', tfs_writeFile, FDTest, sample_data, len(sample_data))

run_test('Read Byte', tfs_readByte, FDTest)  # read byte
run_test('Seek 5', tfs_seek, FDTest, 5)  # seek
run_test('Read Byte', tfs_readByte, FDTest)  # read byte
print_whole_file('test.txt', FDTest)  # read whole file
print_whole_file('test.txt', FDTest)  # read whole file
run_test('Close File', tfs_closeFile, FDTest)  # close file
FDTest = run_test('Open FS', tfs_openFile, "test.txt")  # open file
print_whole_file('test.txt', FDTest)  # read whole file
run_test('Rename File', tfs_rename, "test.txt", "newname.txt")  # rename file
print_whole_file('test.txt', FDTest)  # read whole file

run_test('Close File', tfs_closeFile, FDTest)  # close file

FDTest1 = run_test('Open FS', tfs_openFile, "test1.txt")  # open file

# read file
run_test("Delete File", tfs_deleteFile, FDTest1)  # close file

FDTest1 = run_test('Open FS', tfs_openFile, "test1.txt")  # open new file
FDTest2 = run_test('Open FS', tfs_openFile, "test2.txt")  # open new file
run_test("Read Directory", tfs_readdir)  # list files

run_test("Delete File", tfs_deleteFile, FDTest1)  # delete file

run_test("Read Directory", tfs_readdir)  # list files

FDTest3 = run_test('Open FS', tfs_openFile, "test3.txt")  # open file

# read fd test 3 for timestamp check
# write fd test 3 for timestamp check
# display timestamps
# run_test('timestamp creation', tfs_stat_creation, FDTest3)
# run_test('timestamp last read', tfs_stat_read, FDTest3)
# run_test('timestamp last written', tfs_stat_write, FDTest3)


time.sleep(2)
sample_data = "This is some sample data to write in a virtual file!".encode("utf-8")
run_test('Write Data to test.txt', tfs_writeFile, FDTest3, sample_data, len(sample_data))
time.sleep(2)
run_test('Read Byte', tfs_readByte, FDTest3)

run_test('timestamp creation', tfs_stat_creation, FDTest3)
run_test('timestamp last read', tfs_stat_read, FDTest3)
run_test('timestamp last written', tfs_stat_write, FDTest3)
# unmount fs
run_test("Unmount FS", tfs_unmount)


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

run_error_test("-1", "accessing bad backing store", tfs_mkfs, "BACKING_STORE_NOT_REAL.bin", 0)

tfs_mkfs('test_backing_store.bin', 10240)
tfs_mount('test_backing_store.bin')
run_error_test('-2', 'bad mount', tfs_mount, 'test_backing_store.bin')
tfs_unmount()

openDisk("BACKING_STORE_UNFORMATTED.bin", 0)
run_error_test('-3', 'bad format for mount', tfs_mount, "BACKING_STORE_UNFORMATTED.bin")

run_error_test("-4", "no mounted file system", tfs_unmount)

tfs_mount('test_backing_store.bin')
run_error_test("-5", "attempted to close non-open file", tfs_closeFile, 18)

tfs_unmount()
run_error_test("-6", "failed to create new block", tfs_readdir)

tfs_mkfs('test_backing_store.bin', 10240)
tfs_mount('test_backing_store.bin')
run_error_test("-9", "accessing non-existent file", tfs_rename, "NOT_REAL_FILE", "NOT_RELEVANT")
