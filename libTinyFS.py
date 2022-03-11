from libDisk import openDisk, writeBlock, readBlock, closeDisk
import math, time

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

BLOCKSIZE = 256
magic_num = 6
disk_num = -1

open_files = {
    # file's inode block location: read point
}

# super block layout
# 0: 1
# 1: 45
# 2: first inode in linked list of free inodes
# 4: first free block in linked list of free blocks

# inode block layout
# 0: 2
# 1: 45
# 2: next inode in linked list of inodes
# 4: first file extent block in linked list of file extent blocks
# 6-13: file name
# 14-23: creation time
# 24-33: update time
# 34-43: read time
# 44-: length of file

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
    for i in range(1, int(math.ceil(nBytes / BLOCKSIZE))):
        free_block(file_num, i)

    closeDisk(file_num)
    return 0


def create_super_block(file_num):
    global BLOCKSIZE
    global magic_num

    out = bytearray(BLOCKSIZE)
    out[0] = 1
    out[1] = magic_num

    writeBlock(file_num, 0, out)


def free_block(file_num, i):
    global BLOCKSIZE
    global magic_num

    super_b = readBlock(file_num, 0)
    first_free = super_b[4]

    new_free = bytearray(BLOCKSIZE)
    new_free[0] = 4
    new_free[1] = magic_num
    new_free[2] = first_free

    writeBlock(file_num, i, new_free)

    super_b[4] = i
    writeBlock(file_num, 0, super_b)


# tfs_mount(char *filename) “mounts” a TinyFS file system located within ‘filename’. tfs_unmount(void) “unmounts” the
# currently mounted file system. As part of the mount operation, tfs_mount should verify the file system is the
# correct type. Only one file system may be mounted at a time. Use tfs_unmount to cleanly unmount the currently
# mounted file system. Must return a specified success/error code.
def tfs_mount(filename):
    global disk_num
    global magic_num

    if disk_num >= 0:
        return -2

    disk_num = openDisk(filename, 0)
    if disk_num < 0:
        return -1

    if not readBlock(disk_num, 0)[1] == magic_num:
        closeDisk(disk_num)
        disk_num = -1
        return -3

    return 0


def tfs_unmount():
    global disk_num

    if disk_num < 0:
        return -4

    closeDisk(disk_num)
    disk_num = -1
    return 0


# Opens a file for reading and writing on the currently mounted file system. Creates a dynamic resource table entry
# for the file, and returns a file descriptor (integer) that can be used to reference this file while the filesystem
# is mounted.
def tfs_openFile(name):
    global open_files
    global disk_num

    if disk_num < 0:
        return -4

    super_block = readBlock(disk_num, 0)

    if super_block is int:
        return -6

    inode_location = super_block[2]
    inode = readBlock(disk_num, inode_location)

    while inode_location != 0 and inode[6:14].decode("utf-8") != name:
        inode_location = inode[2]
        inode = readBlock(disk_num, inode_location)
        if inode is int:
            return -6

    if inode[6:14].decode("utf-8") != name:
        inode_location = create_inode(name)

    open_files[inode_location] = 0

    return inode_location


def create_inode(name):
    global BLOCKSIZE
    global magic_num
    global disk_num

    super_block = readBlock(disk_num, 0)
    new_inode_location = super_block[4]

    timestamp = str(int(time.time())).encode("utf-8")

    new_inode = bytearray(BLOCKSIZE)
    new_inode[0] = 2
    new_inode[1] = magic_num
    new_inode[2] = super_block[2]
    new_inode = new_inode[:6] + name[:8].encode("utf-8") + new_inode[14:]
    new_inode = new_inode[:14] + timestamp + new_inode[24:]
    new_inode = new_inode[:24] + timestamp + new_inode[34:]
    new_inode = new_inode[:34] + timestamp + new_inode[44:]

    super_block[2] = super_block[4]
    temp = readBlock(disk_num, super_block[4])
    super_block[4] = temp[2]

    writeBlock(disk_num, 0, super_block)
    writeBlock(disk_num, new_inode_location, new_inode)

    return new_inode_location


# Closes the file, de-allocates all system/disk resources, and removes table entry
def tfs_closeFile(FD):
    global open_files
    global disk_num

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    del open_files[FD]
    return 0


# Writes buffer ‘buffer’ of size ‘size’, which represents an entire file’s contents, to the file system. Sets the
# file pointer to 0 (the start of file) when done. Returns success/error codes.
def tfs_writeFile(FD, buffer, size):
    global disk_num
    global open_files
    global BLOCKSIZE

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    inode = readBlock(disk_num, FD)
    if inode == -1:
        return -6

    if inode[4] != 0:
        free_extent_blocks(inode[4])

    blocks_needed = math.ceil(size / (BLOCKSIZE - 4))
    last_block = create_new_extent_block(buffer[(blocks_needed - 1) * (BLOCKSIZE - 4):], 0)  # ned to pad
    for i in range(blocks_needed - 2, -1, -1):
        last_block = create_new_extent_block(buffer[i * (BLOCKSIZE - 4):(i + 1) * (BLOCKSIZE - 4)], last_block)
        if last_block < 0:
            return -8

    open_files[FD] = 0
    timestamp = str(int(time.time())).encode("utf-8")
    inode = inode[:24] + timestamp + inode[34:]
    inode = inode[:34] + timestamp + inode[44:]
    inode[4] = last_block
    encoded_size = str(size).encode("utf-8")
    inode = inode[:44] + encoded_size + inode[44+len(encoded_size):]

    if writeBlock(disk_num, FD, inode) == -1:
        return -7
    return 0


