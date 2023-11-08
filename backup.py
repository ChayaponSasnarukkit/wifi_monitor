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
            for i in range(len(self.ListNode)) :
                if self.ListNode[i]["node_ip"] == node_ip :
                    messagebox.showerror("error","ip already add !")
                    return
            self.ListNode.append({"node_ip":node_ip,"config":[]})
            self.node = Node(self.subframeBody,self.no,node_ip,"Client",[])
            self.no+=1
            self.node.pack(padx=10, pady=10,anchor="w")
            self.subframeBody.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.popup.destroy()
        else :
            messagebox.showerror("error","invalid ip format !")
            return

    def node_popup(self):
        self.popup = tb.Toplevel(self)
        self.popup.title("add node")
        self.popup.resizable(False, False)
        self.popup.geometry(f"260x50+{self.winfo_x()+25}+{self.winfo_y()+150}")
        self.label = tb.Label(self.popup,text="node ip :")
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.entry = tb.Entry(self.popup)
        self.entry.grid(row=0, column=1, padx=5, pady=10)
        self.button = tb.Button(self.popup,text="add", bootstyle="primary", command=self.add_node)
        self.button.grid(row=0, column=2, padx=5, pady=10)
        self.popup.grab_set()
        self.popup.wait_window()

    def __init__(self):
        super().__init__()
        self.title("WiFi Monitoring")
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
        self.ListNode = []

        self.no = 1

        self.header = Header(self)
        self.header.pack(padx=10,pady=10, anchor="nw")

        self.framemiddle = tb.Frame(self)
        tb.Button(self.framemiddle, text="add node", bootstyle="primary", command=self.node_popup).grid(row=0, column=0, padx=(0,5))
        tb.Button(self.framemiddle, text="scan node", bootstyle="primary").grid(row=0, column=1, padx=5)
        self.framemiddle.pack(padx=15,pady=5,anchor="w")

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

        self.frameBody.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        self.canvas.config(width=600)  # Adjust as per your need

        self.update()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()