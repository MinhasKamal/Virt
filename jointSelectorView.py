# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import movement


tracking_color = "#ff0000"
observing_color = "#0000ff"


def show(view_frame: tk.Frame, doctor_movement: movement.Movement):
    view_frame.name = 'jointSelectorView'

    prompt_frame = tk.Frame(view_frame)
    tk.Label(
        prompt_frame,
        text="Select joints").pack()
    tk.Label(
        prompt_frame,
        width=1,
        height=1,
        text="",
        background=tracking_color).pack(
            side=tk.LEFT)
    tk.Label(
        prompt_frame,
        text="Tracking",
        foreground=tracking_color).pack(
            side=tk.LEFT,
            padx=(0, 20))
    tk.Label(
        prompt_frame,
        width=1,
        height=1,
        background=observing_color).pack(
            side=tk.LEFT)
    tk.Label(
        prompt_frame,
        text="Observing",
        foreground=observing_color).pack(
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
    
    create_joint_selection_button(model_frame, doctor_movement, text="wr", x=385, y=200)
    create_joint_selection_button(model_frame, doctor_movement, text="wl", x=90, y=200)
    create_joint_selection_button(model_frame, doctor_movement, text="er", x=370, y=110)
    create_joint_selection_button(model_frame, doctor_movement, text="el", x=105, y=110)
    create_joint_selection_button(model_frame, doctor_movement, text="sr", x=300, y=75)
    create_joint_selection_button(model_frame, doctor_movement, text="sl", x=180, y=75)
    create_joint_selection_button(model_frame, doctor_movement, text="hr", x=300, y=190)
    create_joint_selection_button(model_frame, doctor_movement, text="hl", x=180, y=190)
    create_joint_selection_button(model_frame, doctor_movement, text="kr", x=330, y=260)
    create_joint_selection_button(model_frame, doctor_movement, text="kl", x=150, y=260)
    create_joint_selection_button(model_frame, doctor_movement, text="ar", x=310, y=350)
    create_joint_selection_button(model_frame, doctor_movement, text="al", x=170, y=350)

    model_frame.pack()

    return


def create_joint_selection_button(model_frame, doctor_movement: movement.Movement, text, x, y):
    button = tk.Button(model_frame, text=text, font=('Arial', 10))
    if text in doctor_movement.tracking_joint_list:
        button.config(background=tracking_color)
    elif text in doctor_movement.observing_joint_list:
        button.config(background=observing_color)
    button.config(
        command=lambda button=button:
            joint_selection_button_command(button, doctor_movement))
    button.place(x=x, y=y)

    return


def joint_selection_button_command(button, doctor_movement: movement.Movement):
    joint_name = button.cget('text')

    if button.cget('bg') == "#ffffff":
        button.config(background=tracking_color)
        doctor_movement.tracking_joint_list.append(joint_name)
    elif button.cget('bg') == tracking_color:
        button.config(background=observing_color)
        doctor_movement.tracking_joint_list.remove(joint_name)
        doctor_movement.observing_joint_list.append(joint_name)
    else:
        button.config(background="#ffffff")
        doctor_movement.observing_joint_list.remove(joint_name)

    return
