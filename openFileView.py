# Minhas Kamal (minhaskamal024@gmail.com)
# 19 Mar 24

import tkinter as tk
from tkinter import filedialog
import movement

class OpenFileView:
    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement):
        view_frame.name = cls.__name__

        tk.Label(
            view_frame,
            text="Select file").pack(
                padx=10,
                pady=10)

        file_path_entry = tk.Entry(view_frame)
        file_path_entry.insert(0, doctor_movement.file_path)
        file_path_entry.pack(
                padx=10,
                pady=10)
        file_path_entry.bind(
            '<KeyRelease>',
            lambda 
                event,
                file_path_entry=file_path_entry,
                doctor_movement=doctor_movement:
                cls.__record_file_path(file_path_entry, doctor_movement))
        
        tk.Button(
            view_frame,
            text="Browse"
            ,command=lambda: cls.__browse_file(
                view_frame,
                doctor_movement,
                file_path_entry)).pack(
                padx=10,
                pady=10)
        

        return

    @classmethod
    def __browse_file(cls, view_frame, doctor_movement, file_path_entry):
        file = filedialog.askopenfile(
            parent=view_frame,
            title='Please select a file',
            filetypes=[('Movement model', '*.json')])
        if file:
            doctor_movement.file_path = file.name[:-5]
            file_path_entry.insert(0, doctor_movement.file_path)
        return


    @classmethod
    def __record_file_path(cls, file_path_entry, doctor_movement: movement.Movement):
        doctor_movement.file_path = file_path_entry.get()

        return

def __test():
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#ffffff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    OpenFileView.show(view_frame)
    ui.mainloop()

# __test()
