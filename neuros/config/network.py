#!/usr/bin/env python

import configobj

# Fields used below. These may be moved to configobj proper

class IPv4Addr(configobj.Field):
    """Validates an IPv4 address, discarding CIDR suffix if present.

    >>> class C(configobj.ConfigObj):
    ...     addr = IPv4Addr()
    ...
    >>> c = C()
    >>> print c.addr
    None
    >>> c.addr = None
    Traceback (most recent call last):
        ...
    ValueError: C.addr <class '...IPv4Addr'> cannot be null.
    >>> c.addr = '192.168.0.1'
    >>> print c.addr
    192.168.0.1
    >>> c.addr = '127.0.0.1/0'
    >>> print c.addr
    127.0.0.1
    >>> c.addr = 4
    Traceback (most recent call last):
        ...
    ValueError: Only dotted-decimal IPv4 addresses supported.
    >>> c.addr = '123.456.78.9'
    Traceback (most recent call last):
        ...
    ValueError: 123.456.78.9 is not a valid IPv4 address.
    """

    def validate(self, value):
        value = super(IPv4Addr, self).validate(value)
        if value is None or value is '': return value

        if not isinstance(value, str):
            # For now, we don't support integer addresses to avoid confusion
            raise ValueError('Only dotted-decimal IPv4 addresses supported.')

        if value.find('/') >= 0:
            value = value.split('/')[0]

        parts = value.split('.')
        if len(parts) != 4:
            raise ValueError('%s is not a valid IPv4 address.' % value)
        
        for part in parts:
            try:
                v = int(part)
            except ValueError:
                raise ValueError('%s is not a valid IPv4 address.' % value)
            if v < 0 or v > 255:
                raise ValueError('%s is not a valid IPv4 address.' % value)
        return value

class IPv4Netmask(IPv4Addr):
    """Validates an IPv4 netmask. Doesn't really do anything in particular at
    this point to differentiate itself from IPv4Addr, but it will."""

    def validate(self, value):
        value = super(IPv4Netmask, self).validate(value)



# The actual ConfigObjs, which do the validating of IO as well as other stuff

class IPv4Config(configobj.ConfigObj):
    address = IPv4Addr()
    netmask = IPv4Netmask(default = '255.255.255.0')
    broadcast = IPv4Addr()
    gw = IPv4Addr(null = True)
    
class Inteface(configobj.ConfigObj):
    pass

class ENIParser:
    """Parser and writer for /etc/network/interfaces. It's not elegant, but
    it's done, and that counts for a whole lot more.
    
    TODO: tests and validators.
    TODO: don't clobber comments if we can avoid it.
    TODO: deal with interfaces we don't care about so much.
    TODO: persistence and consistency checking.
    """

    def __init__(self, file = '/etc/network/interfaces'):
        self.file = file
        self.mtime = os.path.getmtime(file)

    
    def _parse(self):
        f = open(self.file, 'r')
        
        for line in f.readlines():
            pass    
        


        


        


class IPv4Config(configobj.ConfigObj):
    pass
    

class Interface(configobj.ConfigObj):
    """Controls network interfaces, including IP configuration and link
    status."""
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags = doctest.ELLIPSIS)

