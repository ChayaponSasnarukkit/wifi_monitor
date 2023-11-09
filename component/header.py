import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
import requests
import threading
import time
import json
from component.node import Node

class Header(tb.Frame):

    def delete_scenario(self) :
        self.master.conn.execute(f"DELETE FROM template WHERE ScenarioName = '{self.combobox.get()}'")
        self.master.conn.commit()
        self.master.ScenarioNamelist.remove(self.combobox.get())
        self.combobox["values"] = self.master.ScenarioNamelist
        self.combobox.set("select scenario")
        self.master.Describe.set("")
        self.master.ListNode = {
            "nodes": {
            },
            "server": {
                "ssid": "",
                "password": "",
                "ip_address": "",
                "net_mask": "",
                "gateway_address": "",
                "interface_mode": "DHCP",
                "channel": 2.4
            },
            "duration": 10,
            "folder_name": "banC"
        }
        self.master.display()
        self.popup.destroy()

    def delete_popup(self) :
        self.popup = tb.Toplevel(self)
        self.popup.title("save")
        self.popup.resizable(False, False)
        self.popup.geometry(f"250x80+{self.master.winfo_x()+50}+{self.master.winfo_y()+50}")
        frame = tk.Frame(self.popup)
        frame.pack(pady=5)
        tb.Label(frame,text="Do you want to delete ?").grid(column=0,row=0,padx=5,pady=5,columnspan=2)
        self.ok_icon = tk.PhotoImage(file="icon/ok_33x30.png")
        ok_button = tk.Button(frame,image=self.ok_icon,compound=tk.CENTER, width=33, height=30,command=self.delete_scenario)
        ok_button.grid(row=1, column=0, padx=5, pady=5)
        ok_button.configure(bg="white",activebackground="white")

        self.cancel_icon = tk.PhotoImage(file="icon/cancel_54x30.png")
        close_button = tk.Button(frame,image=self.cancel_icon,compound=tk.CENTER, width=54, height=30, command=self.popup.destroy)
        close_button.grid(row=1, column=1, padx=5, pady=5)
        close_button.configure(bg="white",activebackground="white")

        self.popup.focus_set()
        self.popup.bind("<Return>",lambda event : ok_button.invoke())
        self.popup.bind("<Escape>",lambda event : close_button.invoke())

    def save_as_scenario(self) :
        name = self.entry_new_popup.get()
        cursor = self.master.conn.cursor()
        cursor.execute(f'''SELECT ScenarioName FROM template
                    WHERE ScenarioName = '{name}'
                    ''')
        output = cursor.fetchall()
        if output == [] :
            describe = self.entry_new_popup_describe.get()
            self.master.convert_to_json()
            config = json.dumps(self.master.ListNode)
            self.master.ScenarioNamelist.append(name)
            self.combobox["values"] = self.master.ScenarioNamelist
            self.master.conn.execute(f"INSERT INTO template VALUES ('{name}','{describe}','{config}')")
            self.master.conn.commit()
            self.master.Describe.set(describe)
            self.master.ScenarioName.set(name)
            self.popup.destroy()
        else:
            messagebox.showerror("error","name already use")
            return

    def save_scenario(self) :
        self.master.convert_to_json()
        config = json.dumps(self.master.ListNode)
        self.master.conn.execute(f"UPDATE template SET Config = '{config}', Describe = '{self.master.Describe.get()}' WHERE ScenarioName = '{self.master.ScenarioName.get()}'")
        cursor = self.master.conn.cursor()
        cursor.execute(f'''SELECT * FROM template
            ''')
        output = cursor.fetchall()
        self.master.conn.commit()
        self.popup.destroy()

    def save_as_scenario_popup(self) :
        self.popup = tb.Toplevel(self)
        self.popup.title("save as")
        self.popup.resizable(False, False)
        self.popup.geometry(f"275x140+{self.master.winfo_x()+50}+{self.master.winfo_y()+50}")
        self.f = tb.Frame(self.popup)
        tb.Label(self.popup,text="(save as)").grid(row=0,column=0, padx = (10,0), pady = 15,sticky="n")
        frame = tk.Frame(self.popup)
        frame.grid(row=0,column=1)
        tb.Label(frame, text="Name :").grid(row=0, column=0, padx=5, pady=5)
        self.entry_new_popup = tb.Entry(frame)
        self.entry_new_popup.grid(row=0, column=1, padx=5, pady=10, columnspan=2)
        tb.Label(frame, text="Describe :").grid(row=1, column=0, padx=5, pady=5)
        self.entry_new_popup_describe = tb.Entry(frame)
        self.entry_new_popup_describe.grid(row=1, column=1, padx=5, pady=10, columnspan=2)
        
        self.ok_icon = tk.PhotoImage(file="icon/ok_33x30.png")
        ok_button = tk.Button(frame,image=self.ok_icon,compound=tk.CENTER, width=33, height=30, command=self.save_as_scenario)
        ok_button.grid(row=2, column=1, padx=5, pady=5)
        ok_button.configure(bg="white",activebackground="white")

        self.cancel_icon = tk.PhotoImage(file="icon/cancel_54x30.png")
        close_button = tk.Button(frame,image=self.cancel_icon,compound=tk.CENTER, width=54, height=30, command=self.popup.destroy)
        close_button.grid(row=2, column=2, padx=5, pady=5)
        close_button.configure(bg="white",activebackground="white")

        self.entry_new_popup.bind("<Return>", lambda event: ok_button.invoke())
        self.entry_new_popup.bind("<Down>", lambda event: self.entry_new_popup_describe.focus_set())
        self.entry_new_popup.bind("<Escape>", lambda event: close_button.invoke())
        self.entry_new_popup_describe.bind("<Return>", lambda event: ok_button.invoke())
        self.entry_new_popup_describe.bind("<Up>", lambda event: self.entry_new_popup.focus_set())
        self.entry_new_popup_describe.bind("<Escape>", lambda event: close_button.invoke())
        self.entry_new_popup.focus_set()
        self.popup.grab_set()
        self.popup.wait_window()

    def save_scenario_popup(self) :
        if self.master.ScenarioName.get() == "select scenario" :
            self.save_as_scenario()
        else :
            self.popup = tb.Toplevel(self)
            self.popup.title("save")
            self.popup.resizable(False, False)
            self.popup.geometry(f"250x80+{self.master.winfo_x()+50}+{self.master.winfo_y()+50}")
            frame = tk.Frame(self.popup)
            frame.pack(pady=5)
            tb.Label(frame,text="Do you want to save ?").grid(column=0,row=0,padx=5,pady=5,columnspan=2)
            self.ok_icon = tk.PhotoImage(file="icon/ok_33x30.png")
            ok_button = tk.Button(frame,image=self.ok_icon,compound=tk.CENTER, width=33, height=30,command=self.save_scenario)
            ok_button.grid(row=1, column=0, padx=5, pady=5)
            ok_button.configure(bg="white",activebackground="white")

            self.cancel_icon = tk.PhotoImage(file="icon/cancel_54x30.png")
            close_button = tk.Button(frame,image=self.cancel_icon,compound=tk.CENTER, width=54, height=30, command=self.popup.destroy)
            close_button.grid(row=1, column=1, padx=5, pady=5)
            close_button.configure(bg="white",activebackground="white")

            self.popup.focus_set()
            self.popup.bind("<Return>",lambda event : ok_button.invoke())
            self.popup.bind("<Escape>",lambda event : close_button.invoke())

    def clear_combobox_text(self, event):
        self.current_text = self.combobox.get()
        if (self.current_text,) in self.master.ScenarioNamelist :
            return
        if self.current_text == "select scenario" :
            self.combobox.event_generate('<Down>')
            return
        self.master.ScenarioName.set('')
    
    def on_combobox_select(self, event):
        selected_value = self.combobox.get()
        self.master.ListNode = selected_value
        self.combobox.selection_clear()
        cursor = self.master.conn.cursor()
        cursor.execute("SELECT * FROM template")
        output = cursor.fetchall()
        cursor.execute(f"SELECT * FROM template WHERE ScenarioName = '{selected_value}'")
        data = cursor.fetchall()
        self.master.ScenarioName.set(data[0][0])
        self.master.Describe.set(data[0][1])
        self.master.ListNode = json.loads(data[0][2])
        self.master.display()

    def new_popup(self):
        self.popup = tb.Toplevel(self)
        self.popup.title("new scenario")
        self.popup.resizable(False, False)
        self.popup.geometry(f"250x140+{self.master.winfo_x()+50}+{self.master.winfo_y()+50}")
        frame = tk.Frame(self.popup)
        frame.pack()
        tb.Label(frame, text="Name :").grid(row=0, column=0, padx=5, pady=5)
        self.entry_new_popup = tb.Entry(frame)
        self.entry_new_popup.grid(row=0, column=1, padx=5, pady=10, columnspan=2)
        tb.Label(frame, text="Describe :").grid(row=1, column=0, padx=5, pady=5)
        self.entry_new_popup_describe = tb.Entry(frame)
        self.entry_new_popup_describe.grid(row=1, column=1, padx=5, pady=10, columnspan=2)
        
        self.ok_icon = tk.PhotoImage(file="icon/ok_33x30.png")
        ok_button = tk.Button(frame,image=self.ok_icon,compound=tk.CENTER, width=33, height=30, command=self.new_scenario)
        ok_button.grid(row=2, column=1, padx=5, pady=5)
        ok_button.configure(bg="white",activebackground="white")

        self.cancel_icon = tk.PhotoImage(file="icon/cancel_54x30.png")
        close_button = tk.Button(frame,image=self.cancel_icon,compound=tk.CENTER, width=54, height=30, command=self.popup.destroy)
        close_button.grid(row=2, column=2, padx=5, pady=5)
        close_button.configure(bg="white",activebackground="white")

        self.entry_new_popup.bind("<Return>", lambda event: ok_button.invoke())
        self.entry_new_popup.bind("<Down>", lambda event: self.entry_new_popup_describe.focus_set())
        self.entry_new_popup.bind("<Escape>", lambda event: close_button.invoke())
        self.entry_new_popup_describe.bind("<Return>", lambda event: ok_button.invoke())
        self.entry_new_popup_describe.bind("<Up>", lambda event: self.entry_new_popup.focus_set())
        self.entry_new_popup_describe.bind("<Escape>", lambda event: close_button.invoke())
        self.entry_new_popup.focus_set()
        self.popup.grab_set()
        self.popup.wait_window()

    def new_scenario(self):
        name = self.entry_new_popup.get()
        cursor = self.master.conn.cursor()
        cursor.execute(f'''SELECT ScenarioName FROM template
                    WHERE ScenarioName = '{name}'
                    ''')
        output = cursor.fetchall()
        if output == [] :
            describe = self.entry_new_popup_describe.get()
            for i in self.master.ListObjectNode :
                i.pack_forget()
            self.master.ListObjectNode = []
            self.node = Node(self.master.subframeBody, 1, "host", "server", self.master.ListNode["server"]["ssid"], self.master.ListNode["server"]["password"], self.master.ListNode["server"]["ip_address"], self.master.ListNode["server"]["net_mask"], self.master.ListNode["server"]["gateway_address"], self.master.ListNode["server"]["interface_mode"],2.4,"","")
            self.master.ListObjectNode.append(self.node)
            config = {
                "nodes": {
                },
                "server": {
                    "ssid": "",
                    "password": "",
                    "ip_address": "",
                    "net_mask": "",
                    "gateway_address": "",
                    "interface_mode": "DHCP",
                    "channel": 2.4
                },
                "duration": 10,
                "folder_name": "banC"
            }
            self.master.ListNode = config
            config = json.dumps(config)
            self.master.conn.execute(f"INSERT INTO template VALUES ('{name}','{describe}','{config}')")
            self.master.conn.commit()
            self.combobox['values'] = list(self.combobox['values'])+[name]
            self.master.Describe.set(describe)
            self.master.ScenarioName.set(name)
            self.master.ScenarioNamelist.append(name)
            self.master.display()
            self.popup.destroy()
        else:
            messagebox.showerror("error","name already use")
            return

    def edit_popup(self):
        self.popup = tb.Toplevel(self)
        self.popup.title("edit describe")
        self.popup.resizable(False, False)
        self.popup.geometry(f"220x85+{self.master.winfo_x()+50}+{self.master.winfo_y()+50}")
        self.frame = tk.Frame(self.popup)
        self.frame.pack()
        tb.Label(self.frame, text="Describe :").grid(row=0, column=0, padx=5, pady=5)
        self.e_edit_popup = tk.Entry(self.frame)
        self.e_edit_popup.insert(0,self.master.Describe.get())
        self.e_edit_popup.grid(row=0, column=1, padx=5, pady=10, columnspan=2)
        
        self.ok_icon = tk.PhotoImage(file="icon/ok_33x30.png")
        ok_button = tk.Button(self.frame,image=self.ok_icon,compound=tk.CENTER, width=33, height=30, command=self.edit_describe)
        ok_button.grid(row=2, column=1, padx=5, pady=5)
        ok_button.configure(bg="white",activebackground="white")
        
        self.cancel_icon = tk.PhotoImage(file="icon/cancel_54x30.png")
        close_button = tk.Button(self.frame,image=self.cancel_icon,compound=tk.CENTER, width=54, height=30, command=self.popup.destroy)
        close_button.grid(row=2, column=2, padx=5, pady=5)
        close_button.configure(bg="white",activebackground="white")
        
        self.popup.grab_set()
        self.popup.wait_window()
    
    def edit_describe(self):
        self.master.Describe.set(self.e_edit_popup.get())
        self.popup.destroy()

    def disable_mousewheel(self,event):
        return "break"
    
    def check_thread(self):
        if self.waiting_thread.is_alive():
            self.popup.after(100, self.check_thread)
        else:
            self.popup.destroy()

    def run_scenario(self):
        self.popup = tk.Toplevel(self.master)
        self.popup.title("run scenario")
        self.popup.resizable(False, False)
        self.popup.geometry(f"200x100+{self.master.winfo_x()+210}+{self.master.winfo_y()+150}")
        self.frame = tk.Frame(self.popup)
        self.frame.pack(expand=True)
        self.l1 = tk.Label(self.frame,text="running . . .")
        self.l1.pack()
        requests_thread = threading.Thread(target=requests.post, kwargs={'url': "http://127.0.0.1:8888/run_simulation",'json': self.master.ListNode})
        requests_thread.start()
        self.waiting_thread = requests_thread
        self.popup.grab_set()   
        self.popup.after(0, self.check_thread)
        self.popup.mainloop()

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tb.Label(self,text="Scenario :").grid(row=0, column=0, padx=5, pady=5)
        self.labelframe = tb.Labelframe(self,text="Describe")
        self.labelframe.grid(row=2, column=0, padx=5, pady=5,sticky="ewn",columnspan=2,)
        tb.Label(self.labelframe, textvariable=self.master.Describe,wraplength=300).pack(side=tk.LEFT,padx=5)

        self.edit_icon = tk.PhotoImage(file="icon/edit.png")
        self.b_edit = tk.Button(self,image=self.edit_icon,compound=tk.CENTER, width=20, height=20, command=self.edit_popup)
        self.b_edit.grid(row=2, column=2, padx=5, pady=16,sticky="nw")
        self.b_edit.configure(bg="white",activebackground="white")

        #Select Scenario
        self.combobox = tb.Combobox(self, textvariable=self.master.ScenarioName, values=self.master.ScenarioNamelist, state="readonly")
        self.combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combobox.bind("<MouseWheel>", self.disable_mousewheel)
        self.combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)
        
        #run scenario
        self.run_icon = tk.PhotoImage(file="icon/run.png")
        self.Button1 = tk.Button(self, image=self.run_icon,compound=tk.CENTER, width=38, height=30, command=self.run_scenario)
        self.Button1.grid(row=0,column=2,padx=5)
        self.Button1.configure(bg="white",activebackground="white")

        #control_panel
        self.control_panel = tk.Frame(self)
        self.control_panel.grid(row=1, column=1, padx=5, pady=5,)

        #new Button
        self.new_icon = tk.PhotoImage(file="icon/new.png")
        self.Button1 = tk.Button(self.control_panel, image=self.new_icon,compound=tk.CENTER, width=42, height=30, command=self.new_popup)
        self.Button1.grid(row=0, column=0, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")

        #save Button
        self.save_icon = tk.PhotoImage(file="icon/save.png")
        self.Button1 = tk.Button(self.control_panel, image=self.save_icon,compound=tk.CENTER, width=45, height=30, command=self.save_scenario_popup)
        self.Button1.grid(row=0, column=1, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")

        #save as Button
        self.save_as_icon = tk.PhotoImage(file="icon/save_as.png")
        self.Button1 = tk.Button(self.control_panel, image=self.save_as_icon,compound=tk.CENTER, width=60, height=30, command=self.save_as_scenario_popup)
        self.Button1.grid(row=0, column=2, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")

        #delete Button
        self.delete_icon = tk.PhotoImage(file="icon/delete.png")
        self.Button1 = tk.Button(self.control_panel, image=self.delete_icon,compound=tk.CENTER, width=60, height=30, command=self.delete_popup)
        self.Button1.grid(row=0, column=3, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")



       
