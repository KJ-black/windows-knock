import pydivert
import argparse
import subprocess
import os
import sys
import time
import re
import copy
from dataclasses import dataclass

# after python 3.7
@dataclass
class config_entry:
    name: str
    sequence: list
    seq_timeout: int
    command: str
    tcpflags: str

@dataclass
class candidate:
    name: str
    start: float
    end: float
    sequence: list
    command: str
    protocol: str

@dataclass
class interface:
    index: int
    name: str
                  
def get_parser():
    parser = argparse.ArgumentParser(description='Windows Port-knocking Server')
    
    parser.add_argument('-c', '--config', 
                        default='./knockd.conf',
                        help='use an alternate config file (default ./knockd.conf)',
                        type=str)
    parser.add_argument('-d', '--debug', 
                        action='store_true',
                        help='debug mode')
    parser.add_argument('-i', '--interface',
                        nargs='*',
                        type=int,
                        help='index of network interface to liston on (default all)')
    parser.add_argument('-l', '--list_interface',
                        action='store_true',
                        help='list all of the network interface')
    return parser

# global variable
interface_list = []
selected_interface = []
parser = get_parser()
args = parser.parse_args()
config = {}
all_port = dict()
match_queue = []

def get_interface():
    global selected_interface
    output = subprocess.getoutput("netsh int ipv4 show interfaces")
    lines = output.split('\n')
    for i, l in enumerate(lines):
        value = l.split()
        if not value: continue
        if i < 3: continue # get ride of useless info
        interface_list.append(interface(int(value[0]), ' '.join(value[4:])))
        
    # list interface
    if args.list_interface:
        print(f'\n=========== interface ===========')
        for i in interface_list:
            print(i)
        print(f'=================================\n')
        sys.exit()
    
    # selected interface
    if args.interface:
        selected_interface = args.interface
        for i in args.interface:
            for j in interface_list:
                if i == j.index:
                    break
            else:    
                sys.exit("[Error] Selected interface not existied!")
    else:
        for i in interface_list:
            selected_interface.append(i.index)
    if args.debug: print(f"Selected interface: {selected_interface}")
    
def read_config():
    if args.debug:  print(f"[+] config file: {args.config}")
    try:
        config_file = open(args.config, 'r')
    except:
        sys.exit("[Error] Wrong config file location!")
    name = ''
    for line in config_file.readlines():
        line = line.strip()
        if re.search('\[[a-zA-Z0-9 ]+\]', line):
            name = line.strip("[]")
            config[name] = {}
        elif line.strip() == '':
            continue
        elif name != '':
            pair = line.split('=', 1) # split at the first symbol of equal
            key = pair[0].strip()
            value = pair[1].strip()
            if key == "sequence":
                config[name][key] = [ int(s.strip()) for s in value.split(',')]
            else:
                config[name][key] = value
        
    if args.debug:
        for key in config:
            for p in config[key]['sequence']:
                all_port[p] = config[key]['protocol']
    
    if args.debug: 
        print(f'=========== config ===========')
        for i, (key, value) in enumerate(config.items()):
            for sub_key, sub_value in value.items():
                print(f"{i} [{key}]: {sub_key}: {sub_value}")
            print()
        print(f'==============================')
        print(f'All used port: {all_port}\n')
    return config           

def match_exec(q):
    if not q.sequence:
        os.system(q.command)
        if args.debug: print(f"[+] Execute: {q.command}")
        return True
    return False

def match_first(start, protocol, packet):
    for key, rule in config.items():
        if packet.dst_port == rule['sequence'][0] and protocol == rule['protocol']:
            tmp = candidate(key, start, start+int(rule['seq_timeout']), rule['sequence'][1:], rule['command'], rule['protocol'])
            if not match_exec(tmp):
                match_queue.append(tmp)
        
def match_seq(start, protocol, packet):
    remove_list = []
    for q in match_queue:
        if q.start == start: continue
        if q.end < start: 
            remove_list.append(q)
            continue
        if q.sequence[0] == packet.dst_port and protocol == q.protocol:
            q.sequence = q.sequence[1:]
            if match_exec(q):
                remove_list.append(q)
    
    for q in remove_list:
        match_queue.remove(q)
       
def port_knockd():
    w = pydivert.WinDivert()
    w.open()
    while(True):
        packet = w.recv()
        start = time.time()
        if "INBOUND" in str(packet.direction) and packet.interface[0] in selected_interface:
            
            # get protocol
            protocol = None
            if packet.tcp:
                protocol = 'tcp'
            else:
                protocol = 'udp'
            
            # debug message
            if args.debug:
                for key in all_port:
                    if packet.dst_port == key and protocol == all_port[key]:
                        print(f"{time.ctime(start)}: {protocol} {packet.src_addr}:{packet.src_port}->{packet.dst_addr}:{packet.dst_port}")
            
            # rule 
            match_first(start, protocol, packet)
            match_seq(start, protocol, packet)
        w.send(packet)
    w.close()
            
if __name__ == "__main__":
    get_interface()
    read_config()
    # TODO: hidden window
    # Start-Process -verb runAs "python" -WindowStyle hidden
    port_knockd()