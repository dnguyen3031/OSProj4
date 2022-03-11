from libTinyFS import *


def run_test(test_name, function, *args):
    print('\nRunning: ' + test_name)
    result = function(*args)
    print('Result: ' + str(result))
    if result != 0:
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
run_test('Close File', tfs_closeFile, FDTest1)  # close file

FDTest1 = run_test('Open FS', tfs_openFile, "test1.txt")  # open new file
FDTest2 = run_test('Open FS', tfs_openFile, "test2.txt")  # open new file
run_test("Read Directory", tfs_readdir)  # list files

run_test("Delete File", tfs_deleteFile, FDTest1)  # delete file

run_test("Read Directory", tfs_readdir)  # list files

FDTest3 = run_test('Open FS', tfs_openFile, "test3.txt")  # open file

# read fd test 3 for timestamp check
# write fd test 3 for timestamp check
# display timestamps
run_test('timestamp creation', tfs_stat_creation, FDTest2)
run_test('timestamp creation', tfs_stat_read, FDTest2)
run_test('timestamp creation', tfs_stat_write, FDTest2)

run_test('timestamp creation', tfs_stat_creation, FDTest3)
run_test('timestamp creation', tfs_stat_read, FDTest3)
run_test('timestamp creation', tfs_stat_write, FDTest3)
# unmount fs
run_test("Unmount FS", tfs_unmount)

# todo: start error checking
#
