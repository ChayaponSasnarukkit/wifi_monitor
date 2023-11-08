import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox

class NodeClient(tb.Frame):

    def __init__(self, master, client_ip, server_ip, protocol, ssid):
        super().__init__(master)
        self.master = master
        self.client_ip = client_ip
        self.server_ip = server_ip
        self.protocol = protocol
        self.ssid = ssid
