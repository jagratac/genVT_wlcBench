#!/usr/bin/env python3
# consolecallback - provide a persistent console that survives guest reboots

import os
import time
import sys
import logging
import libvirt
import tty
import termios
import atexit
import libvirt_ipaddress as guest_ip
import genvt_ssh as ssh
from argparse import ArgumentParser
from typing import Optional  # noqa F401

login_data = []
un_data = []
def reset_term() -> None:
    termios.tcsetattr(0, termios.TCSADRAIN, attrs)


def error_handler(unused, error) -> None:
    # The console stream errors on VM shutdown; we don't care
    if error[0] == libvirt.VIR_ERR_RPC and error[1] == libvirt.VIR_FROM_STREAMS:
        return
    logging.warn(error)


class Console(object):
    def __init__(self, uri: str, name: str, *args) -> None:
        self.uri = uri
        self.name = name
        self.connection = libvirt.open(uri)
        self.domain = self.connection.lookupByName(name)
        self.state = self.domain.state(0)
        self.connection.domainEventRegister(lifecycle_callback, self)
        self.stream = None  # type: Optional[libvirt.virStream]
        self.run_console = True
        self.stdin_watch = -1
        self.args = args
        logging.info("%s initial state %d, reason %d",
                     self.name, self.state[0], self.state[1])



def check_console(console: Console) -> bool:
    if (console.state[0] == libvirt.VIR_DOMAIN_RUNNING or console.state[0] == libvirt.VIR_DOMAIN_PAUSED):
        if console.stream is None:
            console.stream = console.connection.newStream(libvirt.VIR_STREAM_NONBLOCK)
            console.domain.openConsole(None, console.stream, 0)
            console.stream.eventAddCallback(libvirt.VIR_STREAM_EVENT_READABLE, stream_callback, console)
    else:
        if console.stream:
            console.stream.eventRemoveCallback()
            console.stream = None

    return console.run_console



# most hardcoded part of code need to make it generalize 
def stdin_callback(watch: int, fd: int, events: int, console: Console) -> None:
    readbuf = os.read(fd, 1024)
    if readbuf.startswith(b"+"):
        console.run_console = False
        return

    if console.stream:
        console.stream.send(readbuf)


def stream_callback(stream: libvirt.virStream, events: int, console: Console) -> None:
    try:
        assert console.stream
        received_data = console.stream.recv(1024)
    except Exception:
        return
    os.write(0, received_data)
    try:
        login_data.append(received_data.decode('utf-8'))
    except UnicodeDecodeError:
        print(" ")

    char_data = ''.join(login_data)
    vm_name = console.name
    if stream_callback.login_flag == 1:
        for login_str in char_data.rsplit():
            if login_str == 'login:' and stream_callback.login_flag == 1:
                console.stream.send(b"wlc\n")
                login_data.clear()
                stream_callback.login_flag = 2
    if stream_callback.cmd_flag == 1:
        for login_str in char_data.rsplit():
            if login_str == 'wlc@wlc-ubuntu:~$' and stream_callback.cmd_flag == 1:
                console.stream.send(b"echo wlc123 | sudo -S mount -t 9p -o trans=virtio,version=9p2000.L mytag /mnt\n")
                console.stream.send(b"sudo rm -r synbench \n")
                ipaddress = guest_ip.Guest_IPAddress(console.domain)
                init_cmd = console.args[0][0]['init_cmd']
                try:
                    f = open("ipaddress.txt", mode = 'w',encoding = 'utf-8')
                    f.write(f"{vm_name}:={ipaddress} \n")
                        # perform file operations
                finally:
                    f.close()
                os.system(f"{init_cmd}")
#                os.system(f"python3 libvirt_ipaddress_test.py GenVT.yml")
                #console.stream.send(b"sudo [ ! -d '/home/wlc/test' ] && mkdir test && cd test\n")
                #console.stream.send(b"sudo cp /mnt/Gen_VT.sh .\n")
#                console.stream.send(b"cd test\n")
#                console.stream.send(b"./Gen_VT.sh")
#                console.stream.send(vm_name.encode())
#                console.stream.send(b"\n")
                login_data.clear()
                stream_callback.cmd_flag = 2



def lifecycle_callback(connection: libvirt.virConnect, domain: libvirt.virDomain, event: int, detail: int, console: Console) -> None:
    console.state = console.domain.state(0)
    logging.info("%s transitioned to state %d, reason %d",
                 console.uuid, console.state[0], console.state[1])

# main

print("Escape character is ^]")

libvirt.virEventRegisterDefaultImpl()
libvirt.registerErrorHandler(error_handler, None)

atexit.register(reset_term)
attrs = termios.tcgetattr(0)
tty.setraw(0)
stream_callback.login_flag = 1
stream_callback.cmd_flag = 1

