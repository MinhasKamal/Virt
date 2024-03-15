# Minhas Kamal (minhaskamal024@gmail.com)
# 09 Mar 24

import tkinter as tk
from tkinter import messagebox
import movement
import homeView
import jointSelectorView
import poseCapturerView
import previewMovementView


def main():
    ui = tk.Tk()
    ui.title("Virt")
    ui.geometry("+0+0")
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#ffffff")

    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")

    doctor_movement = movement.Movement()
    
    operation_option = tk.StringVar(view_frame, "0")
    action_button = tk.Button(
        ui,
        text="Ok",
        command=lambda:
        action_button_command(
            action_button,
            view_frame,
            doctor_movement,
            operation_option))
    action_button.pack(pady=10)

    homeView.show(view_frame, operation_option)

    ui.mainloop()
    return 0


def action_button_command(
        action_button, view_frame,
        doctor_movement: movement.Movement, operation_option):
    
    if view_frame.name == "homeView":
        if operation_option.get() == '1':
            clear_view_frame(view_frame)
            jointSelectorView.show(view_frame, doctor_movement)
            action_button.config(text="Next 1")
        elif operation_option.get() == '2':
            print(operation_option)
        else:
            print(operation_option.get())

    elif view_frame.name == "jointSelectorView":
        clear_view_frame(view_frame)
        poseCapturerView.show(view_frame, doctor_movement)
        action_button.config(text="Next 2")

    elif view_frame.name == "poseCapturerView":
        if doctor_movement.resting_pose_image is not None and \
                    doctor_movement.flexing_pose_image is not None:
            clear_view_frame(view_frame)
            previewMovementView.show(view_frame, doctor_movement)
            action_button.config(text="Save")

    elif view_frame.name == "saveMovementView":
        
        doctor_movement.save()
        messagebox.showinfo("Saved", "New movement \"" +
                            doctor_movement.name + "\" is created.")
        clear_view_frame(view_frame)
        homeView.show(view_frame, operation_option)
        action_button.config(text="Ok")

    else:
        action_button.config(background="#ff0000")

    return 0


def clear_view_frame(view_frame):
    for component in view_frame.winfo_children():
        component.destroy()

    return



main()
