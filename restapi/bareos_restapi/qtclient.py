#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import signal
import sys

from PySide2.QtCore import QDir, QFile, Qt, QTimer
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QDockWidget,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QStyle,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from bareos.httpclient import BareosHttpClient


class MainWindow(QMainWindow):
    def __init__(self, client, parent=None):
        super().__init__(parent)

        self.name = "Bareos Admin Client"

        self.tree = BareosNodesTree(self, client)
        self.setCentralWidget(self.tree)

        self.create_actions()
        self.create_menus()
        self.createDockWidgets()

        self.statusBar().showMessage("Ready")

        self.setWindowTitle(self.name)

        self.resize(640, 480)

    def about(self):
        QMessageBox.about(
            self,
            f"About {self.name}",
            f"The <b>{self.name}</b> demonstrates the usage of the Bareos REST-API",
        )

    def create_actions(self):
        self._exit_act = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)

        self._about_act = QAction("&About", self, triggered=self.about)

        self._about_qt_act = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("&File")
        self._file_menu.addAction(self._exit_act)

        self.menuBar().addSeparator()

        self._help_menu = self.menuBar().addMenu("&Help")
        self._help_menu.addAction(self._about_act)
        self._help_menu.addAction(self._about_qt_act)

    def createDockWidgets(self):
        dockWidget = QDockWidget("Content", self)
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.contentWidget = QTextEdit()
        self.contentWidget.setLineWrapMode(QTextEdit.NoWrap)
        self.contentWidget.setReadOnly(True)
        # self.contentWidget.setPlainText("")
        # PySide2.QtWidgets.QTextEdit.clear()
        dockWidget.setWidget(self.contentWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

    def timer(self):
        pass


class BTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, name, path, real=True):
        super().__init__([name, path])
        self.bareos = {
            "name": name,
            "path": path,
            "real": real,
        }

    def name(self):
        return self.bareos["name"]

    def path(self):
        return self.bareos["path"]


class BareosNodesTree(QTreeWidget):
    def __init__(self, parent, client):
        super().__init__(parent)
        self.parent = parent
        self.client = client

        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.setHeaderLabels(("Title", "Location"))

        self._folder_icon = QIcon()
        self._bookmark_icon = QIcon()

        self._folder_icon.addPixmap(
            self.style().standardPixmap(QStyle.SP_DirClosedIcon),
            QIcon.Normal,
            QIcon.Off,
        )
        self._folder_icon.addPixmap(
            self.style().standardPixmap(QStyle.SP_DirOpenIcon), QIcon.Normal, QIcon.On
        )
        self._bookmark_icon.addPixmap(self.style().standardPixmap(QStyle.SP_FileIcon))

        self.itemExpanded.connect(self.slotItemExpanded)
        self.itemActivated.connect(self.slotItemActivated)

        self.root = BTreeWidgetItem("root", "/")
        self.addTopLevelItem(self.root)
        self.root.setExpanded(True)

    def removeChilds(self, item):
        numberOldItems = item.childCount()
        for i in range(numberOldItems, 0, -1):
            item.removeChild(item.child(i - 1))

    def addChilds(self, item):
        response = client.get(item.path())
        print(response.json())

        if len(response.json()["children"]) == 0:
            child = BTreeWidgetItem("empty", None, False)
            item.addChild(child)
        else:
            for child_path, child_info in response.json()["children"].items():
                child = BTreeWidgetItem(child_info["name"], child_path)
                item.addChild(child)
                if child_info["directory"]:
                    expanditem = BTreeWidgetItem("expanding", "...", False)
                    child.addChild(expanditem)

    def updateChilds(self, item):
        self.removeChilds(item)
        self.addChilds(item)

    def slotItemExpanded(self, item):
        self.updateChilds(item)

    def updateItem(self, item):
        response = client.get(item.path())
        print(response.json())
        if "content" in response.json():
            self.parent.contentWidget.setDocumentTitle(response.json()["path"])
            self.parent.contentWidget.setPlainText(response.json()["content"])

    def slotItemActivated(self, item, column):
        self.updateItem(item)


def sigint_handler(*args):
    """
    Handler for the SIGINT signal.
    Only called outside QT main loop, eg. QTimer
    """
    sys.stderr.write("\r")
    QApplication.quit()


def process_commandline_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-d", "--debug", action="store_true")
    argparser.add_argument("URL", help="URL of the Bareos API server")
    argparser.add_argument("username", help="Bareos user- or console-name")
    argparser.add_argument("password", help="Password")
    parsed_args, unparsed_args = argparser.parse_known_args()
    return parsed_args, unparsed_args


if __name__ == "__main__":
    URL = "http://localhost:30588/"
    username = "admin-tls"
    password = "secret"
    username = "admin"
    password = "linuxlinux"

    signal.signal(signal.SIGINT, sigint_handler)

    args, unparsed_args = process_commandline_args()
    qt_args = sys.argv[:1] + unparsed_args

    app = QApplication(qt_args)
    # with BareosHttpClient(base_url=URL) as client:
    #     client.auth(username, password)
    #     client.base_url = str(client.base_url) + "node"
    #     #client.walk("/")
    #     main_win = MainWindow(client)
    #     main_win.show()
    #     #main_win.open()
    client = BareosHttpClient(base_url=args.URL)
    client.auth(args.username, args.password)
    client.base_url = str(client.base_url) + "node"
    main_win = MainWindow(client)
    main_win.show()
    timer = QTimer(app)
    timer.timeout.connect(main_win.timer)
    timer.start(1000)
    sys.exit(app.exec_())
