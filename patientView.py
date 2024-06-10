# Minhas Kamal (minhaskamal024@gmail.com)
# 14 Mar 24

import tkinter as tk
from tkinter import filedialog
import patientRecord
import utils

class PatientView:
    @classmethod
    def show(cls, view_frame: tk.Frame, patient_record: patientRecord.PatientRecord) -> None:
        view_frame.name = cls.__name__

        tk.Label(
            view_frame,
            text="Patient").pack(
                pady=(10, 0))

        name_frame: tk.Frame = tk.Frame(view_frame)
        name_frame.pack(pady=(5, 0))
        tk.Label(
            name_frame,
            text="Name").pack(
                side=tk.LEFT,
                pady=5)
        cls._create_entry(
            name_frame, patient_record.name, patient_record, cls._record_patient_name)
        
        movement_file_path_frame: tk.Frame = tk.Frame(view_frame)
        movement_file_path_frame.pack(pady=(5, 0))
        tk.Label(
            movement_file_path_frame,
            text="Movement file path").pack(
                side=tk.LEFT,
                padx=(10, 0),
                pady=5)
        movement_file_path_entry = cls._create_entry(
            movement_file_path_frame, patient_record.movement_file_path,
            patient_record, cls._record_movement_file_path)
        tk.Button(
            movement_file_path_frame,
            text="Browse"
            ,command=lambda: cls._browse_file(
                view_frame,
                patient_record,
                movement_file_path_entry)).pack(
                padx=10,
                pady=10)
        
        repeat_frame: tk.Frame = tk.Frame(view_frame)
        repeat_frame.pack(pady=(5, 0))
        tk.Label(
            repeat_frame,
            text="Repeat").pack(
                side=tk.LEFT,
                padx=(10, 0),
                pady=5)
        cls._create_entry(
            repeat_frame, patient_record.repeat, patient_record, cls._record_patient_repeat)

        return

    @classmethod
    def _create_entry(
            cls, frame: tk.Frame, value, patient_record: patientRecord.PatientRecord,
            record_func) -> tk.Entry:
        entry: tk.Entry = tk.Entry(frame)
        entry.insert(0, str(value))
        entry.pack(side=tk.LEFT, pady=5)
        entry.bind(
            '<KeyRelease>', lambda event:
                record_func(entry, patient_record))
        return entry

    @classmethod
    def _record_patient_name(
            cls, name_of_movement_entry: tk.Entry, patient_record: patientRecord.PatientRecord) -> None:
        patient_record.name = name_of_movement_entry.get()
        return
    
    @classmethod
    def _record_movement_file_path(
            cls, movement_file_path_entry: tk.Entry, patient_record: patientRecord.PatientRecord) -> None:
        patient_record.movement_file_path = movement_file_path_entry.get()
        return

    @classmethod
    def _record_patient_repeat(
            cls, number_of_repeats_entry: tk.Entry, patient_record: patientRecord.PatientRecord) -> None:
        patient_record.repeat = number_of_repeats_entry.get()
        return
    
    @classmethod
    def _browse_file(cls, view_frame: tk.Frame, patient_record: patientRecord.PatientRecord,
            file_path_entry: tk.Entry) -> None:
        file = filedialog.askopenfile(
            parent=view_frame,
            title='Please select a file',
            filetypes=[('Movement file', '*' + utils.movement_file_extension)])
        if file:
            patient_record.movement_file_path = file.name[:-len(utils.movement_file_extension)]
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, patient_record.movement_file_path)
        return

# test
if __name__ == "__main__":
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#fff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    patient_record = patientRecord.PatientRecord()
    PatientView.show(view_frame, patient_record)

    button_frame = tk.Frame(ui, bg='#eee')
    button_frame.pack(pady=10)
    cancel_button = tk.Button(button_frame, text="Cancel")
    cancel_button.pack(side=tk.LEFT, padx=10)
    action_button = tk.Button(button_frame, text="Save")
    action_button.pack(side=tk.LEFT, padx=10)

    ui.mainloop()
    print(patient_record)
