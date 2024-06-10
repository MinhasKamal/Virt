# Minhas Kamal (minhaskamal024@gmail.com)
# 14 Mar 24

import tkinter as tk
import jointSelectorView
import movement
import utils

class PreviewMovementView:
    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement) -> None:
        view_frame.name = cls.__name__

        tk.Label(
            view_frame,
            text="Preview").pack(
                pady=(10, 0))

        preview_frame: tk.Frame = tk.Frame(view_frame)
        preview_frame.pack(pady=(0, 5))
        joint_selector_frame: tk.Frame = tk.Frame(preview_frame)
        joint_selector_frame.pack(side=tk.LEFT, padx=10)
        jointSelectorView.JointSelectorView.show(joint_selector_frame, doctor_movement)
        tk.Label(preview_frame, text="Resting pose").pack(pady=(10, 0))
        cls._load_image(preview_frame, doctor_movement.resting_pose_image)
        tk.Label(preview_frame, text="Flexing pose").pack(pady=(10, 0))
        cls._load_image(preview_frame, doctor_movement.flexing_pose_image)

        input_frame: tk.Frame = tk.Frame(view_frame)
        input_frame.pack(pady=(5, 0))
        tk.Label(
            input_frame,
            text="Name of movement").pack(
                side=tk.LEFT,
                pady=5)
        cls._create_entry(
            input_frame, doctor_movement.name, doctor_movement, cls._record_movement_name)
        tk.Label(
            input_frame,
            text="Number of repeats").pack(
                side=tk.LEFT,
                padx=(10, 0),
                pady=5)
        cls._create_entry(
            input_frame, doctor_movement.repeat, doctor_movement, cls._record_movement_repeat)

        return

    @classmethod
    def _load_image(cls, frame: tk.Frame, img) -> None:
        label: tk.Label = tk.Label(frame, borderwidth=2, relief="solid")
        if img is not None:
            label.imgtk = utils.get_scaled_imgtk(img, 180)
            label.configure(image=label.imgtk)
        else:
            label.configure(text='No pose img found')
        label.pack(padx=5)

    @classmethod
    def _create_entry(
            cls, frame: tk.Frame, value, doctor_movement: movement.Movement, record_func) -> None:
        entry: tk.Entry = tk.Entry(frame)
        entry.insert(0, str(value))
        entry.pack(side=tk.LEFT, pady=5)
        entry.bind(
            '<KeyRelease>', lambda event:
                record_func(entry, doctor_movement))

    @classmethod
    def _record_movement_name(
            cls, name_of_movement_entry: tk.Entry, doctor_movement: movement.Movement) -> None:
        doctor_movement.name = name_of_movement_entry.get()
        return

    @classmethod
    def _record_movement_repeat(
            cls, number_of_repeats_entry: tk.Entry, doctor_movement: movement.Movement) -> None:
        doctor_movement.repeat = number_of_repeats_entry.get()
        return

# test
if __name__ == "__main__":
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#fff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    doctor_movement = movement.Movement.from_file("res/RightElbow_Flexion_20240415153025")
    PreviewMovementView.show(view_frame, doctor_movement)

    button_frame = tk.Frame(ui, bg='#eee')
    button_frame.pack(pady=10)
    cancel_button = tk.Button(button_frame, text="Cancel")
    cancel_button.pack(side=tk.LEFT, padx=10)
    action_button = tk.Button(button_frame, text="Save")
    action_button.pack(side=tk.LEFT, padx=10)

    ui.mainloop()
    print(doctor_movement)
