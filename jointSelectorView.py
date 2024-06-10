# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import movement
import skeleton

class JointSelectorView:

    normal_color: str = "#fff"
    tracking_color: str = "#f00"
    observing_color: str = "#00f"

    joint_selection_button_properties: list[list] = [
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
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement) -> None:
        view_frame.name = cls.__name__

        prompt_frame: tk.Frame = tk.Frame(view_frame)
        prompt_frame.pack(pady=10)
        tk.Label(
            prompt_frame,
            text="Select joints").pack()
        tk.Label(
            prompt_frame,
            width=1,
            height=1,
            text="",
            bg=cls.tracking_color).pack(
                side=tk.LEFT)
        tk.Label(
            prompt_frame,
            text="Tracking",
            fg=cls.tracking_color).pack(
                side=tk.LEFT,
                padx=(0, 20))
        tk.Label(
            prompt_frame,
            width=1,
            height=1,
            bg=cls.observing_color).pack(
                side=tk.LEFT)
        tk.Label(
            prompt_frame,
            text="Observing",
            fg=cls.observing_color).pack(
                side=tk.LEFT)

        model_frame: tk.Frame = tk.Frame(
            view_frame,
            width=500,
            height=400)
        model_frame.img = tk.PhotoImage(file="res/model.png").subsample(2, 2)
        model_frame.pack()
        tk.Label(
            model_frame,
            image=model_frame.img).place(
                x=0, 
                y=0, 
                width=500, 
                height=400)
        for property in cls.joint_selection_button_properties:
            cls._create_joint_selection_button(
                model_frame,
                doctor_movement,
                text=property[0],
                x=property[1],
                y=property[2])

        return

    @classmethod
    def _create_joint_selection_button(
            cls, model_frame: tk.Frame, doctor_movement: movement.Movement,
            text: str, x: int, y: int) -> None:
        
        button = tk.Button(model_frame, text=text, font=('Arial', 10))
        if text in doctor_movement.tracking_joint_list:
            button.config(bg=cls.tracking_color)
        elif text in doctor_movement.observing_joint_list:
            button.config(bg=cls.observing_color)
        button.config(
            command=lambda:
                cls._joint_selection_button_command(button, doctor_movement))
        button.place(x=x, y=y, anchor="center")

        return

    @classmethod
    def _joint_selection_button_command(
            cls, button: tk.Button, doctor_movement: movement.Movement) -> None:
        
        joint_name: str = button.cget('text')

        if button.cget('bg') == cls.normal_color:
            button.config(bg=cls.tracking_color)
            doctor_movement.tracking_joint_list.append(joint_name)
        elif button.cget('bg') == cls.tracking_color:
            button.config(bg=cls.observing_color)
            doctor_movement.tracking_joint_list.remove(joint_name)
            doctor_movement.observing_joint_list.append(joint_name)
        else:
            button.config(bg=cls.normal_color)
            doctor_movement.observing_joint_list.remove(joint_name)

        return


# test
if __name__ == "__main__":
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#fff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    # doctor_movement = movement.Movement()
    doctor_movement = movement.Movement.from_file("res/test")
    JointSelectorView.show(view_frame, doctor_movement)
    ui.mainloop()
    print(doctor_movement)
