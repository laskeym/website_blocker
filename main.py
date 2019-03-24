#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Website Blocker
"""

import re
import os
import threading

import wx
import validators

from http.server import HTTPServer
from server import Server
from socketserver import ThreadingMixIn

HOST = '127.0.0.1'
PORT = 8000

hosts_path = '/etc/hosts'
redirect = '127.0.0.1'


class ServerThread(threading.Thread):
    def __init__(self, host, port, serverObj):
        super(ServerThread, self).__init__(target=self.run, name='ServerThread')

        self.httpd = HTTPServer((host, port), serverObj)
        self.daemon = True
        self.server_run = True
        self.start()

    def run(self):
        while self.server_run:
            self.httpd.handle_request()


def url_extractor(url):
    """
    Function that will extract domain name out of URL.  

    URL is validated at this point.
    """

    regex = 'https://(.*)'
    if 'www.' in url:
        regex = 'www.(.*)'

    
    try:
        extracted_url = re.compile(regex).search(url).group(1)
        
        return extracted_url
    except AttributeError as err:
        return url

def grant():
    """
    Grant permissions to hosts file
    """
    os.system('sh /home/mark/Programming/Python/Projects/wxpython/grant.sh')


def revoke():
    """
    Revoke permissions to hosts file
    """
    os.system('sh /home/mark/Programming/Python/Projects/wxpython/revoke.sh')


class Example(wx.Frame):
    """
    Main GUI frame
    """

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)

        self.blocked_sites = []
        self.loadBlockedSites()

        self.InitUI()
        self.Centre()

    def InitUI(self):

        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Website URL')
        st1.SetFont(font)
        hbox1.Add(st1)

        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc = wx.TextCtrl(panel)
        btnAdd = wx.Button(panel, id=1, label='Add', size=(70, 30))

        btnAdd.Bind(wx.EVT_BUTTON, self.btnAdd)

        hbox2.Add(self.tc, flag=wx.LEFT, proportion=1)
        hbox2.Add(btnAdd, flag=wx.LEFT, border=10)

        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.lb = wx.ListBox(panel, size=(100, -1), choices=self.blocked_sites, style=wx.LB_SINGLE)

        self.lb.Bind(wx.EVT_LISTBOX, self.checkSelection)

        self.btnDel = wx.Button(panel, label='Remove', size=(70, 30))
        self.btnDel.Disable()

        self.btnDel.Bind(wx.EVT_BUTTON, self.btnDelClick)

        hbox3.Add(self.lb, proportion=1, flag=wx.EXPAND|wx.TOP, border=10)
        hbox3.Add(self.btnDel, flag=wx.LEFT|wx.TOP, border=10)

        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def loadBlockedSites(self):
        """
        Load all current blocked sites from the hosts file
        """
        write_lines = False
        site_list = set()

        grant()
        with open(hosts_path, 'r+') as f:
            content = f.readlines()
            f.seek(0)
            for line in content:
                if line.strip() == '# Website Blocker':
                    write_lines = True
                    continue
                if write_lines:
                    if '.com' in line[10:].strip():
                        site_list.add(url_extractor(line[10:].strip()))
        self.blocked_sites.extend(sorted(site_list))
        revoke()

    def btnAdd(self, e):
        """
        Add blocked site
        """
        txt = self.tc.GetValue().strip()

        error = None
        if txt == '':
            error = wx.MessageDialog(None, 'Field cannot be blank!', 'Error', wx.OK | wx.ICON_WARNING)
        if not validators.url(txt):
            error = wx.MessageDialog(None, 'Not a valid URL!', 'Error', wx.OK | wx.ICON_WARNING)

        if error:
          error.ShowModal()
          return

        url = url_extractor(txt) # Extract domain

        self.blocked_sites.append(url)
        write_to_hosts(url)
        self.tc.SetValue('')
        self.lb.Set(sorted(self.blocked_sites))

    def checkSelection(self, e):
        """
        Check if ListBox has a selection 
        """
        if not e.IsSelection():
            self.btnDel.Disable()
        else:
            self.btnDel.Enable()

    def btnDelClick(self, e):
        """
        Delete blocked site
        """
        url = self.lb.GetString(self.lb.GetSelection())

        self.blocked_sites.remove(url)
        remove_from_hosts(url)
        self.lb.Set(self.blocked_sites) # Need to tweak this a bit


def write_to_hosts(url):
    """
    Adds URL to Hosts file
    """

    grant()

    with open(hosts_path, 'a') as f:
        f.write(redirect + '\t' + 'www.' + url + '\n')
        f.write(redirect + '\t' + url + '\n')

    revoke()

def remove_from_hosts(url):
    """
    Remove URL from hosts file
    """
    grant()
    with open(hosts_path, 'r+') as f:
        content = f.readlines()
        f.seek(0)
        for line in content:
            if url not in line[10:].strip():
                f.write(line)
        f.truncate()
    revoke()


def main():
    app = wx.App()
    
    server = ServerThread(HOST, PORT, Server)

    ex = Example(None, title='Website Blocker')
    ex.Show()

    msg = wx.MessageDialog(None, 'Remember to refresh the browser cache for rules to take effect!', 'INFO', wx.OK | wx.ICON_WARNING)
    msg.ShowModal()

    app.MainLoop()

    server.server_run = False


if __name__ == '__main__':
    main()