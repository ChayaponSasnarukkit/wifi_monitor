import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
import requests
import threading
import time

class Header(tb.Frame):
    
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
        self.combobox.selection_clear()
        

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

        self.popup.grab_set()
        self.popup.wait_window()

    def new_scenario(self):
        name = self.entry_new_popup.get()
        describe = self.entry_new_popup_describe.get()
        cursor = self.master.conn.cursor()
        cursor.execute(f'''SELECT ScenarioName FROM template
                    WHERE ScenarioName = '{name}'
                    ''')
        output = cursor.fetchall()
        if output == [] :
            self.master.conn.execute(f"INSERT INTO template VALUES ('{name}','{describe}','[]')")
            self.master.conn.commit()
            self.combobox['values'] = list(self.combobox['values'])+[name]
            self.master.Describe.set(describe)
            self.master.ScenarioName.set(name)
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
        self.e_edit_popup = self.entry_edit_popup = tk.Entry(self.frame)
        self.e_edit_popup.insert(0,self.master.Describe.get())
        self.entry_edit_popup.grid(row=0, column=1, padx=5, pady=10, columnspan=2)
        
        self.ok_icon = tk.PhotoImage(file="icon/ok_33x30.png")
        ok_button = tk.Button(self.frame,image=self.ok_icon,compound=tk.CENTER, width=33, height=30, command=self.new_scenario)
        ok_button.grid(row=2, column=1, padx=5, pady=5)
        ok_button.configure(bg="white",activebackground="white")
        
        self.cancel_icon = tk.PhotoImage(file="icon/cancel_54x30.png")
        close_button = tk.Button(self.frame,image=self.cancel_icon,compound=tk.CENTER, width=54, height=30, command=self.popup.destroy)
        close_button.grid(row=2, column=2, padx=5, pady=5)
        close_button.configure(bg="white",activebackground="white")
        
        self.popup.grab_set()
        self.popup.wait_window()
    
    def edit_describe(self):
        self.master.Describe.set(self.entry_edit_popup.get())
        self.popup.destroy()

    def disable_mousewheel(self,event):
        return "break"
    
    def check_thread(self):
        if self.waiting_thread.is_alive():
            self.popup.after(100, self.check_thread)
        else:
            self.popup.destroy()

    def run_scenario(self):
        print(self.master)
        self.popup = tk.Toplevel(self.master)
        self.popup.title("run scenario")
        self.popup.resizable(False, False)
        self.popup.geometry(f"200x100+{self.master.winfo_x()+210}+{self.master.winfo_y()+150}")
        self.frame = tk.Frame(self.popup)
        self.frame.pack(expand=True)
        self.l1 = tk.Label(self.frame,text="running . . .")
        self.l1.pack()

        payload = {
            "nodes": {
            "192.168.137.215": [
                {
                    "type": "client",
                    "configuration": {
                        "client_ip": "192.168.227.52",
                        "server_ip": "192.168.227.51",
                        "gateway_ip": "192.168.227.79",
                        "ap_name": "GalaxyNote10+25bc",
                        "password": "qbil0530",
                        "netmask": "255.255.255.0",
                        "channel": 5
                    }
                    }
                ]
            },
            "server": {
                "ssid": "GalaxyNote10+25bc",
                "password": "qbil0530",
                "ip_address": "192.168.227.51",
                "net_mask": "255.255.255.0",
                "gateway_address": "192.168.227.79"
            },
            "duration": 10,
            "folder_name": "banC"
        }
        print(payload)
        requests_thread = threading.Thread(target=requests.post, kwargs={'url': "http://127.0.0.1:8888/run_simulation",'json': payload})
        requests_thread.start()
        # requests.post("http://127.0.0.1:8888/run_simulation",json = payload)
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
        self.Button1 = tk.Button(self.control_panel, image=self.save_icon,compound=tk.CENTER, width=45, height=30)
        self.Button1.grid(row=0, column=1, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")

        #save as Button
        self.save_as_icon = tk.PhotoImage(file="icon/save_as.png")
        self.Button1 = tk.Button(self.control_panel, image=self.save_as_icon,compound=tk.CENTER, width=60, height=30)
        self.Button1.grid(row=0, column=2, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")

        #delete Button
        self.delete_icon = tk.PhotoImage(file="icon/delete.png")
        self.Button1 = tk.Button(self.control_panel, image=self.delete_icon,compound=tk.CENTER, width=60, height=30)
        self.Button1.grid(row=0, column=3, padx=5, pady=5,)
        self.Button1.configure(bg="white",activebackground="white")



       
