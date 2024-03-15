# Minhas Kamal (minhaskamal024@gmail.com)
# 14 Mar 24

import tkinter as tk
import jointSelectorView
import movement
import utils


def show(view_frame: tk.Frame, doctor_movement: movement.Movement):
    view_frame.name = 'saveMovementView'

    tk.Label(
        view_frame,
        text="Preview").pack(
            pady=(10, 0))

    preview_frame = tk.Frame(view_frame)

    joint_selector_frame = tk.Frame(preview_frame)
    jointSelectorView.show(joint_selector_frame, doctor_movement)
    joint_selector_frame.pack(side=tk.LEFT, padx=10)

    resting_pose_label = tk.Label(preview_frame)
    resting_pose_imgtk = utils.get_scaled_imgtk(doctor_movement.resting_pose_image, 220)
    resting_pose_label.imgtk = resting_pose_imgtk
    resting_pose_label.configure(image=resting_pose_imgtk)
    resting_pose_label.pack(padx=10)

    flexing_pose_label = tk.Label(preview_frame)
    flexing_pose_imgtk = utils.get_scaled_imgtk(doctor_movement.flexing_pose_image, 220)
    flexing_pose_label.imgtk = flexing_pose_imgtk
    flexing_pose_label.configure(image=flexing_pose_imgtk)
    flexing_pose_label.pack(padx=10)

    preview_frame.pack(pady=(0, 5))

    input_frame = tk.Frame(view_frame)

    tk.Label(
        input_frame,
        text="Name of movement").pack(
            side=tk.LEFT,
            pady=5)

    name_of_movement = tk.Entry(input_frame)
    name_of_movement.insert(0, str(doctor_movement.name))
    name_of_movement.pack(side=tk.LEFT, pady=5)
    name_of_movement.bind(
        '<KeyRelease>', lambda 
        event,
        name_of_movement=name_of_movement,
        doctor_movement=doctor_movement:
        record_name(name_of_movement, doctor_movement))
    
    tk.Label(
        input_frame,
        text="Number of repeates").pack(
            side=tk.LEFT,
            padx=(10, 0),
            pady=5)
    
    number_of_repeats = tk.Entry(input_frame)
    number_of_repeats.insert(0, str(doctor_movement.repeat))
    number_of_repeats.pack(side=tk.LEFT, pady=5)
    number_of_repeats.bind(
        '<KeyRelease>', lambda 
        event,
        number_of_repeats=number_of_repeats,
        doctor_movement=doctor_movement:
        record_repeat(number_of_repeats, doctor_movement))

    input_frame.pack(pady=(5, 0))

    return


def record_name(name_of_movement, doctor_movement: movement.Movement):
    doctor_movement.name = name_of_movement.get()

    return


def record_repeat(number_of_repeats, doctor_movement: movement.Movement):
    doctor_movement.repeat = number_of_repeats.get()

    return
