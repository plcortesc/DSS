#!/usr/bin/env python

from datetime import datetime
import time
import sys
import threading
import requests
import os

lfnum = -1
lock = threading.Lock()
url = "http://cs553ape.appspot.com"

class multiprocess (threading.Thread):

    def __init__(gae, threadID, op):
        threading.Thread.__init__(gae)
        gae.op = op
        gae.threadID = threadID
  
    def run(gae):
        global lfnum
        lock.acquire()
        fileNum = lfnum + 1
        lfnum = fileNum
        lock.release()
        
        path = "./files"
        dirs = os.listdir(path)
        length = len(dirs)

        while fileNum < length:
            if gae.op == "insert":
                insert(dirs[fileNum],"files/"+dirs[fileNum])
            elif gae.op == "find":
                find(dirs[fileNum])
            elif gae.op == "remove":
                remove(dirs[fileNum])

            lock.acquire()
            fileNum = lfnum + 1
            lfnum = fileNum
            lock.release()

def insert(key, path):
    t1 = datetime.now()
    uploadurl = requests.get(url+"/inserturl").text
    req = requests.post(uploadurl, data={'filekey':key}, files={'file': open(path, 'r')})
    t2 = datetime.now()

    print "Operation: insert ; Time per operation:",(t2-t1).total_seconds()


def find(key):
    t1 = datetime.now()
    req = requests.post(url+"/find", data={'filekey':key})
    t2 = datetime.now()

    print "Operation: find ; Time per operation:",(t2-t1).total_seconds()


def remove(key):
    t1 = datetime.now()
    req = requests.post(url+"/remove", data={'filekey':key})
    t2 = datetime.now()

    print "Operation: remove ; Time per operation:",(t2-t1).total_seconds()

if __name__ == '__main__':
    
    totalThreads = []
    op = sys.argv[1]
    threadsNum = int(sys.argv[2])

    print "Working on it..."

    t1 = datetime.now()

    for thread in range(threadsNum):
        th = multiprocess(thread, op)
        th.start()
        totalThreads.append(th)

    for thread in totalThreads:
        thread.join()

    t2 = datetime.now()
    totTime = (t2-t1).total_seconds()    

    print "Operation:", op,", Number of threads:", threadsNum, ", TOTAL TIME:",totTime

