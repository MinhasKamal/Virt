# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import cv2
from PIL import ImageTk, Image
import mediapipe as mp
import movement
import types


def show(view_frame: tk.Frame, doctor_movement: movement.Movement):
    view_frame.name = 'poseCapturerView'
    doctor_movement.resting_pose_image = None
    doctor_movement.flexing_pose_image = None

    prompt_label = tk.Label(
        view_frame,
        text="Your full body should be visible")
    prompt_label.pack(pady=10)

    camera = cv2.VideoCapture(0)
    pose = mp.solutions.pose.Pose(
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.75,
        model_complexity = 2,
        smooth_landmarks = True
    )

    stream_label = tk.Label(view_frame)
    stream_label.pack()

    timer_label = tk.Label(view_frame, font=('Arial', 38))
    
    frame = types.SimpleNamespace()
    frame.mat = None
    frame.is_run_video_stream = None
    capture_button = tk.Button(
        view_frame,
        text="Capture movement",
        command=lambda: capture_image(
            doctor_movement, 
            frame, 
            prompt_label, 
            timer_label, 
            capture_button))
    capture_button.pack(pady=10)

    def run_streaming():
        _, mat = camera.read()
        mat = cv2.flip(mat, 1)
        frame.mat = mat.copy()
        frame_joint = draw_joints_in_3d_coord_on_2d_img(mat, pose)
        img = Image.fromarray(cv2.cvtColor(frame_joint, cv2.COLOR_BGR2RGBA))
        imgtk = ImageTk.PhotoImage(image=img)
        
        stream_label.imgtk = imgtk
        stream_label.configure(image=imgtk)
        if frame.is_run_video_stream:
            stream_label.after(10, lambda:run_streaming())
        else:
            camera.release()

        return

    frame.is_run_video_stream = True
    run_streaming()

    return


def draw_joints_in_3d_coord_on_2d_img(img, pose):
    pose_landmarks = pose.process(img).pose_landmarks
    mp.solutions.drawing_utils.draw_landmarks(
        img,
        pose_landmarks,
        mp.solutions.pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
    )

    return img


def capture_image(doctor_movement: movement.Movement, frame,
                  prompt_label, timer_label, capture_button):
    capture_button['state'] = tk.DISABLED

    waiting_time = 5
    timer_label.config(text=str(waiting_time+1))

    prompt_label.config(text="Get to resting pose")

    is_resting_pose_not_captured = types.SimpleNamespace()
    is_resting_pose_not_captured.val = True
    def run_countdown():
        time = int(timer_label.cget('text'))
        
        if time > 1:
            timer_label.place(relx=.5, rely=.5, anchor="center")
            timer_label.config(text=str(time-1))
            timer_label.after(1000, run_countdown)
        
        else:
            timer_label.place_forget()

            if is_resting_pose_not_captured.val:
                doctor_movement.resting_pose_image = frame.mat
                doctor_movement.resting_pose_joint_coordinates = calc_joints_in_3d_coord(frame.mat)
                prompt_label.config(text="Resting pose is captured, flex now")
                timer_label.config(text=str(waiting_time+1))
                is_resting_pose_not_captured.val = False
                timer_label.after(3000, run_countdown)
            else:
                doctor_movement.flexing_pose_image = frame.mat
                doctor_movement.flexing_pose_joint_coordinates = calc_joints_in_3d_coord(frame.mat)
                prompt_label.config(text="Flexing pose is also captured, press next")
                frame.is_run_video_stream = False

    run_countdown()
    return


def calc_joints_in_3d_coord(img):
    pose = mp.solutions.pose.Pose(
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.75,
        model_complexity = 2,
        smooth_landmarks = True
    )
    pose_landmarks = pose.process(img).pose_landmarks
    joints_in_3d_coord = pose_landmarks.landmark
    # print(len(joints_in_3d_coord))

    return joints_in_3d_coord