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
import httpx
import argparse
import logging

baseurl = "http://localhost:30588/"
username = "admin-tls"
password = "secret"


def getArguments():
    epilog = """
    """

    argparser = argparse.ArgumentParser(description="Bareos jobs.", epilog=epilog)
    argparser.add_argument(
        "-d", "--debug", action="store_true", help="enable debugging output"
    )
    argparser.add_argument("URL", help="URL of the Bareos API server", default=baseurl)
    argparser.add_argument(
        "username", help="Bareos user- or console-name", default=username
    )
    argparser.add_argument("password", help="Password", default=password)
    args = argparser.parse_args()
    return args


def auth(client, username, password):
    response = client.post("/token", data={"username": username, "password": password})
    # assert response.status_code == 200
    # assert response.json()['token_type'] == "bearer"
    print(response.json())
    # assert 'access_token' in response.json()
    # client.headers = {"Authorization": "Bearer " + response.json()['access_token']}
    client.headers["Authorization"] = (
        response.json()["token_type"] + " " + response.json()["access_token"]
    )
    # return response.json()


def walk(client, path):
    logger = logging.getLogger()
    response = client.get(path)
    logger.debug(response.json())
    try:
        for i in response.json()["children"]:
            if i not in [".", ".."]:
                walk(client, f"{path}/{i}")
    except KeyError:
        pass


# node//.bareosfs-status.txt


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s %(module)s.%(funcName)s: %(message)s", level=logging.INFO
    )
    logger = logging.getLogger()

    args = getArguments()
    print(args)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    with httpx.Client(base_url=baseurl) as client:
        auth(client, username, password)
        walk(client, "/node/")
