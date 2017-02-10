#!/usr/bin/python

# nwscan 0.1
# author: Pedro Buteri Gonring
# email: pedro@bigode.net
# date: 10/02/2017

import subprocess
import sys
import optparse
from multiprocessing.pool import ThreadPool
import ipaddr
from socket import inet_aton


version = '0.1'


# Parse and validate arguments
def get_parsed_args():
    usage = 'usage: %prog network [options]'
    # Create the parser
    parser = optparse.OptionParser(
        description='scan network for alive hosts, uses CIDR notation',
        usage=usage, version=version
    )
    parser.add_option(
        '-r', '--reverse', action='store_true', default=False,
        help='print not responding hosts rather than alive'
    )
    parser.add_option(
        '-w', dest='workers', default=8, type=int,
        help='number of workers threads to use (default: %default)'
    )
    parser.add_option(
        '-t', dest='timeout', default=1, type=int,
        help='timeout of each ping request in seconds (default: %default)'
    )
    parser.add_option(
        '-n', dest='count', default=1, type=int,
        help='number of ping requests to send (default: %default)'
    )
    parser.add_option(
        '-i', dest='input_file',
        help='scan networks from input file (one network per line)'
    )
    parser.add_option(
        '-o', dest='output_file',
        help='save sorted ips output to file'
    )
    # Print help if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # Parse the args
    (options, args) = parser.parse_args()

    # Some args validation
    if len(args) == 0 and options.input_file is None:
        parser.error('network or file not informed')
    if len(args) == 1 and options.input_file is not None:
        parser.error('network and file provided, only one needed')
    if len(args) > 1:
        parser.error('incorrect number of arguments')
    if options.timeout < 1:
        parser.error('timeout must be a positive number')
    if options.count < 1:
        parser.error('count must be a positive number')
    return (options, args)


# Check if host is alive
def is_alive(ip, count, timeout):
    # Check platform to run the correct ping args
    if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        # Run the ping command from OS, in this case Windows
        ret = subprocess.call(
            ['ping', '-n', str(count), '-w', str(timeout * 1000), ip],
            stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w')
        )
    else:
        ret = subprocess.call(
            ['ping', '-c', str(count), '-i', '0.2', '-W', str(timeout), ip],
            stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w')
        )

    # Check the return of the ping command above
    if ret == 0:
        return True
    else:
        return False


# Worker function
def work_work(ip):
    alive = is_alive(ip, options.count, options.timeout)
    if not options.reverse and alive:
        sys.stdout.write('%s is alive\n' % ip)
        output_list.append(ip)
    if options.reverse and not alive:
        sys.stdout.write('%s is not responding\n' % ip)
        output_list.append(ip)


# Main CLI
def cli():
    global options
    global output_list
    output_list = []
    ips = []

    (options, args) = get_parsed_args()

    # Generate ips from file
    if options.input_file is not None:
        try:
            with open(options.input_file, 'r') as f:
                lines = f.read().splitlines()
        except Exception as ex:
            print ex
            sys.exit(1)
        for item in lines:
            if '/' not in item:
                print '\nerror: %s does not appear to be in CIDR format' % item
                sys.exit(1)
            try:
                network = ipaddr.IPv4Network(item)
            except (ipaddr.AddressValueError, ipaddr.NetmaskValueError):
                print '\nerror: %s is not a valid network' % item
                sys.exit(1)
            network_ips = [str(ip) for ip in network.iterhosts()]
            ips += network_ips
    # Get network from command line
    else:
        if '/' not in args[0]:
            print '\nerror: %s does not appear to be in CIDR format' % args[0]
            sys.exit(1)
        try:
            network = ipaddr.IPv4Network(args[0])
        except (ipaddr.AddressValueError, ipaddr.NetmaskValueError):
            print '\nerror: %s is not a valid network' % args[0]
            sys.exit(1)
        ips = [str(ip) for ip in network.iterhosts()]

    print 'Scanning %d hosts...\n' % len(ips)

    # Create thread pool of workers
    pool = ThreadPool(processes=options.workers)
    try:
        # .get(2592000) will set the pool timeout to one month
        # This is a 'fix' to successfull catch keyboard interrupt
        pool.map_async(work_work, ips).get(2592000)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print 'Aborting.'
        sys.exit(1)

    # Save ips to file if needed
    if options.output_file is not None:
        try:
            with open(options.output_file, 'w') as f:
                # Uses inet_aton to convert IP to binary format
                # So the sort works as expected
                output_list.sort(key=lambda ip: inet_aton(ip))
                for ip in output_list:
                    f.write('%s\n' % ip)
        except Exception as ex:
            print ex
            sys.exit(1)

    print '\nFinished: %d hosts scanned' % len(ips)
    if options.reverse:
        print 'Not responding hosts: %d' % len(output_list)
    else:
        print 'Alive hosts: %d' % len(output_list)

    if options.output_file is not None:
        print "\nIPs list saved to '%s'" % options.output_file


# Run cli function if invoked from shell
if __name__ == '__main__':
    cli()