def free_extent_blocks(block_num):
    global BLOCKSIZE
    global magic_num
    global disk_num

    next_extent_block = readBlock(disk_num, block_num)[2]
    super_block = readBlock(disk_num, 0)

    first_free = super_block[4]

    new_free = bytearray(BLOCKSIZE)
    new_free[0] = 4
    new_free[1] = magic_num
    new_free[2] = first_free

    writeBlock(disk_num, block_num, new_free)

    super_block[4] = block_num
    writeBlock(disk_num, 0, super_block)

    if next_extent_block == 0:
        return 0
    free_extent_blocks(next_extent_block)


def create_new_extent_block(data, last_block):
    global disk_num
    global magic_num

    super_block = readBlock(disk_num, 0)
    next_free = super_block[4]
    super_block[4] = readBlock(disk_num, next_free)[2]

    if writeBlock(disk_num, 0, super_block) == -1:
        return -7

    if writeBlock(disk_num, next_free, bytearray([3, magic_num, last_block, 0] + list(data))) == -1:
        return -7
    return next_free


# deletes a file and marks its blocks as free on disk.
def tfs_deleteFile(FD):
    global BLOCKSIZE
    global magic_num
    global disk_num

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    inode = readBlock(disk_num, FD)
    if inode == -1:
        return -6

    if inode[4] != 0:
        free_extent_blocks(inode[4])

    super_block = readBlock(disk_num, 0)

    first_free = super_block[4]

    new_free = bytearray(BLOCKSIZE)
    new_free[0] = 4
    new_free[1] = magic_num
    new_free[2] = first_free

    next_inode = super_block[2]
    prev_inode = -1
    prev_inode_num = -1
    while next_inode != FD:
        prev_inode_num = next_inode
        prev_inode = readBlock(disk_num, next_inode)

        if isinstance(prev_inode, int) and prev_inode < 0:
            return -6
        next_inode = prev_inode[2]

    if prev_inode == -1:
        super_block[2] = inode[2]
    else:
        prev_inode[2] = inode[2]
        writeBlock(disk_num, prev_inode_num, prev_inode)

    writeBlock(disk_num, FD, new_free)

    super_block[4] = FD
    writeBlock(disk_num, 0, super_block)

    del open_files[FD]
    return 0


# reads one byte from the file and copies it to buffer, using the current file pointer location and incrementing it
# by one upon success. If the file pointer is already at the end of the file then tfs_readByte() should return an
# error and not increment the file pointer.
def tfs_readByte(FD, buffer=None):
    global disk_num
    global open_files
    global BLOCKSIZE

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    inode = readBlock(disk_num, FD)
    if inode == -1:
        return -6

    timestamp = str(int(time.time())).encode("utf-8")
    inode = inode[:34] + timestamp + inode[44:]
    writeBlock(disk_num, FD, inode)

    target_block = open_files[FD] // (BLOCKSIZE - 4)
    target_offset = open_files[FD] % (BLOCKSIZE - 4) + 4

    block = readBlock(disk_num, inode[4])
    for i in range(target_block):
        if block == -1:
            return -10
        block = readBlock(disk_num, block[2])

    open_files[FD] += 1
    return block[target_offset]


# change the file pointer location to offset (absolute). Returns success/error codes.
def tfs_seek(FD, offset):
    global disk_num
    global open_files

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    open_files[FD] = offset
    return 0


# Renames a file.  New name should be passed in.
def tfs_rename(old_name, name):
    global open_files
    global disk_num

    if disk_num < 0:
        return -4

    super_block = readBlock(disk_num, 0)

    if isinstance(super_block, int) and super_block < 0:
        return -6

    inode_location = super_block[2]
    inode = readBlock(disk_num, inode_location)

    while inode_location != 0 and inode[6:14].decode("utf-8") != old_name:
        inode_location = inode[2]
        inode = readBlock(disk_num, inode_location)
        if inode < 0:
            return -6

    if inode[6:14].decode("utf-8") != old_name:
        return -9

    inode = inode[:6] + name[:8].encode("utf-8") + inode[14:]

    writeBlock(disk_num, inode_location, inode)

    return 0


# lists all the files and directories on the disk
def tfs_readdir():
    global disk_num
    global open_files
    global BLOCKSIZE

    super_block = readBlock(disk_num, 0)

    if isinstance(super_block, int) and super_block < 0:
        return -6

    next_inode = super_block[2]

    while next_inode != 0:
        inode = readBlock(disk_num, next_inode)
        if isinstance(inode, int) and inode < 0:
            return -6
        next_inode = inode[2]
        print(inode[6:14].decode("utf-8"))

    return 0

def tfs_stat_creation(FD):
    global disk_num
    global open_files
    global BLOCKSIZE

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    inode = readBlock(disk_num, FD)
    if inode == -1:
        return -6

    dec = (inode[14:24])
    return int(inode[14:24].decode("utf-8"))

def tfs_stat_write(FD):
    global disk_num
    global open_files
    global BLOCKSIZE

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    inode = readBlock(disk_num, FD)
    if inode == -1:
        return -6

    dec = (inode[24:34])
    return int(inode[24:34].decode("utf-8"))

def tfs_stat_read(FD):
    global disk_num
    global open_files
    global BLOCKSIZE

    if disk_num < 0:
        return -4

    if FD not in open_files.keys():
        return -5

    inode = readBlock(disk_num, FD)
    if inode == -1:
        return -6

    dec = (inode[34:44])
    return int(inode[34:44].decode("utf-8"))

# In your tinyFS.h file, you must also include the following definitions:

# The default size of the disk and file system block
# define BLOCKSIZE 256

# Your program should use a 10240 Byte disk size giving you 40 blocks total. This is the default size. You must be
# able to support different possible values define DEFAULT_DISK_SIZE 10240

# use this name for a default disk file name
# define DEFAULT_DISK_NAME “tinyFSDisk”
# typedef int fileDescriptor;
