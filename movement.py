# Minhas Kamal (minhaskamal024@gmail.com)
# 10 Mar 24

from datetime import datetime
import cv2
import json
import types


class Movement:

    def __init__(self) -> None:
        self.name = ""
        self.repeat = 3
        self.tracking_joint_list = []
        self.observing_joint_list = []
        self.resting_pose_joint_coordinates = []
        self.flexing_pose_joint_coordinates = []
        self.resting_pose_image = None
        self.flexing_pose_image = None
        self.file_path = ""
        return

    def __str__(self) -> str:
        string = "{\n"
        string += "\"name\" : \"" + self.name + "\",\n"
        string += "\"repeat\" : " + str(self.repeat) + ",\n"

        string += "\"tracking_joint_list\" : ["
        for tracking_joint in self.tracking_joint_list:
            string += "\"" + tracking_joint + "\","
        if self.tracking_joint_list:
            string = string[:-1] 
        string += "],\n"

        string += "\"observing_joint_list\" : ["
        for observing_joint in self.observing_joint_list:
            string += "\"" + observing_joint + "\","
        if self.observing_joint_list:
            string = string[:-1] 
        string += "],\n"

        string += "\"resting_pose_joint_coordinates\" : ["
        if self.resting_pose_joint_coordinates:
            for resting_pose_joint_coordinate in self.resting_pose_joint_coordinates:
                string += "\n{" 
                string += "\"x\":" + str(resting_pose_joint_coordinate.x)
                string += ",\"y\":" + str(resting_pose_joint_coordinate.y)
                string += ",\"z\":" + str(resting_pose_joint_coordinate.z)
                string += ",\"visibility\":" + str(resting_pose_joint_coordinate.visibility)
                string += "},"
            string = string[:-1]
        string += "],\n"

        string += "\"flexing_pose_joint_coordinates\" : ["
        if self.flexing_pose_joint_coordinates:
            for flexing_pose_joint_coordinate in self.flexing_pose_joint_coordinates:
                string += "\n{" 
                string += "\"x\":" + str(flexing_pose_joint_coordinate.x)
                string += ",\"y\":" + str(flexing_pose_joint_coordinate.y)
                string += ",\"z\":" + str(flexing_pose_joint_coordinate.z)
                string += ",\"visibility\":" + str(flexing_pose_joint_coordinate.visibility)
                string += "},"
            string = string[:-1]
        string += "]\n"

        string += "}\n"
        return string
    
    def save(self) -> None:
        file_path = "res/" + self.name + "_" + datetime.today().strftime("%Y%m%d%H%M%S")

        file = open(file_path + ".json", "w")
        file.write(str(self))
        file.close()

        cv2.imwrite(file_path + "_rest.jpg", self.resting_pose_image)
        cv2.imwrite(file_path + "_flex.jpg", self.flexing_pose_image)

        return

    @classmethod
    def from_file(cls, file_path):
        file = open(file_path + ".json", "r")
        movement_json = json.load(file)
        file.close()

        movement = cls()
        movement.file_path = file_path
        movement.name = movement_json["name"]
        movement.repeat = movement_json["repeat"]
        movement.tracking_joint_list = movement_json["tracking_joint_list"]
        movement.observing_joint_list = movement_json["observing_joint_list"]
        for resting_pose_joint_coordinate in movement_json["resting_pose_joint_coordinates"]:
            temp = types.SimpleNamespace()
            temp.x = resting_pose_joint_coordinate["x"]
            temp.y = resting_pose_joint_coordinate["y"]
            temp.z = resting_pose_joint_coordinate["z"]
            temp.visibility = resting_pose_joint_coordinate["visibility"]
            movement.resting_pose_joint_coordinates.append(temp)
        for flexing_pose_joint_coordinate in movement_json["flexing_pose_joint_coordinates"]:
            temp = types.SimpleNamespace()
            temp.x = flexing_pose_joint_coordinate["x"]
            temp.y = flexing_pose_joint_coordinate["y"]
            temp.z = flexing_pose_joint_coordinate["z"]
            temp.visibility = flexing_pose_joint_coordinate["visibility"]
            movement.flexing_pose_joint_coordinates.append(temp)

        movement.resting_pose_image = cv2.imread(file_path + "_rest.jpg")
        movement.flexing_pose_image = cv2.imread(file_path + "_flex.jpg")

        return movement


def __test():
    movement = Movement().from_file("res/test")
    print(movement)

# __test()
