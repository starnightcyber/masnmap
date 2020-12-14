#!/usr/bin/python
# coding=utf-8


import nmap
import datetime
import json
from queue import Queue
from multiprocessing import Pool
import os


ip_file = 'ips.txt'
# masscan_exe = '/usr/local/bin/masscan'
masscan_exe = '/usr/bin/masscan'
masscan_rate = 2000
masscan_file = 'masscan.json'
task_queue = Queue()
result_queue = Queue()
process_num = 50
total_ports = 0
services_info = []


def run_masscan():
    command = 'sudo {} -iL {} -p 1-65535 -oJ {} --rate {}'.format(masscan_exe, ip_file, masscan_file, masscan_rate)
    msg = 'executing ==> {}'.format(command)
    print(msg)
    os.system(command)
    pass


def extract_masscan():
    """
    extract masscan result file masscan.json into ip:port format, and add to queue
    """
    with open(masscan_file, 'r') as fr:
        tmp_lines = fr.readlines()
        lines = tmp_lines[1:-1]
        global total_ports
        total_ports = len(lines)
        for line in lines:
            tmp = line.strip(',\n')
            line_json = json.loads(tmp)
            # print(line_json)
            # extract ip & port
            ip = line_json['ip']
            port = line_json['ports'][0]['port']

            # combine ip:port, and add to queue
            ip_port = '{}:{}'.format(ip, port)
            task_queue.put(ip_port)
            print(ip_port)
            # exit()
    pass


def nmap_scan(ip_port, index):
    # print('scan ==> {}'.format(ip_port))
    try:
        ip, port = ip_port.split(':')
        nm = nmap.PortScanner()
        ret = nm.scan(ip, port, arguments='-Pn,-sS')
        service = ret['scan'][ip]['tcp'][int(port)]['name']
        msg = '{}:{}:{}:{}'.format(index, ip, port, service)
        print(msg)
        return msg
    except:
        print('sth bad happen ...')


def setcallback(msg):
    services_info.append(msg)


def run_nmap():
    pool = Pool(process_num)  # 创建进程池
    index = 0
    while not task_queue.empty():
        index += 1
        ip_port = task_queue.get(timeout=1.0)
        pool.apply_async(nmap_scan, args=(ip_port, index), callback=setcallback)
    pool.close()
    pool.join()


def save_results():
    print('save_results ...')
    print("services {} lines".format(len(services_info)))
    with open("services.txt", 'w') as fw:
        for line in services_info:
            fw.write(line+'\n')


def main():
    # Step 1, run masscan to detect all the open port on all ips
    run_masscan()

    # Step 2, extract masscan result file:masscan.json to ip:port format
    extract_masscan()

    # Step 3, using nmap to scan ip:port
    run_nmap()

    # Step 4, save results
    save_results()


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    spend_time = (end - start).seconds
    msg = 'It takes {} process {} seconds to run ... {} tasks'.format(process_num, spend_time, total_ports)
    print(msg)
