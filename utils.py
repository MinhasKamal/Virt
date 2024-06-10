# Minhas Kamal (minhaskamal024@gmail.com)
# 14 Mar 24

import cv2
from PIL import ImageTk, Image

patient_file_extension: str = ".patient"
movement_file_extension: str = ".movement"

def get_scaled_imgtk(mat: cv2.typing.MatLike, scaled_height: int) -> ImageTk.PhotoImage:
    resting_pose_img: Image.Image = Image.fromarray(cv2.cvtColor(mat, cv2.COLOR_BGR2RGBA))
    resting_pose_img = resting_pose_img.resize((
        int(resting_pose_img.width*scaled_height/resting_pose_img.height),
        scaled_height))
    resting_pose_imgtk: ImageTk.PhotoImage = ImageTk.PhotoImage(image=resting_pose_img)

    return resting_pose_imgtk

