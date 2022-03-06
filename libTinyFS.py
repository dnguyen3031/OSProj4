from libDisk import openDisk


# Makes a blank TinyFS file system of size nBytes on the file specified by ‘filename’. This function should use the
# emulated disk library to open the specified file, and upon success, format the file to be mountable. This includes
# initializing all data to 0x00, setting magic numbers, initializing and writing the superblock and inodes,
# etc. Must return a specified success/error code.
def tfs_mkfs(filename, nBytes):
    openDisk(filename, nBytes)



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
