#!/usr/bin/env python

import numpy as np
import multiprocessing as mp
import sys
import mmap
import time


def do_something_with_frame(frame):
    print("processing a frame:")
    return 100


def frame_supplier(filename,keyword=b'Begin: Segment'):
    """A generator for frames"""
    f = open(filename)
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    cursor = 0
    while True:
        initial = s.find(keyword, cursor)
        if initial == -1:
            break
        cursor = initial + 14
        final = s.find(keyword, cursor)

        yield s[initial:final]

        if final == -1:
            break


def main():
    """Process a file of atom frames

    Args:
      filename: the file to process
      processes: the size of the pool
    """
    filename = sys.argv[1]
    nump = int(sys.argv[2])

    frames = frame_supplier(filename)

    pool = mp.Pool(nump)

    # play around with the chunksize
    for result in pool.imap(do_something_with_frame, frames, chunksize=10):
        print(result)


def plain_run(keyword='Begin: Segment'):
    frame = []
    with open(filename) as file:
        for line in file:
            if line.beginswith(keyword):
                yield frame
            else:
                frame.append(line)


if __name__=='__main__':
    #data = np.random.random(size=(400,400))
    #print (data.shape)
    #np.savetxt('Random_num.dat',data)
    
    st = time.time()
    main()
    print ('Use Multiprocessing, time = {:8.5f}'.format(time.time()-st))

    st = time.time()
    plain_run()
    print ('No  Multiprocessing, time = {:8.5f}'.format(time.time()-st))
