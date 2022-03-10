from libTinyFS import *
import os

class Test(object):
    def demo01(self):
        #test if mkfs works by verifying bytes
        print("Running Demo01")
        tfs_mkfs("BACKING_STORE.bin", 256*3)
        f = open("BACKING_STORE.bin", "rb")
        print(f.read())
        file_size = os.path.getsize("BACKING_STORE.bin")
        print("File Size is :", file_size, "bytes")

    def demo02(self):
        #test mkfs by verifying that opening with 0 bytes still leaves 5 after demo01
        print("Running Demo02")
        tfs_mkfs("BACKING_STORE.bin", 0)
        f = open("BACKING_STORE.bin", "rb")
        print(f.read())
        file_size = os.path.getsize("BACKING_STORE.bin")
        print("File Size is :", file_size, "bytes")

    def demo03(self):
        #test open and closing of a file
        print("Running Demo03")
        tfs_mkfs("BACKING_STORE.bin", 256 * 3)
        tfs_mount("BACKING_STORE.bin")
        FD = tfs_openFile("test.txt")
        print(FD)
        byte = tfs_readByte(FD)
        print(byte)
        tfs_closeFile(FD)
        tfs_unmount()

    def demoError01(self):
        #attempt to run without mounting (should return -4)
        print("Running Demo03")
        tfs_mkfs("BACKING_STORE.bin", 256 * 3)
        FD = tfs_openFile("test.txt")
        print(FD)
        byte = tfs_readByte(FD)
        print(byte)
        tfs_closeFile(FD)

    #b'\xb8\xaa\x4b\x1e\x5e\x4a\x29\xab\x5f\x49'



if __name__ == '__main__':
    Test().demo03()