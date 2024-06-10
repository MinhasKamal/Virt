# Minhas Kamal (minhaskamal024@gmail.com)
# 20 Mar 24

import movement
import skeleton
import changeDetector

class PoseFeedbacker:
    _change_detector = changeDetector.ChangeDetector()

    @classmethod
    def get_feedback(cls, landmarks, movement: movement.Movement) -> str:
        feed_back = cls._check_visibility_of_related_joints(landmarks, movement)
        if not feed_back:
            feed_back = cls._check_stillness(landmarks, movement)
        return feed_back

    @classmethod
    def _check_visibility_of_related_joints(cls, landmarks, movement: movement.Movement):
        feed_back = ""

        if landmarks:
            for joint in [*movement.tracking_joint_list, *movement.observing_joint_list]:
                if landmarks.landmark[skeleton.Skeleton.get_mediapipe_index(joint)].visibility < 0.5:
                    feed_back = f"{skeleton.Skeleton.get_mediapipe_label(joint)} is not visible"
                    break
        else:
            feed_back = "Body is not detected"

        return feed_back

    @classmethod
    def _check_stillness(cls, landmarks, movement: movement.Movement):
        feed_back = ""
        if cls._change_detector.is_changing(skeleton.Skeleton.calc_angle(
                skeleton.Skeleton.get_mediapipe_index(movement.tracking_joint_list[0]),
                landmarks.landmark)):
            feed_back = "Please maintain a still pose"
        return feed_back
