# windows-knock

It’s a simply port knocking server for windows which is implemented by python and [pydivert](https://github.com/ffalcinelli/pydivert). This project is based on https://github.com/jvinet/knock and rewritten from C to python to let it fit the windows environment.

### Install dependencies

```
pip instlall -r requirements.txt
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

The format is like above  and below detailed explain each arguments.

- `[whoami]` - Name of the knock action, also indicates the begin of one action block
- `sequence = <port_number>` - A sequence of port number which will trigger this action. The port number needs to be knocked at the given order.
- `seq_timeout = <sec>` - A timer to set the packet expiration time. In this example, the received time between the first packet which port is 4000 and the last packet which port is 4002 needs to be smaller than 5 seconds.
- `command = <command>` - What command you wish the action to take when successfully knocked. ( powershell command )
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