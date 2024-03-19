# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import movement
import skeleton

class JointSelectorView:

    normal_color = "#ffffff"
    tracking_color = "#ff0000"
    observing_color = "#0000ff"

    joint_selection_button_properties = [
            [skeleton.Skeleton.joints[0][0], 315, 85],
            [skeleton.Skeleton.joints[1][0], 185, 85],
            [skeleton.Skeleton.joints[2][0], 395, 130],
            [skeleton.Skeleton.joints[3][0], 105, 130],
            [skeleton.Skeleton.joints[4][0], 405, 210],
            [skeleton.Skeleton.joints[5][0], 100, 210],
            [skeleton.Skeleton.joints[6][0], 315, 200],
            [skeleton.Skeleton.joints[7][0], 190, 200],
            [skeleton.Skeleton.joints[8][0], 345, 270],
            [skeleton.Skeleton.joints[9][0], 165, 270],
            [skeleton.Skeleton.joints[10][0], 327, 350],
            [skeleton.Skeleton.joints[11][0], 178, 350]
        ]

    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement):
        view_frame.name = cls.__name__

        prompt_frame = tk.Frame(view_frame)
        tk.Label(
            prompt_frame,
            text="Select joints").pack()
        tk.Label(
            prompt_frame,
            width=1,
            height=1,
            text="",
            background=cls.tracking_color).pack(
                side=tk.LEFT)
        tk.Label(
            prompt_frame,
            text="Tracking",
            foreground=cls.tracking_color).pack(
                side=tk.LEFT,
                padx=(0, 20))
        tk.Label(
            prompt_frame,
            width=1,
            height=1,
            background=cls.observing_color).pack(
                side=tk.LEFT)
        tk.Label(
            prompt_frame,
            text="Observing",
            foreground=cls.observing_color).pack(
                side=tk.LEFT)
        prompt_frame.pack(pady=10)

        model_frame = tk.Frame(
            view_frame,
            width=500,
            height=400)
        global model_img
        model_img = tk.PhotoImage(file="res/model.png").subsample(2, 2)
        tk.Label(
            model_frame,
            image=model_img).place(
                x=0, 
                y=0, 
                width=500, 
                height=400)
        for property in cls.joint_selection_button_properties:
            cls.__create_joint_selection_button(
                model_frame,
                doctor_movement,
                text=property[0],
                x=property[1],
                y=property[2])
        model_frame.pack()

        return

    @classmethod
    def __create_joint_selection_button(
            cls, model_frame, doctor_movement: movement.Movement, text, x, y):
        
        button = tk.Button(model_frame, text=text, font=('Arial', 10))
        if text in doctor_movement.tracking_joint_list:
            button.config(background=cls.tracking_color)
        elif text in doctor_movement.observing_joint_list:
            button.config(background=cls.observing_color)
        button.config(
            command=lambda button=button:
                cls.__joint_selection_button_command(button, doctor_movement))
        button.place(x=x, y=y, anchor="center")

        return

    @classmethod
    def __joint_selection_button_command(
            cls, button: tk.Button, doctor_movement: movement.Movement):
        
        joint_name = button.cget('text')

        if button.cget('bg') == cls.normal_color:
            button.config(background=cls.tracking_color)
            doctor_movement.tracking_joint_list.append(joint_name)
        elif button.cget('bg') == cls.tracking_color:
            button.config(background=cls.observing_color)
            doctor_movement.tracking_joint_list.remove(joint_name)
            doctor_movement.observing_joint_list.append(joint_name)
        else:
            button.config(background=cls.normal_color)
            doctor_movement.observing_joint_list.remove(joint_name)

        return


def __test():
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#ffffff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    doctor_movement = movement.Movement()
    JointSelectorView.show(view_frame, doctor_movement)
    ui.mainloop()
    print(doctor_movement)

# __test()
