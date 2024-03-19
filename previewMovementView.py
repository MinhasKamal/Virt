# Minhas Kamal (minhaskamal024@gmail.com)
# 14 Mar 24

import tkinter as tk
import jointSelectorView
import movement
import utils

class PreviewMovementView:
    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement):
        view_frame.name = cls.__name__

        tk.Label(
            view_frame,
            text="Preview").pack(
                pady=(10, 0))

        preview_frame = tk.Frame(view_frame)

        joint_selector_frame = tk.Frame(preview_frame)
        jointSelectorView.JointSelectorView.show(joint_selector_frame, doctor_movement)
        joint_selector_frame.pack(side=tk.LEFT, padx=10)

        resting_pose_label = tk.Label(preview_frame)
        if doctor_movement.resting_pose_image is not None:
            resting_pose_imgtk = utils.get_scaled_imgtk(doctor_movement.resting_pose_image, 220)
            resting_pose_label.imgtk = resting_pose_imgtk
            resting_pose_label.configure(image=resting_pose_imgtk)
        else:
            resting_pose_label.configure(text='No resting pose')
        resting_pose_label.pack(padx=10)

        flexing_pose_label = tk.Label(preview_frame)
        if doctor_movement.flexing_pose_image is not None:
            flexing_pose_imgtk = utils.get_scaled_imgtk(doctor_movement.flexing_pose_image, 220)
            flexing_pose_label.imgtk = flexing_pose_imgtk
            flexing_pose_label.configure(image=flexing_pose_imgtk)
        else:
            flexing_pose_label.configure(text='No flexing pose')
        flexing_pose_label.pack(padx=10)

        preview_frame.pack(pady=(0, 5))

        input_frame = tk.Frame(view_frame)

        tk.Label(
            input_frame,
            text="Name of movement").pack(
                side=tk.LEFT,
                pady=5)

        name_of_movement_entry = tk.Entry(input_frame)
        name_of_movement_entry.insert(0, str(doctor_movement.name))
        name_of_movement_entry.pack(side=tk.LEFT, pady=5)
        name_of_movement_entry.bind(
            '<KeyRelease>', lambda 
                event,
                name_of_movement_entry=name_of_movement_entry,
                doctor_movement=doctor_movement:
                cls.__record_movement_name(name_of_movement_entry, doctor_movement))
        
        tk.Label(
            input_frame,
            text="Number of repeates").pack(
                side=tk.LEFT,
                padx=(10, 0),
                pady=5)
        
        number_of_repeats_entry = tk.Entry(input_frame)
        number_of_repeats_entry.insert(0, str(doctor_movement.repeat))
        number_of_repeats_entry.pack(side=tk.LEFT, pady=5)
        number_of_repeats_entry.bind(
            '<KeyRelease>', lambda 
                event,
                number_of_repeats_entry=number_of_repeats_entry,
                doctor_movement=doctor_movement:
                cls.__record_movement_repeat(number_of_repeats_entry, doctor_movement))

        input_frame.pack(pady=(5, 0))

        return

    @classmethod
    def __record_movement_name(cls, name_of_movement_entry, doctor_movement: movement.Movement):
        doctor_movement.name = name_of_movement_entry.get()

        return

    @classmethod
    def __record_movement_repeat(cls, number_of_repeats_entry, doctor_movement: movement.Movement):
        doctor_movement.repeat = number_of_repeats_entry.get()

        return


def __test():
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#ffffff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    doctor_movement = movement.Movement.from_file("res/test")
    PreviewMovementView.show(view_frame, doctor_movement)
    ui.mainloop()
    print(doctor_movement)

# __test()
