#!/usr/bin/python

import bareos.fuse
import fuse
import logging

LOG_FILENAME        = '/tmp/bareos-fuse-bsock.log'

if __name__ == '__main__':
    usage = """
    Bareos Fuse filesystem: displays files from Bareos backups as a (userspace) filesystem.

    """ + fuse.Fuse.fusage

    fs = bareos.fuse.BareosFuse(
        #version="%prog: " + BAREOS_FUSE_VERSION,
        usage = usage,
        # required to let "-s" set single-threaded execution
        dash_s_do = 'setsingle',
    )

    fs.parser.add_option(
        mountopt="address",
        metavar="BAREOS_DIRECTOR",
        default='localhost',
        help="address of the Bareos Director to connect [default: \"%default\"]")
    fs.parser.add_option(
        mountopt="port",
        metavar="PORT",
        default='9101',
        help="address of the Bareos Director to connect [default: \"%default\"]")
    fs.parser.add_option(
        mountopt="dirname",
        metavar="NAME",
        default='',
        help="name of the Bareos Director to connect [default: \"%default\"]")
    fs.parser.add_option(
        mountopt="name",
        metavar="NAME",
        help="name of the Bareos Named Console")
    fs.parser.add_option(
        mountopt="password",
        metavar="PASSWORD",
        default='',
        help="password to authenticate at Bareos Director [default: \"%default\"]")
    fs.parser.add_option(
        mountopt="logfile",
        metavar="FILENAME",
        default='',
        help="if given, log to FILENAME")

    fs.parse(values=fs, errex=1)

    fs.main()
