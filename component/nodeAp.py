import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox

class NodeAP(tb.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master