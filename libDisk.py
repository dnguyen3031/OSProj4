import os.path

BLOCKSIZE = 256
disks = {
    # 1: {
    #     'file_name': some file,
    #     'contents': some byte array
    #     'nBytes': 1
    # }
}


# This function opens a regular UNIX file and designates the first nBytes of it as space for the emulated disk.
# nBytes should be a number that is evenly divisible by the block size. If nBytes > 0 and there is already a file by
# the given filename, that disk is resized to nBytes, and that file’s contents may be overwritten. If nBytes is 0,
# an existing disk is opened, and should not be overwritten. There is no requirement to maintain integrity of any
# content beyond nBytes. Errors must be returned for any other failures, as defined by your own error code system.
def getByteArray(filename, nBytes):
    with open(filename, 'rb') as f:
        return bytearray(f.read(nBytes))

# def getByteArray(filename, nBytes):
#     f = open(filename, 'rb')
#     frame = f.read(nBytes)
#     clean = codecs.encode(bytes(frame), 'hex').decode("utf-8").upper()
#     f.close()
#
#     return clean

def openDisk(filename, nBytes):
    global BLOCKSIZE
    global disks
    if nBytes == 0:
        if os.path.exists(filename):
            b_array = getByteArray(filename, os.path.getsize(filename))
            disks[len(disks)] = {'file_name': filename, 'nBytes': os.path.getsize(filename), 'contents': b_array}
        else:
            return -1 #error of file
    else:
        if not os.path.exists(filename):
            f = open(filename, "w+")
            b_array = bytearray(nBytes)
            f.close()
        else:
            b_array = getByteArray(filename, nBytes)

        disks[len(disks)] = {'file_name': filename, 'nBytes': nBytes, 'contents': b_array}


# readBlock() reads an entire block of BLOCKSIZE bytes from the open disk (identified by ‘disk’) and copies the
# result into a local buffer (must be at least of BLOCKSIZE bytes). The bNum is a logical block number, which must be
# translated into a byte offset within the disk. The translation from logical to physical block is straightforward:
# bNum=0 is the very first byte of the file. bNum=1 is BLOCKSIZE bytes into the disk, bNum=n is n*BLOCKSIZE bytes
# into the disk. On success, it returns 0. Errors must be returned if ‘disk’ is not available (i.e. hasn’t been
# opened) or for any other failures, as defined by your own error code system.
def readBlock(disk, bNum, block=None):
    global BLOCKSIZE
    global disks

    if disk not in disks.keys() or (bNum+1)*BLOCKSIZE > disks[disk].nBytes:
        return -1

    return disks[disk].contents[bNum*BLOCKSIZE:(bNum + 1) * BLOCKSIZE]


# writeBlock() takes disk number ‘disk’ and logical block number ‘bNum’ and writes the content of the buffer ‘block’
# to that location. BLOCKSIZE bytes will be written from ‘block’ regardless of its actual size. The disk must be
# open. Just as in readBlock(), writeBlock() must translate the logical block bNum to the correct byte position in
# the file. On success, it returns 0. Errors must be returned if ‘disk’ is not available (i.e. hasn’t been opened) or
# for any other failures, as defined by your own error code system.
def writeBlock(disk, bNum, block):
    global BLOCKSIZE
    global disks

    if disk not in disks.keys() or (bNum + 1) * BLOCKSIZE > disks[disk].nBytes:
        return -1

    disks[disk].contents = disks[disk].contents[:bNum*BLOCKSIZE] + block + disks[disk].contents[(bNum+1)*BLOCKSIZE:]
    return 0


# closeDisk() takes a disk number ‘disk’ and makes the disk closed to further I/O; i.e. any subsequent reads or
# writes to a closed disk should return an error. Closing a disk should also close the underlying file, committing
# any writes being buffered by the real OS.
def closeDisk(disk):
    global BLOCKSIZE
    global disks

    dDisk = disks[disk]
    with open(dDisk['file_name'], "wb") as binary_file:
        binary_file.write(dDisk['contents'])

    del disks[disk]
