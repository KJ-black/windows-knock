# windows-knock

It’s a simple port knocking server for windows which is implemented by python and [pydivert](https://github.com/ffalcinelli/pydivert). This project is based on [jvinet/knock](https://github.com/jvinet/knock) and rewritten to let it fit the windows environment.

Details about the port-knocking mechanism can refer to my [article](https://www.notion.so/Port-Knocking-acf3e7bd78bf46268cda1977214ef8e0).

### Environment

- Windows 10 Professional 10.0.19044
- Python version 3.7
- Needs to be executed with Administrator privilege

### Install dependencies

```
pip install -r requirements.txt
```

## Usage

### Configure knockd.conf

```
[open udp port 8888]
	sequence 	= 5000, 5001
	seq_timeout = 10
	command 	= netsh advfirewall firewall add rule name="open udp port 8888" protocol=UDP dir=out localport=8888 remoteip=%IP% action=allow
	protocol	= udp
```

The format is like the above and the below detailed explains each argument.

- `[open udp port 8888]` - The name of the knock action, also indicates the beginning of one action block
- `sequence = <port_number>` - A sequence of port numbers that will trigger this action. The port number needs to be knocked at the given order.
- `seq_timeout = <sec>` - A timer to set the packet expiration time. In this example, the received time between the first packet which port is 4000, and the last packet which port is 4002 needs to be smaller than 5 seconds.
- `command = <command>` - What command do you wish the action to take when successfully knocked. ( Powershell command )
    - `%IP%` is a specific variable which will  depends on the source IP.
- `protocol = tcp` - Indicate what protocol the packet used, tcp or udp. ( Case sensitive )

### Run Server

```
usage: knockd.py [-h] [-c CONFIG] [-d] [-i [INTERFACE [INTERFACE ...]]] [-l]

Windows Port-knocking Server

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        use an alternate config file (default ./knockd.conf)
  -d, --debug           debug mode
  -i [INTERFACE [INTERFACE ...]], --interface [INTERFACE [INTERFACE ...]]
                        index of network interface to liston on (default all)
  -l, --list_interface  list all of the network interface
```

### Client

There are lots of ready-made port-knocking clients.

- Linux
    - [jvinet/knock](https://github.com/jvinet/knock) needs to compile the client ourselves
    - We can directly use Natcat to send the packets which can let us use different TCP flags to send the packet.
        
        E.g., `sudo nmap -sF -r 140.113.194.76 -p4000-4002`
        
        ※ Nmap randomizes the port scan order by default to make detection slightly harder. The `-r` option causes them to be scanned in numerical order instead.
        
- Windows
    - [grongor/knock](https://github.com/grongor/knock) is a python written client which can use both in linux and windows and it can set the timeout parameter.
    - [Windows port knock application with gregsowell](https://gregsowell.com/?p=2020) is a well-compiled executable file with a GUI interface. It’s friendly for windows users.

## TODO

- [ ]  different protocol and difference flag. Now only tcp and udp takes effect.
- [ ]  timeout mechanism to close the firewall
- [ ]  cryptographic hashes to defends against packet sniffing and replay attacks.
- [ ]  dynamic length and pool of length to increase its security
- [ ]  dynamic attack response