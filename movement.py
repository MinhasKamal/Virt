# Minhas Kamal (minhaskamal024@gmail.com)
# 10 Mar 24

from datetime import datetime
import cv2


class Movement:
    name = ""
    repeat = 3
    tracking_joint_list = []
    observing_joint_list = []
    resting_pose_joint_coordinates = []
    flexing_pose_joint_coordinates = []
    resting_pose_image = None
    flexing_pose_image = None

    def __init__(self):
        return

    def __str__(self):
        string = "{\n"
        string += "\"name\" : \"" + self.name + "\",\n"
        string += "\"repeat\" : " + str(self.repeat) + ",\n"

        string += "\"tracking_joint_list\" : ["
        for tracking_joint in self.tracking_joint_list:
            string += "\"" + tracking_joint + "\","
        string += "],\n"

        string += "\"observing_joint_list\" : ["
        for observing_joint in self.observing_joint_list:
            string += "\"" + observing_joint + "\","
        string += "],\n"

        string += "\"resting_pose_joint_coordinates\" : ["
        for resting_pose_joint_coordinate in self.resting_pose_joint_coordinates:
            string += "\n{" 
            string += "\"x\":" + str(resting_pose_joint_coordinate.x)
            string += ",\"y\":" + str(resting_pose_joint_coordinate.y)
            string += ",\"z\":" + str(resting_pose_joint_coordinate.z)
            string += ",\"visibility\":" + str(resting_pose_joint_coordinate.visibility)
            string += "},"
        string += "],\n"

        string += "\"flexing_pose_joint_coordinates\" : ["
        for flexing_pose_joint_coordinate in self.flexing_pose_joint_coordinates:
            string += "\n{" 
            string += "\"x\":" + str(flexing_pose_joint_coordinate.x)
            string += ",\"y\":" + str(flexing_pose_joint_coordinate.y)
            string += ",\"z\":" + str(flexing_pose_joint_coordinate.z)
            string += ",\"visibility\":" + str(flexing_pose_joint_coordinate.visibility)
            string += "},"
        string += "],\n"

        string += "}\n"
        return string
    
    def save(self):
        file_path = "res/" + self.name + "_" + datetime.today().strftime('%Y%m%d%H%M%S')

        file = open(file_path + ".json", "w")
        file.write(str(self))
        file.close()

        cv2.imwrite(file_path + "_rest.jpg", self.resting_pose_image)
        cv2.imwrite(file_path + "_flex.jpg", self.flexing_pose_image)

        return
