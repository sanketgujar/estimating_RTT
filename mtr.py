import numpy as np
import os
import sys
import pdb
import subprocess
import matplotlib.pyplot as plt
import pandas as pd




def convert_str_to_avg(out, indx = -4):
    out  = out.decode('utf-8').split('\n')
    filter_indx  = indx
    filter_data  = []  #avg -4
    ip_data      = []
    for i in range(2, len(out)-1):
        curr_line  = out[i].split(' ')
        curr_line  = ' '.join(curr_line).split()
        try:
            filter_data.append(float(curr_line[filter_indx]))
            ip_data.append(curr_line)
        except:
            print ('The loop Broke')
            # pdb.set_trace()
    ip_id = np.argmax(filter_data)
    latency_ip = ip_data[ip_id][2]
    latency_As = ip_data[ip_id][1]
    return filter_data, latency_ip, latency_As, filter_data[ip_id]


if __name__ == '__main__':
    #read the ip
    final_data = []
    df = pd.read_csv('../../zmap_data/high_latency/combined_high_latency.csv')
    Ip = df['saddr'].values
    counter = 1
    for ip in Ip:
        # ip = '8.8.8.8'
        print ('Starting Process for ', str(ip))
        cmnd = 'mtr --report-wide  --no-dns --show-ips --aslookup -Z 60 '
        cmnd += str(ip)
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, shell = True)
        res= p.communicate()
        data, high_ip, As, rtt = convert_str_to_avg(res[0])
        final_data.append([ip,high_ip, As, rtt])
        print ('Finised Process for ', str(ip))
        if counter % 50 == 0:
            #pdb.set_trace()
            final_data_1  = np.reshape(final_data, (-1,4))
            df1 = pd.DataFrame({'Ip' : final_data_1[:,0],
                                'high_ip': final_data_1[:,1],
                                'As' : final_data_1[:,2],
                                'rtt' : final_data_1[:,3]})
            df1.to_csv('High_hop_locati.csv')
            print ('********CSV files stored******')
        counter += 1
    # pdb.set_trace()
