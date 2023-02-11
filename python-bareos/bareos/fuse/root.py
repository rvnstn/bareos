"""
bareosfs root node (top level directory)
"""

from copy import copy

import bareos.fuse.exceptions
from bareos.fuse.nodefactory import NodeFactory
from bareos.fuse.node.directory import Directory
from bareos.fuse.node import *
from bareos.util import Path


class Root(Directory):
    """
    Define filesystem structure of root (/) directory.
    """

    def __init__(self, bsock, restoreclient, restorejob, restorepath):
        self.bsock = bsock
        self.restoreclient = restoreclient
        if restoreclient:
            data = self.bsock.call(".clients")
            if not restoreclient in [item["name"] for item in data["clients"]]:
                raise bareos.fuse.RestoreClientUnknown(restoreclient)
        self.restorejob = restorejob
        if restorejob:
            data = self.bsock.call(".jobs")
            if not restorejob in [item["name"] for item in data["jobs"]]:
                raise bareos.fuse.RestoreJobUnknown(restorejob)
        self.restorepath = restorepath
        super(Root, self).__init__(self, None)
        self.factory = NodeFactory(self)
        self.add_subnode(Jobs, "jobs")
        self.add_subnode(VolumeList, "volumes")
        self.add_subnode(Pools, "pools")
        self.add_subnode(Clients, "clients")
        self.add_subnode(Status, ".bareosfs-status.txt")

    # Node methods
    # ============

    # def get_children(self, path : str, offset = None):
    #     relative_children = self.readdir(Path(path), offset)
    #     if relative_children is None:
    #         return {}
    #     children = [ str(Path(f"{path}/{i}")) for i in relative_children ]
    #     return children

    def get_children(self, path: str, offset=None):
        relative_child_paths = self.readdir(Path(path), offset)
        if relative_child_paths is None:
            return {}
        result = {}
        for i in relative_child_paths:
            self.logger.debug(f"rel_path: {i}")
            child_fullpath = Path(f"{path}/{i}")
            self.logger.debug(f"full_path: {child_fullpath}")
            tmp = copy(child_fullpath)
            node = self.get_node(tmp)
            if node:
                result[str(child_fullpath)] = {
                    "name": node.get_name(),
                    #'id': node.id,
                    #'path': child_path,
                }
        return result
