from libDisk import openDisk, writeBlock, readBlock

# error codes:
# -1 = failed to open disk

BLOCKSIZE = 256
magic_num = 45

open_files = {
    # 1: 0
}

# super block layout
# 0: 1
# 1: 45
# 2: first free block in linked list of free blocks
# 4: first inode in linked list of free inodes

# inode block layout
# 0: 2
# 1: 45
# 2: next inode in linked list of inodes
# 4: first file extent block in linked list of file extent blocks
# 6-13: file name
# 14-: length of file

# file extent block layout
# 0: 3
# 1: 45
# 2: next file extent block in linked list of file extent blocks
# 4-: data

# free block layout
# 0: 4
# 1: 45
# 2: next free block in linked list of free blocks


# Makes a blank TinyFS file system of size nBytes on the file specified by ‘filename’. This function should use the
# emulated disk library to open the specified file, and upon success, format the file to be mountable. This includes
# initializing all data to 0x00, setting magic numbers, initializing and writing the superblock and inodes,
# etc. Must return a specified success/error code.
def tfs_mkfs(filename, nBytes):
    global BLOCKSIZE

    file_num = openDisk(filename, nBytes)
    if file_num < 0:
        return -1

    create_super_block(file_num)
    for i in range(1, nBytes/BLOCKSIZE):
        free_block(file_num, i)


def create_super_block(file_num):
    global BLOCKSIZE
    global magic_num

    out = bytearray(BLOCKSIZE)
    out[0] = 1
    out[1] = magic_num
    out[2] = 1

    writeBlock(file_num, 0, out)


def free_block(file_num, i):
    global BLOCKSIZE
    global magic_num

    super_b = readBlock(file_num, 0)
    first_free = super_b[2]

    new_free = bytearray(BLOCKSIZE)
    new_free[0] = 4
    new_free[1] = magic_num
    new_free[2] = first_free

    writeBlock(file_num, i, new_free)

    super_b[2] = i
    writeBlock(file_num, 0, super_b)



# tfs_mount(char *filename) “mounts” a TinyFS file system located within ‘filename’. tfs_unmount(void) “unmounts” the
# currently mounted file system. As part of the mount operation, tfs_mount should verify the file system is the
# correct type. Only one file system may be mounted at a time. Use tfs_unmount to cleanly unmount the currently
# mounted file system. Must return a specified success/error code.
def tfs_mount(filename):
    pass


def tfs_unmount():
    pass


# Opens a file for reading and writing on the currently mounted file system. Creates a dynamic resource table entry
# for the file, and returns a file descriptor (integer) that can be used to reference this file while the filesystem
# is mounted.
def tfs_openFile(name):
    pass


# Closes the file, de-allocates all system/disk resources, and removes table entry
def tfs_closeFile(FD):
    pass


# Writes buffer ‘buffer’ of size ‘size’, which represents an entire file’s contents, to the file system. Sets the
# file pointer to 0 (the start of file) when done. Returns success/error codes.
def tfs_writeFile(FD, buffer, size):
    pass


# deletes a file and marks its blocks as free on disk.
def tfs_deleteFile(FD):
    pass


# reads one byte from the file and copies it to buffer, using the current file pointer location and incrementing it
# by one upon success. If the file pointer is already at the end of the file then tfs_readByte() should return an
# error and not increment the file pointer.
def tfs_readByte(FD, buffer):
    pass


# change the file pointer location to offset (absolute). Returns success/error codes.
def tfs_seek(FD, offset):
    pass

# In your tinyFS.h file, you must also include the following definitions:

# The default size of the disk and file system block
# define BLOCKSIZE 256

# Your program should use a 10240 Byte disk size giving you 40 blocks total. This is the default size. You must be
# able to support different possible values define DEFAULT_DISK_SIZE 10240

# use this name for a default disk file name
# define DEFAULT_DISK_NAME “tinyFSDisk”
# typedef int fileDescriptor;
