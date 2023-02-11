"""
"""

from bareos.fuse.node.base import Base
from bareos.util import Path
from copy import deepcopy
import errno
import logging
from pprint import pformat
import stat


class Directory(Base):
    """
    Directory node.
    """

    def __init__(self, root, name):
        super(Directory, self).__init__(root, name)
        # self.defaultdirs = [".", ".."]
        self.defaultdirs = []
        self.stat.st_mode = stat.S_IFDIR | 0o755
        self.stat.st_nlink = len(self.defaultdirs)
        # arbitrary default value
        self.stat.st_size = 4096

    def readdir(self, path, offset):
        self.logger.debug('%s("%s")' % (str(self.name), str(path)))
        result = None
        # copy default dirs
        if path.len() == 0:
            self.update()
            result = list(self.defaultdirs) + list(self.subnodes.keys())
        else:
            if not (path.get(0) in self.subnodes):
                self.update()
            if path.get(0) in self.subnodes:
                topdir = path.shift()
                if callable(getattr(self.subnodes[topdir], "readdir", None)):
                    result = self.subnodes[topdir].readdir(path, offset)
        return result

    def get_stat(self):
        self.stat.st_nlink = len(self.defaultdirs) + self.subnode_count
        return super(Directory, self).get_stat()

    # Node methods
    # ============

    def get_node(self, path: Path):
        self.logger.debug('%s.get_node("%s")' % (str(self.name), str(path)))
        result = None
        if path.len() == 0:
            self.logger.debug("path.len == 0")
            return self
        else:
            if not (path.get(0) in self.subnodes):
                self.update()
            if path.get(0) in self.subnodes:
                subpath = deepcopy(path)
                topdir = subpath.shift()
                result = self.subnodes[topdir].get_node(subpath)
        self.logger.debug("result = " + str(result))
        return result
