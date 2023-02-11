#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# BAREOS - Backup Archiving REcovery Open Sourced
#
# Copyright (C) 2023-2023 Bareos GmbH & Co. KG
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of version three of the GNU Affero General Public
# License as published by the Free Software Foundation, which is
# listed in the file LICENSE.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from __future__ import print_function
from bareos.httpclient import BareosHttpClient
import argparse
import logging


def getArguments():
    epilog = """
    """

    argparser = argparse.ArgumentParser(description="Bareos jobs.", epilog=epilog)
    argparser.add_argument(
        "-d", "--debug", action="store_true", help="enable debugging output"
    )
    argparser.add_argument("URL", help="URL of the Bareos API server")
    argparser.add_argument("username", help="Bareos user- or console-name")
    argparser.add_argument("password", help="Password")
    args = argparser.parse_args()
    return args


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s %(module)s.%(funcName)s: %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    args = getArguments()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("bareos.httpclient").setLevel(logging.DEBUG)

    with BareosHttpClient(base_url=args.URL) as client:
        client.auth(args.username, args.password)
        client.base_url = str(client.base_url) + "node"
        client.walk("/")
