# Minhas Kamal (minhaskamal024@gmail.com)
# 18 Mar 24

import numpy as np

class Skeleton:
    joints: list[list] = [
            ["SR", 11, "Right Shoulder"],
            ["SL", 12, "Left Shoulder"],
            ["ER", 13, "Right Elbow"],
            ["EL", 14, "Left Elbow"],
            ["WR", 15, "Right Wrist"],
            ["WL", 16, "Left Wrist"],
            ["HR", 23, "Right Hip"],
            ["HL", 24, "Left Hip"],
            ["KR", 25, "Right Knee"],
            ["KL", 26, "Left Knee"],
            ["AR", 27, "Right Ancle"],
            ["AL", 28, "Left Ancle"]
        ]

    joint_neighbor_lists: list[list[int]] = [
            [16, 14, 12, 24, 26, 28],
            [15, 13, 11, 23, 25, 27],
            # [15, 13, 11, 12, 14, 16] # horizontal
        ]

# poseLandmarkLocations = [
#     '0 - nose',
#     '1 - left eye (inner)',
#     '2 - left eye',
#     '3 - left eye (outer)',
#     '4 - right eye (inner)',
#     '5 - right eye',
#     '6 - right eye (outer)',
#     '7 - left ear',
#     '8 - right ear',
#     '9 - mouth (left)',
#     '10 - mouth (right)',
#     '11 - left shoulder',
#     '12 - right shoulder',
#     '13 - left elbow',
#     '14 - right elbow',
#     '15 - left wrist',
#     '16 - right wrist',
#     '17 - left pinky',
#     '18 - right pinky',
#     '19 - left index',
#     '20 - right index',
#     '21 - left thumb',
#     '22 - right thumb',
#     '23 - left hip',
#     '24 - right hip',
#     '25 - left knee',
#     '26 - right knee',
#     '27 - left ankle',
#     '28 - right ankle',
#     '29 - left heel',
#     '30 - right heel',
#     '31 - left foot index',
#     '32 - right foot index'
# ]

    @classmethod
    def get_mediapipe_index(cls, joint_name: str) -> int:
        for joint in cls.joints:
            if joint_name == joint[0]:
                return joint[1]
        return -1

    @classmethod
    def get_mediapipe_index_list(cls, joint_name_list: list[str]) -> list[int]:
        mediapipe_index_list: list[int] = []
        for joint_name in joint_name_list:
            mediapipe_index_list.append(cls.get_mediapipe_index(joint_name))
        return mediapipe_index_list

    @classmethod
    def get_mediapipe_label(cls, joint_name: str) -> str:
        for joint in cls.joints:
            if joint_name == joint[0]:
                return joint[2]
        return ""

    @classmethod
    def calc_joint_angles(cls, joint_list: list[int], joints_in_3d_coord) -> list[int]:
        angle_list = []
        for joint in joint_list:
            angle_list.append(cls.calc_angle_with_respect_to_neighbor_joints(
                    joint, joints_in_3d_coord))
        return angle_list

    @classmethod
    def calc_angle(cls, joint: int, joints_in_3d_coord) -> int:
        neighboring_joints = cls._get_neighboring_joints(joint)
        # print(f"{neighboring_joints[0]} {joint} {neighboring_joints[1]}")
        if neighboring_joints:
            angle_deg = cls._calc_angle_2d(
                    joints_in_3d_coord[neighboring_joints[0]],
                    joints_in_3d_coord[joint],
                    joints_in_3d_coord[neighboring_joints[1]])
        else:
            angle_deg = 0
        return angle_deg

    @classmethod
    def _get_neighboring_joints(cls, joint: int) -> list[int]:
        neighboring_joints = []
        for jointNeighborList in cls.joint_neighbor_lists:
            if(joint in jointNeighborList):
                index = jointNeighborList.index(joint)
                if index > 0 and index < len(jointNeighborList)-1:
                    neighboring_joints.append(jointNeighborList[index - 1])
                    neighboring_joints.append(jointNeighborList[index + 1])
                break
        return neighboring_joints

    @classmethod
    def _calc_angle_2d(cls, a, b, c) -> int:
        ab_vec = np.array([ a.x - b.x, a.y - b.y ])
        ab_vec_magnitude = np.sqrt(ab_vec[0] * ab_vec[0] + ab_vec[1] * ab_vec[1])
        ab_vec_normal = np.array([ ab_vec[0] / ab_vec_magnitude, ab_vec[1] / ab_vec_magnitude])

        cb_vec = np.array([ c.x - b.x, c.y - b.y ])
        cb_vec_magnitude = np.sqrt(cb_vec[0] * cb_vec[0] + cb_vec[1] * cb_vec[1])
        cb_vec_normal = np.array([ cb_vec[0] / cb_vec_magnitude, cb_vec[1] / cb_vec_magnitude])

        angle_rad = np.arccos( ab_vec_normal[0] * cb_vec_normal[0] +
                ab_vec_normal[1] * cb_vec_normal[1])
        return int(np.rad2deg(angle_rad))

    @classmethod
    def _calc_angle(cls, a, b, c) -> int:
        ab_vec = np.array([ a.x - b.x, a.y - b.y, a.z - b.z ])
        ab_vec_magnitude = np.sqrt(ab_vec[0] * ab_vec[0] + ab_vec[1] * ab_vec[1] +
                ab_vec[2] * ab_vec[2])
        ab_vec_normal = np.array([ ab_vec[0] / ab_vec_magnitude,
                ab_vec[1] / ab_vec_magnitude,
                ab_vec[2] / ab_vec_magnitude ])

        cb_vec = np.array([ c.x - b.x, c.y - b.y, c.z - b.z ])
        cb_vec_magnitude = np.sqrt(cb_vec[0] * cb_vec[0] + cb_vec[1] * cb_vec[1] +
                cb_vec[2] * cb_vec[2])
        cb_vec_normal = np.array([ cb_vec[0] / cb_vec_magnitude,
                cb_vec[1] / cb_vec_magnitude,
                cb_vec[2] / cb_vec_magnitude ])

        angle_rad = np.arccos( ab_vec_normal[0] * cb_vec_normal[0] +
                ab_vec_normal[1] * cb_vec_normal[1] +
                ab_vec_normal[2] * cb_vec_normal[2] )

        return int(np.rad2deg(angle_rad))

