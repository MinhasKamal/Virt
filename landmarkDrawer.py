# Minhas Kamal (minhaskamal024@gmail.com)
# 27 Mar 24

import mediapipe as mp
import movement
import skeleton
import cv2
import math

class LandmarkDrawer:

    def __init__(self, movement: movement.Movement) -> None:
        self._landmark_drawing_spec: dict = self._create_landmark_drawing_spec(movement)
        self._tracking_joints = skeleton.Skeleton.get_mediapipe_index_list(movement.tracking_joint_list)
        return

    def _create_landmark_drawing_spec(self, movement: movement.Movement) -> dict:
        _RED = (0, 0, 255)
        _BLUE = (255, 0, 0)
        _WHITE = (255, 255, 255)
        _THIN = 1
        _THICK = 7
        _SMALL = 1
        _LARGE = 6

        simple_joint_spec = mp.solutions.drawing_utils.DrawingSpec(
            color=_WHITE, thickness=_THIN, circle_radius=_SMALL)
        tracking_joint_spec = mp.solutions.drawing_utils.DrawingSpec(
            color=_RED, thickness=_THICK, circle_radius=_LARGE)
        observing_joint_spec = mp.solutions.drawing_utils.DrawingSpec(
            color=_BLUE, thickness=_THICK, circle_radius=_LARGE)

        pose_landmark_style = {}
        for index in range(33):
            pose_landmark_style[index] = simple_joint_spec
        for index in skeleton.Skeleton.get_mediapipe_index_list(movement.tracking_joint_list):
            pose_landmark_style[index] = tracking_joint_spec
        for index in skeleton.Skeleton.get_mediapipe_index_list(movement.observing_joint_list):
            pose_landmark_style[index] = observing_joint_spec

        return pose_landmark_style

    def draw(self, mat: cv2.typing.MatLike, pose_landmarks) -> cv2.typing.MatLike:
        if mat is None:
            return mat

        mat_with_joints = mat.copy()
        mp.solutions.drawing_utils.draw_landmarks(
            mat_with_joints,
            pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self._landmark_drawing_spec
        )
        self._draw_angles(mat_with_joints, pose_landmarks)
        return mat_with_joints

    def _draw_angles(self, mat: cv2.typing.MatLike, pose_landmarks) -> None:
        if pose_landmarks:
            for joint in self._tracking_joints:
                landmark = pose_landmarks.landmark[joint]
                if landmark.visibility > 0.5:
                    angle = skeleton.Skeleton.calc_angle(joint, pose_landmarks.landmark)
                    self._write_text(mat, landmark.x, landmark.y, str(angle))
        return

    def _write_text(self, mat: cv2.typing.MatLike, x: float, y: float, text: str) -> None:
        cv2.putText(
            mat,
            text,
            self._normalize_to_pixel_coordinates(x, y, mat),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.8,
            color = (0, 255, 0),
            thickness = 2
        )
        return

    def _normalize_to_pixel_coordinates(
            self, x: float, y: float, image: cv2.typing.MatLike) -> tuple[int, int]:
        image_rows, image_cols, _ = image.shape
        x_px = min(math.floor(x * image_cols), image_cols - 1)
        y_px = min(math.floor(y * image_rows), image_rows - 1)
        return x_px, y_px

