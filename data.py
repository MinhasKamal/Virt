# Minhas Kamal (minhaskamal024@gmail.com)
# 08 Mar 24

import cv2
import mediapipe as mp
import numpy as np


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
joint_neighbor_lists = [
    [16, 14, 12, 24, 26, 28],
    [15, 13, 11, 23, 25, 27],
    # [15, 13, 11, 12, 14, 16] # horizontal
]


def run():
    path_movementOne_doctor_pose1 = "res/MovementOne-Doctor-Pose1.jpg"
    path_movementOne_doctor_pose2 = "res/MovementOne-Doctor-Pose2.jpg"
    path_movementOne_patient_pose1 = "res/MovementOne-Patient-Pose1.jpg"
    path_movementOne_patient_pose2 = "res/MovementOne-Patient-Pose2.jpg"

    img_doc1 = cv2.imread(path_movementOne_doctor_pose1)
    img_doc2 = cv2.imread(path_movementOne_doctor_pose2)
    img_pat1 = cv2.imread(path_movementOne_patient_pose1)
    img_pat2 = cv2.imread(path_movementOne_patient_pose2)

    # cv2.imshow("img_pat2", cv2.resize(img, (300, 300)))
    # cv2.waitKey(0)


    # This part will be taken as an input from the doctor
    # tracking_joint_list = [23, 24, 25, 26]; # tracking both knees and hips for ROM evaluation
    # observing_joint_list = [11, 12, 13, 14]; # observing shoulder and elbow for pose verification
    
    tracking_joint_list = [14]; # tracking both knees and hips for ROM evaluation
    observing_joint_list = []; # observing shoulder and elbow for pose verification
    

    doc1_tracking_angles, doc1_observing_angles = detect_joint_and_calc_angles(
        img_doc1, tracking_joint_list, observing_joint_list)
    doc2_tracking_angles, doc2_observing_angles = detect_joint_and_calc_angles(
        img_doc2, tracking_joint_list, observing_joint_list)
    pat1_tracking_angles, pat1_observing_angles = detect_joint_and_calc_angles(
        img_pat1, tracking_joint_list, observing_joint_list)
    pat2_tracking_angles, pat2_observing_angles = detect_joint_and_calc_angles(
        img_pat2, tracking_joint_list, observing_joint_list)
    


def detect_joint_and_calc_angles(img, tracking_joint_list, observing_joint_list):
    joints_in_3d_coord = calc_joints_in_3d_coord(img)
    tracking_angle_list = calc_joint_angles(joints_in_3d_coord, tracking_joint_list)
    observing_angle_list = calc_joint_angles(joints_in_3d_coord, observing_joint_list)

    return tracking_angle_list, observing_angle_list


def calc_joint_angles(joints_in_3d_coord, joint_list):
    angle_list = []

    for joint in joint_list:
        angle_list.append(calc_angle_with_respect_to_neighbor_joints(
            joints_in_3d_coord, joint))
        
    print(angle_list)
    return angle_list


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

    # mp.solutions.drawing_utils.draw_landmarks(
    #     img,
    #     pose_landmarks,
    #     mp.solutions.pose.POSE_CONNECTIONS,
    #     landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
    # )
    # cv2.imwrite("out-pose.jpg", img)

    return joints_in_3d_coord


def calc_angle_with_respect_to_neighbor_joints(joints_in_3d_coord, joint):
    neighboring_joints = get_neighbor_joints(joint)
    # print(neighboringJoints[0], " ", joint, " ", neighboringJoints[1])
    angle_deg = calc_angle(joints_in_3d_coord[neighboring_joints[0]], 
                           joints_in_3d_coord[joint],
                           joints_in_3d_coord[neighboring_joints[1]])
    
    return angle_deg


def get_neighbor_joints(joint):
    neighbor_joints = []

    for jointNeighborList in joint_neighbor_lists:
        if(joint in jointNeighborList):
            index = jointNeighborList.index(joint)
            neighbor_joints.append(jointNeighborList[index - 1])
            neighbor_joints.append(jointNeighborList[index + 1])
            break

    return neighbor_joints


def calc_angle(a, b, c):       

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
    return np.rad2deg(angle_rad)




run()