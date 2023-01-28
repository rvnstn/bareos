#!/usr/bin/python

# -*- coding: utf-8 -*-

import bareos.fuse
import fuse
import logging
import sys

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
        metavar="BAREOS_DIRECTOR_NAME",
        default='',
        help="name of the Bareos Director to connect [default: \"%default\"]")
    fs.parser.add_option(
        mountopt="name",
        metavar="BAREOS_CONSOLE_NAME",
        help="name of the Bareos Named Console. If not given, it tries to use the Bareos Default Console")
    fs.parser.add_option(
        mountopt="password",
        metavar="PASSWORD",
        default='',
        help="password of the Bareos Console to authenticate at the Bareos Director")
    fs.parser.add_option(
        mountopt="restoreclient",
        metavar="BAREOS_CLIENT_NAME",
        default='',
        help="Bareos client used to restore files")
    fs.parser.add_option(
        mountopt="restorejob",
        metavar="BAREOS_JOB_NAME",
        default='',
        help="Bareos job used to restore files")
    fs.parser.add_option(
        mountopt="restorepath",
        metavar="PATH",
        default=fs.restorepath,
        help="path prefix to restore files [default: \"%default\"]")
    fs.parser.add_option(
        mountopt="logfile",
        metavar="FILENAME",
        default='',
        help="if given, log to FILENAME")

    try:
        fs.parse(values=fs, errex=1)
    except (bareos.fuse.exceptions.ParameterMissing,
            bareos.fuse.exceptions.RestorePathInvalid) as e:
        print(e.__module__ + "." + e.__class__.__name__+ ": " + str(e))
        sys.exit(1)

    try:
        fs.main()
    except (bareos.fuse.SocketConnectionRefused,
        bareos.exceptions.AuthenticationError,
        bareos.fuse.exceptions.RestoreClientUnknown,
        fuse.FuseError) as e:
            print(e.__module__ + "." + e.__class__.__name__+ ": " + str(e))
            sys.exit(1)
