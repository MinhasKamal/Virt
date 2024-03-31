# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import cv2
from PIL import ImageTk, Image
import mediapipe as mp
import movement
import poseFeedbacker
import landmarkDrawer

class PoseCapturerView:
    _pose = mp.solutions.pose.Pose(
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.75,
        model_complexity = 2,
        smooth_landmarks = True
    )

    _stream_label: tk.Label
    _feedback_label: tk.Label
    _timer_label: tk.Label

    _waiting_time: int = 5

    camera: cv2.VideoCapture

    _landmark_drawer: landmarkDrawer.LandmarkDrawer

    @classmethod
    def show(cls, view_frame: tk.Frame, doctor_movement: movement.Movement) -> None:
        view_frame.name = cls.__name__

        prompt_label = tk.Label(
            view_frame,
            text="Press capture when you are ready")
        prompt_label.pack(pady=10)

        cls._stream_label = tk.Label(view_frame)
        cls._stream_label.mat = None
        cls._stream_label.isstreaming = False
        cls._stream_label.pack()

        cls._feedback_label = tk.Label(
            view_frame,
            bg='#ff0',
            fg='#f00',
            font=('Arial', 18))
        cls._feedback_label.isvisible = False

        cls._timer_label = tk.Label(
            view_frame,
            bg='#fff',
            fg='#0f0',
            font=('Arial', 38))
        cls._timer_label.waiting_time = cls._waiting_time + 1
        cls._timer_label.isvisible = False

        capture_button = tk.Button(
            view_frame,
            text="Capture movement",
            command=lambda: cls._capture_image(
                doctor_movement,
                prompt_label,
                capture_button))
        capture_button.pack(pady=10)

        cls._landmark_drawer = landmarkDrawer.LandmarkDrawer(doctor_movement)
        cls._start_streaming(doctor_movement)

        return
    
    @classmethod
    def _start_streaming(cls, doctor_movement):
        cls.camera = cv2.VideoCapture(0)
        cls._stream_label.isstreaming = True
        cls._run_streaming(cls._landmark_drawer, doctor_movement)
        return
    
    @classmethod
    def _run_streaming(cls, landmark_drawer, doctor_movement):
        cls._stream_label.mat = cv2.flip(cls.camera.read()[1], 1)
        pose_landmarks = cls._pose.process(cls._stream_label.mat).pose_landmarks

        cls._update_frame(landmark_drawer, pose_landmarks)
        cls._update_feedback(poseFeedbacker.PoseFeedbacker.get_feedback(
            pose_landmarks, doctor_movement))
            
        if cls._stream_label.isstreaming and cls.camera.isOpened():
            cls._stream_label.after(1, lambda: cls._run_streaming(
                    landmark_drawer, doctor_movement))
        else:
            cls.camera.release()

        return

    @classmethod
    def _capture_image(cls, doctor_movement: movement.Movement, prompt_label: tk.Label,
            capture_button: tk.Button) -> None:
        capture_button['state'] = tk.DISABLED
        doctor_movement.resting_pose_image = None
        doctor_movement.flexing_pose_image = None

        if not cls._stream_label.isstreaming:
            cls._start_streaming(doctor_movement)

        prompt_label['text'] = "Get to resting pose"

        def run_countdown():
            if cls._feedback_label.isvisible:
                cls._timer_label.after(500, run_countdown)
                return
            
            if cls._timer_label.waiting_time > 1:
                cls._show_and_update_timer()
                cls._timer_label.after(1000, run_countdown)
            
            else:
                cls._hide_and_reset_timer()

                if doctor_movement.resting_pose_image is None:
                    cls._capture_resting_pose(doctor_movement, prompt_label)
                    cls._timer_label.after(3000, run_countdown)
                else:
                    cls._capture_flexing_pose(doctor_movement, prompt_label)
                    cls._stream_label.isstreaming = False
                    capture_button['text'] = "Retry"
                    capture_button['state'] = tk.NORMAL

        run_countdown()
        return
    
    @classmethod
    def _update_frame(cls, landmark_drawer: landmarkDrawer.LandmarkDrawer, pose_landmarks) -> None:
        mat_with_joint = landmark_drawer.draw(cls._stream_label.mat, pose_landmarks)
        img = Image.fromarray(cv2.cvtColor(mat_with_joint, cv2.COLOR_BGR2RGBA))
        cls._stream_label.imgtk = ImageTk.PhotoImage(image=img)
        cls._stream_label.configure(image=cls._stream_label.imgtk)

    @classmethod
    def _update_feedback(cls, feedback: str) -> None:
        if feedback:
            if not cls._feedback_label.isvisible:
                cls._hide_and_reset_timer()
                cls._feedback_label.place(relx=.5, rely=.5, anchor="center")
                cls._feedback_label.isvisible = True

            cls._feedback_label.configure(text=feedback)
        else:
            if cls._feedback_label.isvisible:
                cls._feedback_label.place_forget()
                cls._feedback_label.isvisible = False
        return
    
    @classmethod
    def _show_and_update_timer(cls) -> None:
        if not cls._timer_label.isvisible:
            cls._timer_label.place(relx=.5, rely=.5, anchor="center")
            cls._timer_label.isvisible = True

        cls._timer_label.waiting_time -= 1
        cls._timer_label['text'] = str(cls._timer_label.waiting_time)
        return
    
    @classmethod
    def _hide_and_reset_timer(cls) -> None:
        if cls._timer_label.isvisible:
            cls._timer_label.place_forget()
            cls._timer_label.waiting_time = cls._waiting_time + 1
            cls._timer_label.isvisible = False
        return
    
    @classmethod
    def _capture_resting_pose(cls, doctor_movement: movement.Movement, prompt_label: tk.Label):
        doctor_movement.resting_pose_image = cls._stream_label.mat
        doctor_movement.resting_pose_joint_coordinates = \
            cls._calc_joints_in_3d_coord(cls._stream_label.mat)
        prompt_label['text'] = "Resting pose is captured, flex now"
        return
    
    @classmethod
    def _capture_flexing_pose(cls, doctor_movement: movement.Movement, prompt_label: tk.Label):
        doctor_movement.flexing_pose_image = cls._stream_label.mat
        doctor_movement.flexing_pose_joint_coordinates = \
            cls._calc_joints_in_3d_coord(cls._stream_label.mat)
        prompt_label['text'] = "Flexing pose is also captured, press next"
        return

    @classmethod
    def _calc_joints_in_3d_coord(cls, img):
        pose_landmarks = cls._pose.process(img).pose_landmarks

        joints_in_3d_coord = None
        if pose_landmarks:
            joints_in_3d_coord = pose_landmarks.landmark

        return joints_in_3d_coord

# test
if __name__ == "__main__":
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#0f0")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    doctor_movement = movement.Movement.from_file("res/test")
    PoseCapturerView.show(view_frame, doctor_movement)
    ui.mainloop()
    # print(doctor_movement)
