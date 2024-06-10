# Minhas Kamal (minhaskamal024@gmail.com)
# 10 Mar 24

from datetime import datetime
import cv2
import json
import types
import utils

class Movement:

    def __init__(self) -> None:
        self.name: str = ""
        self.repeat: str = "3"
        self.tracking_joint_list: list[str] = []
        self.observing_joint_list: list[str] = []
        self.resting_pose_joint_coordinates: list = []
        self.flexing_pose_joint_coordinates: list = []
        self.resting_pose_image: cv2.typing.MatLike = None
        self.flexing_pose_image: cv2.typing.MatLike = None
        self.file_path: str = ""
        return

    def __str__(self) -> str:
        string: str = "{\n"
        string += f"\"name\" : \"{self.name}\",\n"
        string += f"\"repeat\" : {self.repeat},\n"
        string += f"\"tracking_joint_list\" : {json.dumps(self.tracking_joint_list)},\n"
        string += f"\"observing_joint_list\" : {json.dumps(self.observing_joint_list)},\n"
        string += f"\"resting_pose_joint_coordinates\" : \
            [{self._joint_coordinates_to_str(self.resting_pose_joint_coordinates)}],\n"
        string += f"\"flexing_pose_joint_coordinates\" : \
            [{self._joint_coordinates_to_str(self.flexing_pose_joint_coordinates)}]\n"
        string += "}\n"
        return string
    
    def _joint_coordinates_to_str(self, joint_coordinates: list) -> str:
        joint_str: str = ""
        if joint_coordinates:
            for joint_coordinate in joint_coordinates:
                joint_str += "\n{" 
                joint_str += f"\"x\":{joint_coordinate.x},"
                joint_str += f"\"y\":{joint_coordinate.y},"
                joint_str += f"\"z\":{joint_coordinate.z},"
                joint_str += f"\"visibility\":{joint_coordinate.visibility}"
                joint_str += "},"
            joint_str = joint_str[:-1]
        return joint_str
    
    def save(self) -> None:
        file_path = "res/" + self.name + "_" + datetime.today().strftime("%Y%m%d%H%M%S")
        with open(file_path + utils.movement_file_extension, "w") as file:
            file.write(str(self))

        cv2.imwrite(file_path + "_rest.jpg", self.resting_pose_image)
        cv2.imwrite(file_path + "_flex.jpg", self.flexing_pose_image)

        return

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path + utils.movement_file_extension, "r") as file:
            movement_json = json.load(file)

        movement: Movement = cls()
        movement.file_path = file_path
        movement.name = movement_json["name"]
        movement.repeat = movement_json["repeat"]
        movement.tracking_joint_list = movement_json["tracking_joint_list"]
        movement.observing_joint_list = movement_json["observing_joint_list"]
        for resting_pose_joint_coordinate in movement_json["resting_pose_joint_coordinates"]:
            movement.flexing_pose_joint_coordinates.append(
                cls._load_coordinate(resting_pose_joint_coordinate))
        for flexing_pose_joint_coordinate in movement_json["flexing_pose_joint_coordinates"]:
            movement.flexing_pose_joint_coordinates.append(
                cls._load_coordinate(flexing_pose_joint_coordinate))

        movement.resting_pose_image = cv2.imread(file_path + "_rest.jpg")
        movement.flexing_pose_image = cv2.imread(file_path + "_flex.jpg")

        return movement
    
    @classmethod
    def _load_coordinate(cls, joint_coordinate) -> types.SimpleNamespace:
        coordinate = types.SimpleNamespace()
        coordinate.x = joint_coordinate["x"]
        coordinate.y = joint_coordinate["y"]
        coordinate.z = joint_coordinate["z"]
        coordinate.visibility = joint_coordinate["visibility"]
        return coordinate


# test
if __name__ == "__main__":
    movement = Movement.from_file("res/test")
    print(movement)
