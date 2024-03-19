# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import cv2
from PIL import ImageTk, Image
import mediapipe as mp
import movement
import skeleton
import types

class PoseCapturerView:
    pose = mp.solutions.pose.Pose(
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.75,
        model_complexity = 2,
        smooth_landmarks = True
    )

    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement):
        view_frame.name = cls.__name__
        doctor_movement.resting_pose_image = None
        doctor_movement.flexing_pose_image = None

        prompt_label = tk.Label(
            view_frame,
            text="Your full body should be visible")
        prompt_label.pack(pady=10)

        stream_label = tk.Label(view_frame)
        stream_label.pack()

        timer_label = tk.Label(view_frame, font=('Arial', 38))
        
        video_stream = types.SimpleNamespace()
        video_stream.mat = None
        video_stream.is_run = False
        capture_button = tk.Button(
            view_frame,
            text="Capture movement",
            command=lambda: cls.__capture_image(
                doctor_movement, 
                video_stream, 
                prompt_label, 
                timer_label, 
                capture_button))
        capture_button.pack(pady=10)

        camera = cv2.VideoCapture(0)
        def run_streaming():
            _, mat = camera.read()
            mat = cv2.flip(mat, 1)
            video_stream.mat = mat.copy()
            frame_joint = cls.__draw_joints_in_3d_coord_on_2d_img(mat, doctor_movement)
            img = Image.fromarray(cv2.cvtColor(frame_joint, cv2.COLOR_BGR2RGBA))
            imgtk = ImageTk.PhotoImage(image=img)
            
            stream_label.imgtk = imgtk
            stream_label.configure(image=imgtk)
            if video_stream.is_run:
                stream_label.after(10, lambda:run_streaming())
            else:
                camera.release()

            return

        video_stream.is_run = True
        run_streaming()

        return

    @classmethod
    def __draw_joints_in_3d_coord_on_2d_img(cls, img, doctor_movement: movement.Movement):
        tracking_joint_index_list = skeleton.Skeleton.get_mediapipe_index_list(
            doctor_movement.tracking_joint_list)
        observing_joint_index_list = skeleton.Skeleton.get_mediapipe_index_list(
            doctor_movement.observing_joint_list)
        landmark_drawing_spec = cls.__create_landmark_drawing_spec(
            tracking_joint_index_list, observing_joint_index_list)
        
        pose_landmarks = cls.pose.process(img).pose_landmarks
        # if pose_landmarks:
        #     for idx, landmark in enumerate(pose_landmarks.landmark):
        #         if idx not in tracking_joint_index_list and idx not in observing_joint_index_list:
        #             landmark.visibility = 0

        mp.solutions.drawing_utils.draw_landmarks(
            img,
            pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            landmark_drawing_spec=landmark_drawing_spec
            # landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )

        return img
    
    @classmethod
    def __create_landmark_drawing_spec(cls, tracking_joint_index_list, observing_joint_index_list):
        _RED = (0, 0, 255)
        _BLUE = (255, 0, 0)
        _WHITE = (255, 255, 255)
        _THIN = 1
        _THICK = 7

        simple_joint_spec = mp.solutions.drawing_utils.DrawingSpec(
            color=_WHITE, thickness=_THIN)
        tracking_joint_spec = mp.solutions.drawing_utils.DrawingSpec(
            color=_RED, thickness=_THICK)
        observing_joint_spec = mp.solutions.drawing_utils.DrawingSpec(
            color=_BLUE, thickness=_THICK)
        
        pose_landmark_style = {}
        for index in range(33):
            pose_landmark_style[index] = simple_joint_spec
        for index in tracking_joint_index_list:
            pose_landmark_style[index] = tracking_joint_spec
        for index in observing_joint_index_list:
            pose_landmark_style[index] = observing_joint_spec

        return pose_landmark_style

    @classmethod
    def __capture_image(cls, doctor_movement: movement.Movement, video_stream,
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
                    doctor_movement.resting_pose_image = video_stream.mat
                    doctor_movement.resting_pose_joint_coordinates = \
                        cls.__calc_joints_in_3d_coord(video_stream.mat)
                    prompt_label.config(text="Resting pose is captured, flex now")
                    timer_label.config(text=str(waiting_time+1))
                    is_resting_pose_not_captured.val = False
                    timer_label.after(3000, run_countdown)
                else:
                    doctor_movement.flexing_pose_image = video_stream.mat
                    doctor_movement.flexing_pose_joint_coordinates = \
                        cls.__calc_joints_in_3d_coord(video_stream.mat)
                    prompt_label.config(text="Flexing pose is also captured, press next")
                    video_stream.is_run = False

        run_countdown()
        return

    @classmethod
    def __calc_joints_in_3d_coord(cls, img):
        pose_landmarks = cls.pose.process(img).pose_landmarks

        joints_in_3d_coord = None
        if pose_landmarks is not None:
            joints_in_3d_coord = pose_landmarks.landmark
        # print(len(joints_in_3d_coord))

        return joints_in_3d_coord


def __test():
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#ffffff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    doctor_movement = movement.Movement.from_file("res/test")
    PoseCapturerView.show(view_frame, doctor_movement)
    ui.mainloop()
    print(doctor_movement)

# __test()
