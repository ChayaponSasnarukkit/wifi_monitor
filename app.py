import tkinter as tk
import ttkbootstrap as tb
import sqlite3
from tkinter import messagebox
from component.header import Header
from component.node import Node
import re

class MyApp(tk.Tk):

    def add_node(self) :
        node_ip = self.entry.get()
        regexp = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})$"
        if bool(re.match(regexp, node_ip)) :
            #to do check duplicate ip
            self.node = Node(self.subframeBody,self.no,node_ip,"client","","","","","","DHCP","RealTime",2.4,"")
            self.no+=1
            self.node.pack(padx=10, pady=10,anchor="w")
            self.ListObjectNode.append(self.node)
            self.subframeBody.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.popup.destroy()
        else :
            messagebox.showerror("error","invalid ip format !")
            return

    def on_enter(self,event):
        self.button.invoke()

    def convert_to_json(self):
        self.ListNode = {"nodes":{},"server":{},"duration":10,"folder_name":"banC"}
        for e in self.ListObjectNode :
            if e.mode.get() == "server" :
                self.ListNode["server"]["ssid"] = e.e_ssid.get()
                self.ListNode["server"]["password"] = e.e_password.get()
                self.ListNode["server"]["ip_address"] = e.e_ip.get()
                self.ListNode["server"]["net_mask"] = e.e_subnet.get()
                self.ListNode["server"]["gateway_address"] = e.e_gateway.get()
                self.ListNode["server"]["interface_mode"] = e.interface_mode.get()
            elif e.mode.get() == "client" :
                print("ok")
                self.ListNode["nodes"][e.node_ip] = [{"type":"","configuration":{}}]
                self.ListNode["nodes"][e.node_ip][0]["type"] = e.mode.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["client_ip"] = e.e_ip.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["gateway_ip"] = e.e_gateway.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["ap_name"] = e.e_ssid.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["password"] = e.e_password.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["netmask"] = e.e_subnet.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["interface_mode"] = e.interface_mode.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["protocol"] = e.protocol.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["channel"] = e.channel.get()
                self.ListNode["nodes"][e.node_ip][0]["configuration"]["server_ip"] = e.server_ip
            
        print(self.ListNode)
                
    
    def node_popup(self):
        self.popup = tb.Toplevel(self)
        self.popup.title("add node")
        self.popup.resizable(False, False)
        self.popup.geometry(f"260x50+{self.winfo_x()+25}+{self.winfo_y()+150}")
        self.label = tb.Label(self.popup,text="node ip :")
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.entry = tb.Entry(self.popup)
        self.entry.grid(row=0, column=1, padx=5, pady=10)

        self.add_icon = tk.PhotoImage(file="icon/add_39x30.png")
        self.button = tk.Button(self.popup,image=self.add_icon,compound=tk.CENTER, width=39, height=30, command=self.add_node)
        self.button.grid(row=0, column=2, padx=5, pady=10)
        self.button.configure(bg="white",activebackground="white")

        self.entry.bind("<Return>", lambda event: self.on_enter(event))
        self.popup.grab_set()
        self.popup.wait_window()

    def display(self):
        for e in self.ListObjectNode :
            e.pack_forget()
        self.ListObjectNode = []

        self.node = Node(self.subframeBody, 1, "host", "server", self.ListNode["server"]["ssid"], self.ListNode["server"]["password"], self.ListNode["server"]["ip_address"], self.ListNode["server"]["net_mask"], self.ListNode["server"]["gateway_address"], self.ListNode["server"]["interface_mode"],"", "", "")
        self.node.pack(padx=10, pady=10,anchor="w")
        self.ListObjectNode.append(self.node)
        self.no = 2
        for e in self.ListNode["nodes"] :
            self.node = Node(self.subframeBody, self.no, e, self.ListNode["nodes"][e][0]["type"], self.ListNode["nodes"][e][0]["configuration"]["ap_name"], self.ListNode["nodes"][e][0]["configuration"]["password"], self.ListNode["nodes"][e][0]["configuration"]["client_ip"], self.ListNode["nodes"][e][0]["configuration"]["netmask"], self.ListNode["nodes"][e][0]["configuration"]["gateway_ip"], self.ListNode["nodes"][e][0]["configuration"]["interface_mode"], self.ListNode["nodes"][e][0]["configuration"]["protocol"], self.ListNode["nodes"][e][0]["configuration"]["channel"], self.ListNode["nodes"][e][0]["configuration"]["server_ip"])
            self.no+=1
            self.node.pack(padx=10, pady=10,anchor="w")
            self.ListObjectNode.append(self.node)

        self.no += 1
        self.subframeBody.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        region = self.canvas.bbox("all")
        max_y = region[3] - region[1] - self.canvas.winfo_height()

        if event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

        if self.canvas.winfo_y() < 0:
            self.canvas.yview_moveto(0)
        elif self.canvas.winfo_y() > max_y:
            self.canvas.yview_moveto(1)
        self.focus_set()

    def __init__(self):
        super().__init__()
        self.title("WiFi Monitoring System")
        self.geometry('700x700')
        self.resizable(0, 0)
        self.conn = sqlite3.connect("Scenario.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(f'''SELECT ScenarioName FROM template
                        ''')
        self.ScenarioNamelist = self.cursor.fetchall()
        self.ScenarioName = tk.StringVar()
        self.ScenarioName.set("select scenario")
        self.Describe = tk.StringVar()
        self.Describe.set(".....")
        #to do when create object server mode must create dump
        self.ListNode = {
            "nodes": {
            },
            "server": {
                "ssid": "",
                "password": "",
                "ip_address": "",
                "net_mask": "",
                "gateway_address": "",
                "interface_mode": "DHCP"
            },
            "duration": 10,
            "folder_name": "banC"
        }
        self.ListObjectNode = []

        self.header = Header(self)
        self.header.pack(padx=10,pady=10, anchor="nw")

        self.framemiddle = tb.Frame(self)
        self.add_node_icon = tk.PhotoImage(file="icon/add_node.png")
        self.button = tk.Button(self.framemiddle, image=self.add_node_icon,compound=tk.CENTER, width=72, height=30, command=self.node_popup)
        self.button.grid(row=0, column=0, padx=(0,5))
        self.button.configure(bg="white",activebackground="white")
        
        self.scan_node_icon = tk.PhotoImage(file="icon/scan_node.png")
        self.button = tk.Button(self.framemiddle, image=self.scan_node_icon,compound=tk.CENTER, width=77, height=30, command=self.convert_to_json)
        self.button.configure(bg="white",activebackground="white")
        self.button.grid(row=0, column=1, padx=5)
        self.framemiddle.pack(padx=25,pady=5,anchor="w")

        self.bgframeBody = tk.Canvas(self,width=5000, height=3500)
        self.bgframeBody.create_rectangle(0, 0, 660, 459, fill="#fcba03", outline=self.cget('bg'))
        self.bgframeBody.place(x=20,y=211)
        
        self.frameBody = tb.Frame(self)
        self.canvas = tk.Canvas(self.frameBody)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.frameBody, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.subframeBody = tb.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.subframeBody, anchor=tk.NW)
        self.subframeBody.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.frameBody.pack(padx=30, pady=(15,40), fill=tk.BOTH, expand=True)
        #self.canvas.config(width=600)

        self.update()

        self.node = Node(self.subframeBody, 1, "host", "server", self.ListNode["server"]["ssid"], self.ListNode["server"]["password"], self.ListNode["server"]["ip_address"], self.ListNode["server"]["net_mask"], self.ListNode["server"]["gateway_address"], self.ListNode["server"]["interface_mode"],"","","")
        self.node.pack(padx=10, pady=10,anchor="w")
        self.ListObjectNode.append(self.node)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.no = 2

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()