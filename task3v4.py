import os
import time
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

def bytes(x):
    return (sys.getsizeof(x) - 33)

def file_gen(file_name, length):
    # generate a file of random data
    f = open(file_name, "wb")
    pt = os.urandom(length)
    print(str(bytes(pt)) + " byte file generated")
    f.write(pt)
    f.close()
    return

def sha_hash(file_name):
    # read data file and create a hash
    shaHash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    f = open(file_name, "rb")
    data = f.read()
    f.close()
    
    # Record time while generating hash based on the data
    start_time = time.perf_counter_ns()
    shaHash.update(data)
    shaHV = shaHash.finalize()
    elapse = time.perf_counter_ns() - start_time

    # save hash as a file
    f = open(file_name + "sha", "wb")
    f.write(shaHV)
    f.close()

    # return time taken to create hash from data
    #print(str(bytes(shaHV)) + " byte SHA-256 hash created in " + str(elapse) + " ns")
    return elapse

def md5_hash(file_name):
    # read data file and create a hash
    md5Hash = hashes.Hash(hashes.MD5(), backend=default_backend())
    f = open(file_name, "rb")
    data = f.read()
    f.close()
    
    # Record time while generating hash based on the data
    start_time = time.perf_counter_ns()
    md5Hash.update(data)
    md5HV = md5Hash.finalize()
    elapse = time.perf_counter_ns() - start_time

    # save hash as a file
    f = open(file_name + "md5", "wb")
    f.write(md5HV)
    f.close()

    # return time taken to create hash from data
    return elapse

runs = 100
filesize = [8, 16, 32, 500, 1000, 2000] #length in bytes of the data files to be created

# Generate several files of different lengths
for i in range(6):
    file_gen("file" + str(i), filesize[i])
print()

# Hash the file with SHA256 multiple times and calculate hashes/sec from the average
for i in range(6):
    shaSum = 0
    for j in range(len(filesize)):
        shaSum = shaSum + sha_hash("file" + str(i))
    shaAvg = shaSum / runs
    print(str(filesize[i]) + " byte file hashed with SHA256 " + str(runs) + " times")
    print("\t" + '{0:.3f}'.format(shaAvg) + " ns/hash")
    shaPerSec = 1 / (shaAvg * 0.000000001)  # Calculate hash/sec from average ns
    print("\t" + '{0:.3f}'.format(shaPerSec) + " hash/s")
print()

# Hash with the file with MD5 multiple times and calculate hashes/sec from the average
for i in range(6):
    md5Sum = 0
    for j in range(len(filesize)):
        md5Sum = md5Sum + md5_hash("file" + str(i))
    md5Avg = md5Sum / runs
    print(str(filesize[i]) + " byte file hashed with MD5 " + str(runs) + " times")
    print("\t" + '{0:.3f}'.format(md5Avg) + "\tns/hash")
    md5PerSec = 1 / (md5Avg * 0.000000001) # Calculate hash/sec from average ns
    print("\t" + '{0:.3f}'.format(md5PerSec) + "\thash/s")
print()
