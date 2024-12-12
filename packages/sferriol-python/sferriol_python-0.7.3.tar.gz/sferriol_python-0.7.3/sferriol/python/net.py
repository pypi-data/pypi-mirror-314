# -*- coding: utf-8 -*-
#
#  Copyright 2023 sferriol <s.ferriol@ip2i.in2p3.fr>
"""Network utilities"""
import fcntl
import socket
import struct


def are_in_same_network(ip_addr1: str, ip_addr2: str,
                        netmask_addr: str) -> bool:
    """Returns True if two addresses are in the same network specified by its netmask

    Examples:
    >>> are_in_same_network('1.2.3.4', '1.2.3.5', '255.255.255.0')
    True
    """
    a1 = socket.inet_aton(ip_addr1)
    a2 = socket.inet_aton(ip_addr2)
    n = socket.inet_aton(netmask_addr)
    return all([a1[i] & n[i] == a2[i] & n[i] for i in range(4)])


def get_interface_ip_address(if_str: str) -> str:
    """Returns the ip address of the interface

    Args:
      if_str name of the interface or ip address of its network

    Examples:
    >>> get_interface_ip_address('lo')
    '127.0.0.1'
    """
    if_name = get_interface_name(if_str) if is_ipv4_address(if_str) else if_str
    if if_name in list_interfaces():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            return socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915,
                            struct.pack('256s', bytes(if_name[:15],
                                                      'utf-8')))[20:24])
        except OSError:
            pass

def get_interface_name(ip_addr: str) -> str:
    """Returns the interface name

    Args:
    ip_addr ip address of interface network

    Examples:
    >>> get_interface_name('127.0.0.1')
    'lo'
    """
    interfaces = list_interfaces()
    ret = None
    for if_name in interfaces:
        try:
            if_addr = get_interface_ip_address(if_name)
            netmask_addr = get_netmask_address(if_name)
        except OSError:
            continue
        else:
            if are_in_same_network(ip_addr, if_addr, netmask_addr):
                ret = if_name
                break
    return ret


def get_netmask_address(if_name: str) -> str:
    """Returns the netmask of an interface

    Examples:
    >>> get_netmask_address('lo')
    '255.0.0.0'
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(s.fileno(), 0x891b,
                    struct.pack('256s', bytes(if_name[:15], 'utf-8')))[20:24])


def is_interface_connected(if_name: str) -> bool:
    """Returns if interface has a carrier up status

    Examples:
    >>> is_interface_connected('lo')
    True
    """
    file = f'/sys/class/net/{if_name}/carrier'
    with open(file) as f:
        return int(f.read().strip()) == 1


def is_ipv4_address(ip_addr: str) -> bool:
    """Returns if the addr has en IPV4 format

    Examples:
    >>> is_ipv4_address('1.2.3.4')
    True
    >>> is_ipv4_address('toto')
    False
    
    """
    nbrs = ip_addr.strip().split('.')
    return len(nbrs) == 4 and all([n.isdigit() for n in nbrs])


def is_port_in_use(port: int) -> bool:
    """Test if the port is already used"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def list_interfaces() -> tuple[str, ...]:
    """Returns all network interfaces available"""
    return (k[1] for k in socket.if_nameindex())


def unused_port() -> int:
    """Return an unsued port

    Returns:
      Port value
    """
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    _, port = sock.getsockname()
    sock.close()
    return port
