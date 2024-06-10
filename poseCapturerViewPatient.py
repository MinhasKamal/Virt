# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import tkinter as tk
import cv2
from PIL import ImageTk, Image
import mediapipe as mp
import poseFeedbacker
import landmarkDrawer
import utils
import patientRecord
from datetime import datetime

class PoseCapturerViewPatient:
    _pose = mp.solutions.pose.Pose(
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.75,
        model_complexity = 2,
        smooth_landmarks = True
    )

    _stream_label: tk.Label
    _feedback_label: tk.Label
    _timer_label: tk.Label

    _countdown_time: int = 3
    _interval_time: int = 3

    camera: cv2.VideoCapture

    _landmark_drawer: landmarkDrawer.LandmarkDrawer

    @classmethod
    def show(cls, view_frame: tk.Frame, patient_record: patientRecord.PatientRecord) -> None:
        view_frame.name = cls.__name__

        prompt_label = tk.Label(view_frame)
        prompt_label.pack(pady=5)

        movement_frame: tk.Frame = tk.Frame(view_frame)
        movement_frame.pack()

        preview_frame: tk.Frame = tk.Frame(movement_frame)
        preview_frame.pack(side=tk.LEFT, pady=(0, 5))

        preview_label: tk.Label = tk.Label(preview_frame, text="Follow the pose")
        preview_label.pack(padx=10)

        preview_label: tk.Label = tk.Label(preview_frame, borderwidth=2, relief="solid")
        preview_label.pack(padx=10)
        cls._load_image(preview_label, patient_record.assigned_movement.resting_pose_image)

        repeat_label: tk.Label = tk.Label(preview_frame, font=('Arial', 20))
        repeat_label.pack()
        repeat_label.value = 0

        stream_frame: tk.Frame = tk.Frame(movement_frame)
        stream_frame.pack(pady=(0, 5))

        cls._stream_label = tk.Label(stream_frame)
        cls._stream_label.mat = None
        cls._stream_label.isstreaming = False
        cls._stream_label.pack()

        cls._feedback_label = tk.Label(
            stream_frame,
            bg='#ff0',
            fg='#f00',
            font=('Arial', 18))
        cls._feedback_label.isvisible = False

        cls._timer_label = tk.Label(
            stream_frame,
            bg='#fff',
            fg='#f0f',
            font=('Arial', 38))
        cls._timer_label.waiting_time = cls._countdown_time + 1
        cls._timer_label.isvisible = False

        retry_button = tk.Button(
            view_frame,
            text="Retry",
            state=tk.DISABLED,
            command=lambda: cls._capture_image(
                patient_record,
                prompt_label,
                preview_label,
                repeat_label,
                retry_button))
        retry_button.pack(pady=10)

        cls._landmark_drawer = landmarkDrawer.LandmarkDrawer(patient_record.assigned_movement)
        cls._start_streaming(
            patient_record, prompt_label, preview_label, repeat_label, retry_button)

        return

    @classmethod
    def _start_streaming(cls, patient_record: patientRecord.PatientRecord,
                prompt_label, preview_label, repeat_label, retry_button):
        cls.camera = cv2.VideoCapture(0)
        cls._stream_label.isstreaming = True
        cls._run_streaming(patient_record.assigned_movement)
        cls._capture_image(patient_record, prompt_label, preview_label, repeat_label, retry_button)
        return

    @classmethod
    def _run_streaming(cls, doctor_movement):
        cls._stream_label.mat = cv2.flip(cls.camera.read()[1], 1)
        pose_landmarks = cls._pose.process(cls._stream_label.mat).pose_landmarks

        cls._update_frame(cls._landmark_drawer, pose_landmarks)
        cls._update_feedback(poseFeedbacker.PoseFeedbacker.get_feedback(
            pose_landmarks, doctor_movement))

        if cls._stream_label.isstreaming and cls.camera.isOpened():
            cls._stream_label.after(1, lambda: cls._run_streaming(doctor_movement))
        else:
            cls.camera.release()

        return

    @classmethod
    def _capture_image(cls, patient_record: patientRecord.PatientRecord, prompt_label: tk.Label,
            preview_label, repeat_label, retry_button: tk.Button) -> None:
        retry_button['state'] = tk.DISABLED
        patient_record.resting_pose_images.clear()
        patient_record.flexing_pose_images.clear()
        patient_record.dates.append(datetime.today().strftime("%Y%m%d%H%M%S"))

        if not cls._stream_label.isstreaming:
            cls._start_streaming(
                patient_record, prompt_label, preview_label, repeat_label, retry_button)

        prompt_label['text'] = "Get to resting pose"
        repeat_label.value = 1
        repeat_label['text'] = f"Repeat: {repeat_label.value} / {patient_record.repeat}"

        def run_countdown():
            if cls._feedback_label.isvisible:
                cls._timer_label.after(500, run_countdown)
                return

            if cls._timer_label.waiting_time > 1:
                cls._show_and_update_timer()
                cls._timer_label.after(1000, run_countdown)

            else:
                cls._hide_and_reset_timer()

                if len(patient_record.resting_pose_images) < repeat_label.value:
                    cls._capture_resting_pose(patient_record)
                    prompt_label['text'] = "Resting pose is captured, flex now"
                    cls._load_image(preview_label,
                            patient_record.assigned_movement.flexing_pose_image)
                    cls._timer_label.after(cls._interval_time * 1000, run_countdown)
                else:
                    cls._capture_flexing_pose(patient_record)

                    repeat_label.value += 1
                    repeat_label['text'] = f"Repeat: {repeat_label.value} / {patient_record.repeat}"
                    if repeat_label.value <= patient_record.repeat:
                        prompt_label['text'] = "Flexing pose is also captured, get to resting again"
                        cls._load_image(preview_label, 
                                patient_record.assigned_movement.resting_pose_image)
                        cls._timer_label.after(cls._interval_time * 1000, run_countdown)
                    else :
                        prompt_label['text'] = "Flexing pose is also captured, press next"
                        repeat_label['text'] = "Task Finished"
                        cls._stream_label.isstreaming = False
                        retry_button['state'] = tk.NORMAL

        run_countdown()
        return

    @classmethod
    def _load_image(cls, label: tk.Label, img) -> None:
        if img is not None:
            label.imgtk = utils.get_scaled_imgtk(img, 220)
            label.configure(image=label.imgtk)
        else:
            label.configure(text='No pose img found')
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
            cls._timer_label.waiting_time = cls._countdown_time + 1
            cls._timer_label.isvisible = False
        return

    @classmethod
    def _capture_resting_pose(cls, patient_record: patientRecord.PatientRecord):
        patient_record.resting_pose_images.append(cls._stream_label.mat)
        # patient_record.resting_pose_joint_coordinates = \
        #     cls._calc_joints_in_3d_coord(cls._stream_label.mat)
        return

    @classmethod
    def _capture_flexing_pose(cls, patient_record: patientRecord.PatientRecord):
        patient_record.flexing_pose_images.append(cls._stream_label.mat)
        # patient_record.flexing_pose_joint_coordinates = \
        #     cls._calc_joints_in_3d_coord(cls._stream_label.mat)
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
    ui.option_add("*Background", "#afa")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    patient_record = patientRecord.PatientRecord()
    patientRecord.PatientRecord.from_file(patient_record, "res/test_patient")
    PoseCapturerViewPatient.show(view_frame, patient_record)
    ui.mainloop()
    print(patient_record)
