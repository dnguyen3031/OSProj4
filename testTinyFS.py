from libTinyFS import *
import os

default_size = 10240

class Test(object):
    def demo01(self):
        #test if mkfs works by verifying bytes
        print("Running Demo01")
        tfs_mkfs("BACKING_STORE.bin", default_size)
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
        #test open and closing of a file, with a readByte
        print("Running Demo03")
        tfs_mkfs("BACKING_STORE.bin", default_size)
        tfs_mount("BACKING_STORE.bin")
        FD = tfs_openFile("test.txt")
        # should we call write before readByte? or can we set open_file[FD] to 0 in tfs_openFile
        print(FD)
        byte = tfs_readByte(FD)
        print(byte)
        tfs_closeFile(FD)
        tfs_unmount()

    def demo04(self):
        #test open and closing of a file, with a seek, then readByte
        print("Running Demo04")
        tfs_mkfs("BACKING_STORE.bin", default_size)
        tfs_mount("BACKING_STORE.bin")
        FD = tfs_openFile("test.txt")
        print(FD)
        tfs_seek(FD, 256)
        byte = tfs_readByte(FD)
        print(byte)
        tfs_closeFile(FD)
        tfs_unmount()

    def demoError01(self):
        #attempt to run without mounting (should return -4)
        print("Running Demo03")
        tfs_mkfs("BACKING_STORE.bin", default_size)
        FD = tfs_openFile("test.txt")
        print(FD)
        byte = tfs_readByte(FD)
        print(byte)
        tfs_closeFile(FD)

    #b'\xb8\xaa\x4b\x1e\x5e\x4a\x29\xab\x5f\x49'



if __name__ == '__main__':
    Test().demo04()