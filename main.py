# Minhas Kamal (minhaskamal024@gmail.com)
# 09 Mar 24

import tkinter as tk
from tkinter import messagebox
import movement
import homeView
import jointSelectorView
import openFileView
import poseCapturerView
import previewMovementView

class Main:

    @classmethod
    def main(cls):
        ui = tk.Tk()
        ui.title("Virt")
        ui.geometry("+0+0")
        ui.option_add("*Font", ('Arial', 12))
        ui.option_add("*Background", "#ffffff")

        view_frame = tk.Frame(ui)
        view_frame.pack(fill="both")

        doctor_movement = movement.Movement()
        operation_option = tk.StringVar(view_frame, "0")
        
        button_frame = tk.Frame(ui, background='#eeeeee')
        cancel_button = tk.Button(
            button_frame,
            text="Exit",
            command=lambda:
            cls.__cancel_button_command(
                action_button,
                cancel_button,
                view_frame,
                doctor_movement,
                operation_option))
        cancel_button.pack(side=tk.LEFT, padx=10)
        action_button = tk.Button(
            button_frame,
            text="Ok",
            command=lambda:
            cls.__action_button_command(
                action_button,
                cancel_button,
                view_frame,
                doctor_movement,
                operation_option))
        action_button.pack(side=tk.LEFT, padx=10)
        button_frame.pack(pady=10)


        homeView.HomeView.show(view_frame, operation_option)

        ui.mainloop()
        return 0

    @classmethod
    def __cancel_button_command(
            cls, action_button, cancel_button, view_frame,
            doctor_movement: movement.Movement, operation_option):
        
        if view_frame.name == homeView.HomeView.__name__:
            view_frame.quit()
            return
        elif view_frame.name == poseCapturerView.PoseCapturerView.__name__:
            if doctor_movement.resting_pose_image is None or \
                        doctor_movement.flexing_pose_image is None:
                return
                
        cls.__clear_view_frame(view_frame)
        homeView.HomeView.show(view_frame, operation_option)
        action_button.config(text="Ok")
        cancel_button.config(text="Exit")

        return

    @classmethod
    def __action_button_command(
            cls, action_button, cancel_button, view_frame,
            doctor_movement: movement.Movement, operation_option):
        
        cancel_button.config(text="Cancel")

        if view_frame.name == homeView.HomeView.__name__:
            if operation_option.get() == '1':
                cls.__clear_view_frame(view_frame)
                jointSelectorView.JointSelectorView.show(view_frame, doctor_movement)
                action_button.config(text="Next 1")
            elif operation_option.get() == '2':
                cls.__clear_view_frame(view_frame)
                openFileView.OpenFileView.show(view_frame, doctor_movement)
                action_button.config(text="Open")
            else:
                print(operation_option.get())

        elif view_frame.name == jointSelectorView.JointSelectorView.__name__:
            cls.__clear_view_frame(view_frame)
            poseCapturerView.PoseCapturerView.show(view_frame, doctor_movement)
            action_button.config(text="Next 2")

        elif view_frame.name == poseCapturerView.PoseCapturerView.__name__:
            if doctor_movement.resting_pose_image is not None and \
                        doctor_movement.flexing_pose_image is not None:
                cls.__clear_view_frame(view_frame)
                previewMovementView.PreviewMovementView.show(view_frame, doctor_movement)
                action_button.config(text="Save")

        elif view_frame.name == previewMovementView.PreviewMovementView.__name__:
            if operation_option.get() == '1':
                doctor_movement.save()
                messagebox.showinfo("Saved", "New movement \"" +
                                    doctor_movement.name + "\" is created.")
            
            cls.__clear_view_frame(view_frame)
            homeView.HomeView.show(view_frame, operation_option)
            action_button.config(text="Ok")
            cancel_button.config(text="Exit")

        elif view_frame.name == openFileView.OpenFileView.__name__:
            if doctor_movement.file_path:
                cls.__clear_view_frame(view_frame)
                doctor_movement = movement.Movement.from_file(doctor_movement.file_path)
                previewMovementView.PreviewMovementView.show(view_frame, doctor_movement)
                action_button.config(text="Ok")

        else:
            action_button.config(background="#ff0000")

        return 0

    @classmethod
    def __clear_view_frame(cls, view_frame):
        for component in view_frame.winfo_children():
            component.destroy()

        return



Main.main()
