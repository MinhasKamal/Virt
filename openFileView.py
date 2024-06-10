# Minhas Kamal (minhaskamal024@gmail.com)
# 19 Mar 24

import tkinter as tk
from tkinter import filedialog
import movement
import utils

class OpenFileView:
    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement) -> None:
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
            lambda event:
                cls._record_file_path(file_path_entry, doctor_movement))
        
        tk.Button(
            view_frame,
            text="Browse"
            ,command=lambda: cls._browse_file(
                view_frame,
                doctor_movement,
                file_path_entry)).pack(
                padx=10,
                pady=10)
        
        return

    @classmethod
    def _browse_file(cls, view_frame: tk.Frame, doctor_movement: movement.Movement,
            file_path_entry: tk.Entry) -> None:
        file = filedialog.askopenfile(
            parent=view_frame,
            title='Please select a file',
            filetypes=[('Patient file', '*' + utils.patient_file_extension)])
        if file:
            doctor_movement.file_path = file.name[:-len(utils.patient_file_extension)]
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, doctor_movement.file_path)
        return

    @classmethod
    def _record_file_path(
            cls, file_path_entry: tk.Entry, doctor_movement: movement.Movement) -> None:
        doctor_movement.file_path = file_path_entry.get()

        return


# test
if __name__ == "__main__":
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#fff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    doctor_movement = movement.Movement.from_file("res/test")
    OpenFileView.show(view_frame, doctor_movement)
    ui.mainloop()
    print(doctor_movement.file_path)
