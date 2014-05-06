#!/usr/bin/env python

import threading
import requests
from lxml import etree
from wx import MessageBox

class UpdaterThread(threading.Thread):
    def __init__(self, current_version):
        threading.Thread.__init__(self)
        self.current_version = current_version

        self.daemon = True
        self.start()

    def run(self):
        req = requests.get('https://racingleaguecharts.com/version.xml', verify=False)
        if req.status_code == 200:
            tree = etree.fromstring(req.text)
            version = tree.find('version').text
            if version != self.current_version:
                link = "https://racingleaguecharts.com/racingleaguecharts.exe"
                MessageBox("New version!\n\nThere is a new version (%s) of the app available for download:\n\n%s" % (version, link))
