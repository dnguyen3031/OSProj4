from libTinyFS import *


def run_test(test_name, function, *args):
    print('Running: ' + test_name)
    result = function(*args)
    print('Result: ' + str(result))
    return result


# todo: start general behavior display
run_test('Make FS', tfs_mkfs, 'test_backing_store.bin', 10240)  # make fs
# mount fs
run_test('Mount FS', tfs_mount, "BACKING_STORE.bin")
# open fs
FDTest = run_test('Open FS', tfs_openFile, "test.txt")
# create file
# write file
# read byte
run_test('Read Byte', tfs_readByte, FDTest)
# read whole file
# seek
# read byte
run_test('Read Byte', tfs_readByte, FDTest)
# close file
run_test('Close File', tfs_closeFile, FDTest)
# open file
FDTest1 = run_test('Open FS', tfs_openFile, "test1.txt")
# read file
# rename file
run_test('Rename File', tfs_rename, "test1.txt", "newname.txt")
# close file
run_test('Close File', tfs_closeFile, FDTest1)
# open file
FDTest1 = run_test('Open FS', tfs_openFile, "test1.txt")
# read file
# close file
run_test('Close File', tfs_closeFile, FDTest1)
# open 2 new files
FDTest1 = run_test('Open FS', tfs_openFile, "test1.txt")
FDTest2 = run_test('Open FS', tfs_openFile, "test2.txt")
# list files
run_test("Read Directory", tfs_readdir)
# delete file
run_test("Delete File", tfs_deleteFile(FDTest1))
# list files
run_test("Read Directory", tfs_readdir)
# open file
FDTest3 = run_test('Open FS', tfs_openFile, "test3.txt")
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
