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
import argparse
import httpx
import logging

class BareosHttpClient(httpx.Client):

    def auth(self, username, password):
        response = self.post("/token", data={"username": username, "password": password})
        # assert response.status_code == 200
        # assert response.json()['token_type'] == "bearer"
        #print(response.json())
        # assert 'access_token' in response.json()
        # client.headers = {"Authorization": "Bearer " + response.json()['access_token']}
        self.headers["Authorization"] = (
            response.json()["token_type"] + " " + response.json()["access_token"]
        )
        # return response.json()

    def walk(self, path, maxdepth=None):
        logger = logging.getLogger(__name__)

        if maxdepth is not None:
            if maxdepth <= 0:
                logger.debug(f"{path}: stop because maxdepth reached")
                return
            else:
                maxdepth -= 1

        response = self.get(path)
        logger.debug(response.json())

        try:
            for child_path, child_info in response.json()["children"].items():
                self.walk(child_path, maxdepth)
        except KeyError:
            pass


if __name__ == "__main__":

    def getArguments():
        epilog = """
        """

        argparser = argparse.ArgumentParser(description="Bareos HTTP client.", epilog=epilog)
        argparser.add_argument(
            "-d", "--debug", action="store_true", help="enable debugging output"
        )
        argparser.add_argument("URL", help="URL of the Bareos API server")
        argparser.add_argument(
            "username", help="Bareos user- or console-name"
        )
        argparser.add_argument("password", help="Password")
        args = argparser.parse_args()
        return args


    logging.basicConfig(
        format="%(levelname)s %(module)s.%(funcName)s: %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    args = getArguments()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    with BareosHttpClient(base_url=args.URL) as client:
        client.auth(args.username, args.password)
        client.base_url = str(client.base_url) + "node"
        client.walk("/", 1)
