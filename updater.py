#!/usr/bin/env python

import threading
import requests
from lxml import etree
import wx
import re


class UpdaterThread(threading.Thread):
    def __init__(self, current_version, parent):
        threading.Thread.__init__(self)
        self.current_version = current_version
        self.parent = parent

        self.daemon = True
        self.start()

    def run(self):
        req = requests.get('https://racingleaguecharts.com/version.xml', verify=False)
        if req.status_code == 200:
            tree = etree.fromstring(req.text)
            version = tree.find('version').text
            if self.version_compare(version, self.current_version):
                msg = "New version!\n\nThere is a new version (%s) of the app available for download!" % version
                dlg = wx.MessageDialog(self.parent, msg, 'Racing League Charts', wx.OK | wx.CANCEL | wx.ICON_WARNING)
                dlg.SetOKLabel('Download')
                if dlg.ShowModal() == wx.ID_OK:
                    r = requests.get('https://racingleaguecharts.com/racingleaguecharts.exe', stream=True, verify=False)
                    if r.status_code == 200:
                        filepath = "racingleaguecharts%s.exe" % version.replace('.', '')
                        with open(filepath, 'wb') as f:
                            total_length = int(r.headers.get('content-length'))
                            dialog = wx.ProgressDialog('Racing League Charts Updater',
                                                       'Downloading version %s to %s' % (version, filepath),
                                                       total_length,
                                                       style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
                            downloaded = 0
                            for chunk in r.iter_content(chunk_size=4096):
                                if chunk:
                                    downloaded += len(chunk)
                                    f.write(chunk)
                                    f.flush()
                                    dialog.Update(downloaded)

                        dialog.Destroy()
                dlg.Destroy()

    def version_compare(self, old_version, new_version):
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

        return cmp(normalize(old_version), normalize(new_version))