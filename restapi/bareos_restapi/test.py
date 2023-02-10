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


from fastapi.testclient import TestClient

#from .main import app
from bareos_restapi import app

client = TestClient(app)


def DISABLED_test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

def auth():
    #curl --silent -X POST "${REST_API_URL}/token" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "username=admin-tls&password=secret" | grep access_token | cut -d 
    response = client.post("/token", data={'username': 'admin-tls', 'password': 'secret'})
    assert response.status_code == 200
    assert response.json()['token_type'] == "bearer"
    print(response.json())
    assert 'access_token' in response.json()
    return response.json()
    
def test_node():
    auth_response = auth()
    response = client.get("/node", headers={"Authorization": "Bearer " + auth_response['access_token']})
    assert response.status_code == 200
    assert response.json()['path'] ==  ''
    assert 'children' in response.json()

# node//.bareosfs-status.txt
