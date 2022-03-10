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
run_test('Open FS', tfs_openFile, "test.txt")
# create file

# write file
# read byte
# read whole file
# seek
# read byte
# close file
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
# unmount fs
run_test("Unmount FS", tfs_unmount)

# todo: start error checking
#
