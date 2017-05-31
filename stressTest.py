#!/usr/bin/python3
import queue
import threading
import socket
import time


ip_port = ('dev.adapi.revanow.com',80)
req = """POST /adapi/load/1002 HTTP/1.1\nHOST:dev.adapi.revanow.com\nContent-Type:application/json\nContent-Length:409\n\n{"androidId":"d25be5d642710594","appVer":"1.0","brand":"E3658","dataProt":"json","device":"E3658","deviceType":"phone","imei1":"325","imsi":null,"language":"US","model":"Y13","netWork":"WIFI","opName":"unknown","osVersion":"6.0","placeId":"FA0621D6035677ED3C9FE0228BF23C98","test":"1","utcTime":"2016-07-28 10:37:22","utcZone":"7","wifiIp":"10.0.16.180","wifiMac":"02:00:00:00:00:00","trackerType":"urlPing"}\n""".encode()

clients = 150
tasks = 100000
thread_pool = []
event_pool = []
task_queue = queue.Queue()

for n in range(tasks):
    task_queue.put(n)


def get_socket(ip_port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(ip_port)
    return s

def work_1_0(event):
    while not event.is_set():
        s = get_socket(ip_port)
        s.send(req)
        ret = s.recv(15).decode()
        status = int(ret.split()[1])
        if status == 200:
            task_queue.get()
        else:
            print('status={}'.format(status))
        s.close()
    print('.')

def work_1_1(event):
    '''Need to handle multi package arrive'''
    s = get_socket(ip_port)
    while not event.is_set():
        try:
            s.send(req)
        except Exception as e:
            s.close()
            s = get_socket(ip_port)
            s.send(req)
        ret = s.recv(8192).decode()
        if ret:
            try:
                status = int(ret.split()[1])
            except Exception as e:
                print(ret)
            if status == 200:
                tmp = task_queue.get()
            
    s.close()

for n in range(clients):
    event = threading.Event()
    t = threading.Thread(target=work_1_0,args=(event,))
    thread_pool.append(t)
    event_pool.append(event)


for t in thread_pool:
    t.setDaemon('daemonic')
    t.start()


while not task_queue.empty():
    old_size = task_queue.qsize()
    time.sleep(1)
    new_size = task_queue.qsize()
    processed_req = old_size - new_size
    print("{}r/s".format(processed_req))

for t in event_pool:
    t.set()
print("Test is over!")
