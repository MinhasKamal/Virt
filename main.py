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

    view_frame: tk.Frame
    action_button: tk.Button
    cancel_button: tk.Button

    @classmethod
    def main(cls) -> None:
        doctor_movement = movement.Movement()

        ui = tk.Tk()
        ui.title("Virt")
        ui.geometry("+0+0")
        ui.option_add("*Font", ('Arial', 12))
        ui.option_add("*Background", "#fff")

        cls.view_frame = tk.Frame(ui)
        cls.view_frame.name = ""
        cls.view_frame.pack(fill="both")

        button_frame = tk.Frame(ui, bg='#eee')
        button_frame.pack(pady=10)

        operation_option = tk.StringVar(cls.view_frame, "0")

        cls.cancel_button = tk.Button(
            button_frame,
            command=lambda:
            cls._cancel_button_command(
                doctor_movement,
                operation_option))
        cls.cancel_button.pack(side=tk.LEFT, padx=10)

        cls.action_button = tk.Button(
            button_frame,
            command=lambda:
            cls._action_button_command(
                doctor_movement,
                operation_option))
        cls.action_button.pack(side=tk.LEFT, padx=10)

        cls._load_view("Ok", "Exit", homeView.HomeView.show, operation_option)

        ui.mainloop()
        return

    @classmethod
    def _cancel_button_command(
            cls, doctor_movement: movement.Movement, operation_option: tk.StringVar) -> None:
        
        if cls.view_frame.name == homeView.HomeView.__name__:
            cls.view_frame.quit()
            return
        elif cls.view_frame.name == poseCapturerView.PoseCapturerView.__name__:
            if poseCapturerView.PoseCapturerView.camera.isOpened():
                poseCapturerView.PoseCapturerView.camera.release()
                
        cls._load_view("Ok", "Exit", homeView.HomeView.show, operation_option)

        return

    @classmethod
    def _action_button_command(
            cls, doctor_movement: movement.Movement, operation_option: tk.StringVar) -> None:
        
        if cls.view_frame.name == homeView.HomeView.__name__:
            if operation_option.get() == '1':
                cls._load_view("Next 1", "Cancel", jointSelectorView.JointSelectorView.show,
                               doctor_movement)
            elif operation_option.get() == '2':
                cls._load_view("Open", "Cancel", openFileView.OpenFileView.show,
                               doctor_movement)
            else:
                print(operation_option.get())

        elif cls.view_frame.name == jointSelectorView.JointSelectorView.__name__:
            cls._load_view("Next 2", "Cancel", poseCapturerView.PoseCapturerView.show,
                           doctor_movement)

        elif cls.view_frame.name == poseCapturerView.PoseCapturerView.__name__:
            if doctor_movement.resting_pose_image is not None and \
                        doctor_movement.flexing_pose_image is not None:
                cls._load_view("Save", "Cancel", previewMovementView.PreviewMovementView.show,
                           doctor_movement)

        elif cls.view_frame.name == previewMovementView.PreviewMovementView.__name__:
            if cls.action_button.cget("text") == "Save":
                doctor_movement.save()
                messagebox.showinfo("Saved", "New movement \"" +
                                    doctor_movement.name + "\" is created.")
            
            cls._load_view("Ok", "Exit", homeView.HomeView.show, operation_option)

        elif cls.view_frame.name == openFileView.OpenFileView.__name__:
            if doctor_movement.file_path:
                doctor_movement = movement.Movement.from_file(doctor_movement.file_path)
                cls._load_view("Ok", "Cancel", previewMovementView.PreviewMovementView.show,
                           doctor_movement)

        else:
            cls.action_button.config(bg="#f00")

        return

    @classmethod
    def _load_view(
            cls, action_button_text: str, cancel_button_text: str,
            show_func, show_func_arg) -> None:
        cls._clear_view_frame(cls.view_frame)
        cls.action_button['text'] = action_button_text
        cls.cancel_button['text'] = cancel_button_text
        show_func(cls.view_frame, show_func_arg)

    @classmethod
    def _clear_view_frame(cls, view_frame: tk.Frame) -> None:
        for component in view_frame.winfo_children():
            component.destroy()
        return


if __name__ == "__main__":
    Main.main()
