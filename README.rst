nwscan
=======

Python script to scan networks for alive hosts, uses CIDR notation.

Install
-------

Install using pip:

::

    pip install nwscan

Usage
-----

::

    Usage: nwscan network [options]

    scan networks for alive hosts, uses CIDR notation

    Options:
    --version       show program's version number and exit
    -h, --help      show this help message and exit
    -r, --reverse   print not responding hosts rather than alive
    -w WORKERS      number of workers threads to use (default: 8)
    -t TIMEOUT      timeout of each ping request in seconds (default: 1)
    -n COUNT        number of ping requests to send (default: 1)
    -i INPUT_FILE   scan networks from input file (one network per line)
    -o OUTPUT_FILE  save sorted ips output to file

Examples
--------

Scan all 254 usable IPs of network '192.168.0.*':

::

    $ nwscan 192.168.0.0/24

Scan networks from 'networks.txt' file using 16 workers:

::

    $ nwscan -i networks.txt -w 16

Scan not responding hosts and save ips to file 'ips.txt':

::

    $ nwscan 192.168.0.0/24 -r -o ips.txt

Notes
-----

- Works on Python 2
- Tested on Linux and Windows (Cygwin)
