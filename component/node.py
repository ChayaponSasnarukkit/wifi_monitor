import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
import re

class Node(tb.Frame):

    def disable_mousewheel(self,event):
        return "break"

    def on_combobox_select(self,event,this) :
        this.selection_clear()

    def show_password(self):
        self.show_pass = not self.show_pass
        if self.show_pass:
            self.e_password.config(show="")
            self.show_button.config(image=self.show_icon, command=self.hide_password)
        else:
            self.e_password.config(show="*")
            self.show_button.config(image=self.hide_icon, command=self.show_password)

    def hide_password(self):
        self.show_password()

    def check_ip_format(self,event,this):
        regexp = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})$"
        if bool(re.match(regexp, this.get())):
            this.configure(highlightbackground="#28a745", highlightcolor="#28a745")
        else:
            this.configure(highlightbackground="#dc3545", highlightcolor="#dc3545")
    
    def select_interface_mode(self):
        if self.interface_mode.get() == "DHCP":
            self.e_ip.delete(0, 'end')
            self.e_subnet.delete(0, 'end')
            self.e_gateway.delete(0, 'end')
            self.e_ip["state"] = "disabled"
            self.e_subnet["state"] = "disabled"
            self.e_gateway["state"] = "disabled"
            self.e_ip.configure(highlightbackground="#BBBBBB", highlightcolor="#BBBBBB")
            self.e_subnet.configure(highlightbackground="#BBBBBB", highlightcolor="#BBBBBB")
            self.e_gateway.configure(highlightbackground="#BBBBBB", highlightcolor="#BBBBBB")
        else :
            self.e_ip.configure(highlightbackground="#dc3545", highlightcolor="#dc3545")
            self.e_subnet.configure(highlightbackground="#dc3545", highlightcolor="#dc3545")
            self.e_gateway.configure(highlightbackground="#dc3545", highlightcolor="#dc3545")
            self.e_ip.bind("<KeyRelease>", lambda event, text=self.e_ip: self.check_ip_format(event, text))
            self.e_subnet.bind("<KeyRelease>", lambda event, text=self.e_subnet: self.check_ip_format(event, text))
            self.e_gateway.bind("<KeyRelease>", lambda event, text=self.e_gateway: self.check_ip_format(event, text))
            self.e_ip["state"] = "normal"
            self.e_subnet["state"] = "normal"
            self.e_gateway["state"] = "normal"

    def __init__(self, master, index,node_ip, mode, ssid, password, ip_address, net_mask, gateway_address, interface_mode, channel, protocol, server_ip):
        super().__init__(master)
        #Server
        self.master = master
        self.index = index
        self.node_ip = node_ip
        self.mode = tk.StringVar()
        self.mode.set(mode)
        self.ssid = ssid
        self.password = password
        self.ip_address = ip_address
        self.net_mask = net_mask
        self.gateway_address = gateway_address
        self.interface_mode = tk.StringVar()
        self.interface_mode.set(interface_mode)
        self.server_ip = "192.168.227.51"

        #client
        self.protocol = tk.StringVar()
        self.protocol.set(protocol)
        self.channel = tk.IntVar()
        self.channel.set(channel)
        
        self.frame = tb.Labelframe(self, text=f"no.{self.index}",bootstyle="dark",style="Custom.TLabelframe")
        tb.Label(self.frame, text=f"node ip : ").grid(row=0, column=0,padx=5,pady=5)
        self.e = tk.Entry(self.frame)
        self.e.grid(row=0, column=1,padx=(0,5),pady=5)

        tb.Label(self.frame, text=f"mode : ").grid(row=0, column=2,padx=5,pady=5,sticky='w')
        self.frame.columnconfigure(3, weight=100)
        self.rbframe = tb.Frame(self.frame)
        tb.Label(self.rbframe, text="config interface : ").grid(row=0, column=0,padx=(0,5),pady=5)
        tb.Radiobutton(self.rbframe,text="DHCP",variable=self.interface_mode,value="DHCP",command=lambda: self.select_interface_mode()).grid(row=0, column=1,padx=5,pady=5)
        tb.Radiobutton(self.rbframe,text="STATIC",variable=self.interface_mode,value="STATIC",command=lambda: self.select_interface_mode()).grid(row=1, column=1,padx=5,pady=5)
        tb.Label(self.rbframe, text="ip : ").grid(row=1, column=2,padx=5,pady=5)
        self.e_ip = tk.Entry(self.rbframe,highlightbackground="red")
        self.e_ip.grid(row=1, column=3,padx=(0,5),pady=5)
        tb.Label(self.rbframe, text="subnet :   ").grid(row=1, column=4,padx=(5,0),pady=5,sticky='e')
        self.e_subnet = tk.Entry(self.rbframe)
        self.e_subnet.grid(row=1, column=5,padx=(0,5),pady=5)
        tb.Label(self.rbframe, text="gateway : ").grid(row=2, column=4,padx=5,pady=5,sticky="w")
        self.e_gateway = tk.Entry(self.rbframe)
        self.e_gateway.grid(row=2, column=5,padx=(0,5),pady=5)
        self.select_interface_mode()
        self.rbframe.grid(row=1, column=1,padx=(0,5),pady=5,sticky="w",columnspan=3)
        
        self.f = tb.Frame(self.frame)
        tb.Label(self.f, text="ssid : ").grid(padx=5,pady=5,row=0, column=0)
        self.e_ssid = tk.Entry(self.f,width = 15)
        self.e_ssid.grid(pady=5,row=0,column=1)
        tb.Label(self.f, text="password : ").grid(padx=5,pady=5,row=0, column=2)
        self.e_password = tk.Entry(self.f,show="*",width = 15)
        self.e_password.grid(pady=5,row=0,column=3)
        self.show_icon = tk.PhotoImage(file="icon/show.png")
        self.hide_icon = tk.PhotoImage(file="icon/hide.png")
        self.show_pass = False
        self.show_button = tk.Button(self.f, image=self.hide_icon, command=self.show_password, compound=tk.CENTER, width=20, height=20)
        self.show_button.configure(bg="white",activebackground="white")
        self.show_button.grid(padx=5,pady=5,row=0, column=4)
        tb.Label(self.f, text="bandwidth : ",).grid(padx=5,pady=5,row=0, column=5)
        self.cb_channel = tb.Combobox(self.f, textvariable=self.channel,values=[2.4,5], state="readonly",width=3)
        self.cb_channel.grid(pady=5,row=0,column=6)
        self.cb_channel.bind("<<ComboboxSelected>>", lambda event, this = self.cb_channel: self.on_combobox_select(event,this))
        self.cb_channel.bind("<MouseWheel>", self.disable_mousewheel)
        tb.Label(self.f, text="GHz",).grid(padx=5,pady=5,row=0, column=7)
        self.f.grid(row=2, column=1,padx=(0,5),pady=5,sticky="w",columnspan=4)

        if self.mode.get() == "server" :
            self.modeCB = tb.Combobox(self.frame, textvariable=self.mode, value="server", state="readonly", width=10)
            self.modeCB.grid(row=0, column=3,padx=(0,5),pady=5,sticky='w')
            self.modeCB.bind("<MouseWheel>", self.disable_mousewheel)
            self.modeCB.bind("<<ComboboxSelected>>", lambda event, this = self.modeCB: self.on_combobox_select(event,this))
        else :
            self.modeCB = tb.Combobox(self.frame, textvariable=self.mode, values=["Client","AP"], state="readonly")
            self.modeCB.grid(row=0, column=3,padx=(0,5),pady=5,sticky='w')
            self.modeCB.bind("<MouseWheel>", self.disable_mousewheel)
            self.modeCB.bind("<<ComboboxSelected>>", lambda event, this = self.modeCB: self.on_combobox_select(event,this))

            self.cross_icon = tk.PhotoImage(file="icon/cross.png")
            self.b_cross = tk.Button(self.frame,image=self.cross_icon,compound=tk.CENTER, width=25, height=25)
            self.b_cross.grid(row=0, column=3,padx=10,pady=5,sticky='e')
            self.b_cross.configure(bg="white",activebackground="white")

            self.f = tb.Frame(self.frame)
            tb.Label(self.f, text="protocol : ").grid(padx=5,pady=5,row=0, column=0)
            self.cb_protocol = tb.Combobox(self.f, textvariable=self.protocol,values=["Realtime","Web","Socket"], state="readonly")
            self.cb_protocol.grid(pady=5,row=0,column=1)
            self.cb_protocol.bind("<<ComboboxSelected>>", lambda event, this = self.cb_protocol: self.on_combobox_select(event,this))
            self.cb_protocol.bind("<MouseWheel>", self.disable_mousewheel)
            self.f.grid(row=3, column=1,padx=(0,5),pady=5,sticky="w",columnspan=4)
        
        self.e.insert(0,node_ip)
        self.e_ssid.insert(0,ssid)
        self.e_password.insert(0,password)
        self.e_ip.insert(0,ip_address)
        self.e_subnet.insert(0,net_mask)
        self.e_gateway.insert(0,gateway_address)
        self.check_ip_format(None, self.e_ip)
        self.check_ip_format(None, self.e_subnet)
        self.check_ip_format(None, self.e_gateway)
        if self.mode.get()=="server" :
            self.e["state"] = "disabled"
        else :
            self.e.bind("<KeyRelease>", lambda event, text=self.e: self.check_ip_format(event, text))
            self.check_ip_format(None, self.e)
        
        
        self.frame.pack(pady=(0,5),padx=5)
        