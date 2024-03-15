# Minhas Kamal (minhaskamal024@gmail.com)
# 13 Mar 24

import tkinter as tk

def show(view_frame: tk.Frame, operation_option: tk.StringVar):
    view_frame.name = 'homeView'

    tk.Label(
        view_frame,
        text="Select operation").pack(
            padx=10,
            pady=10)

    tk.Radiobutton(
        view_frame,
        text="Create new movement",
        value=1,
        variable=operation_option).pack(
            padx=10,
            pady=10)

    tk.Radiobutton(
        view_frame,
        text="Load movement",
        value=2,
        variable=operation_option).pack(
            padx=10,
            pady=10)

    return

