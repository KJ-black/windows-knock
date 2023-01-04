# windows-knock

It’s a simple port knocking server for windows which is implemented by python and [pydivert](https://github.com/ffalcinelli/pydivert). This project is based on [jvinet/knock](https://github.com/jvinet/knock) and rewritten to let it fit the windows environment.

### Install dependencies

```
pip install -r requirements.txt
```

## Usage

### Configure knockd.conf

```
[whoami]
	sequence	= 4000, 4001, 4002
	seq_timeout	= 5
	command		= whoami
	protocol	= tcp
```

The format is like the above and the below detailed explains each argument.

- `[whoami]` - The name of the knock action, also indicates the beginning of one action block
- `sequence = <port_number>` - A sequence of port numbers that will trigger this action. The port number needs to be knocked at the given order.
- `seq_timeout = <sec>` - A timer to set the packet expiration time. In this example, the received time between the first packet which port is 4000, and the last packet which port is 4002 needs to be smaller than 5 seconds.
- `command = <command>` - What command do you wish the action to take when successfully knocked. ( Powershell command )
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
- Windows
    - [grongor/knock](https://github.com/grongor/knock) is a python written client which can use both in linux and windows and it can set the timeout parameter.
    - [Windows port knock application with gregsowell](https://gregsowell.com/?p=2020) is a well-compiled executable file with a GUI interface. It’s friendly for windows users.