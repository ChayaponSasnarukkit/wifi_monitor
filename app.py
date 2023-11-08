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
            self.node = Node(self.subframeBody,self.no,node_ip,"Client",[])
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
        self.no = len(self.ListNode)
        for i in range(len(self.ListNode)) :
            self.node = Node(self.subframeBody, self.no, self.ListNode[i]["node_ip"],self.ListNode[i]["mode"],self.ListNode[i]["config"])
            self.node.pack(padx=10, pady=10,anchor="w")
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
        self.ListNode = [{"mode" : "Server","node_ip":"host","config" : [{"client_ip": "", "netmask": "", "gateway_ip": "", "ssid": "", "password": ""}]}]
        self.ListObjectNode = []

        self.header = Header(self)
        self.header.pack(padx=10,pady=10, anchor="nw")

        self.framemiddle = tb.Frame(self)
        self.add_node_icon = tk.PhotoImage(file="icon/add_node.png")
        self.button = tk.Button(self.framemiddle, image=self.add_node_icon,compound=tk.CENTER, width=72, height=30, command=self.node_popup)
        self.button.grid(row=0, column=0, padx=(0,5))
        self.button.configure(bg="white",activebackground="white")
        
        self.scan_node_icon = tk.PhotoImage(file="icon/scan_node.png")
        self.button = tk.Button(self.framemiddle, image=self.scan_node_icon,compound=tk.CENTER, width=77, height=30)
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

        self.frameBody.pack(padx=30, pady=(20,40), fill=tk.BOTH, expand=True)
        #self.canvas.config(width=600)

        self.update()

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.display()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()