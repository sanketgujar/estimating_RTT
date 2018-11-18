# coding: utf-8

import pandas as pd
import numpy as np
import csv
import glob
import os
import sys
from threading import Timer
import subprocess
import multiprocessing
from signal import SIGKILL
import signal
from os import kill
def write_txt_to_csv(txt):
    num_lines = sum(1 for line in open(txt))
    csv_name = txt.split('.')[0]
    f1 = open(txt,"r")
    s1 = []
    for i in range(4):
        f1.readline()
    for j in range(4,num_lines-4):
        line  = f1.readline()
        tokens = line.split()
        #print (tokens)
        s1.append(tokens)
    df = pd.DataFrame(s1)
    df.columns = ['reply_type','time_s','rtt_us','ttl','probe_addr','reply_addr']
    df.to_csv(csv_name + '.csv', index=False)
    #saves the csv to file


def kill_proc(proc):
    # os.kill(p, signal.SIGTERM)
    kill(proc.pid, SIGKILL)
    exit(proc.wait())
    print ('The process is killed')

if __name__ == '__main__':
    file_path = sys.argv[-1] + '/*.bz2'
    print (file_path)
    print (sys.argv)
    bin_files = glob.glob(file_path)
    print ('The zip files are : ', bin_files)
    for file in bin_files:
        print ("Converting " + file +" to txt")
        name_file = file.split('.')[-2]
        name_file += '.txt'
        command_line = './print_datafile  -j ' + file  + ' > '+ name_file
        print (command_line)
        seconds  = 60
        print ('Process Started')
        p = subprocess.Popen(command_line, shell = True)
        print ('Starting timer for ', seconds, '  secs')
        t = Timer(seconds, kill_proc, [p])
        t.start()
        print ('Waiting for process and timer to finish')
        # wait for the test process to return
        rcode = p.wait()
        t.cancel()
        print ('Converting done')
        print ('Converting text to csv')
        write_txt_to_csv(name_file)
        print (' Finished with this job')
