# Minhas Kamal (minhaskamal024@gmail.com)
# 10 Mar 24

import movement
import cv2
import json
from datetime import datetime
import utils

class PatientRecord:
    _datetime_format = "%Y%m%d%H%M%S"

    def __init__(self) -> None:
        self.name: str = ""
        self.repeat: int = ""
        self.assigned_movement: movement.Movement = None
        self.resting_pose_images: list[cv2.typing.MatLike] = []
        self.flexing_pose_images: list[cv2.typing.MatLike] = []
        self.dates: list[str] = []
        self.scores: list[str] = []
        self.file_path: str = ""
        self.movement_file_path: str = ""
        return

    def __str__(self) -> str:
        string: str = "{\n"
        string += f"\"name\" : \"{self.name}\",\n"
        string += f"\"repeat\" : {self.repeat},\n"
        string += f"\"dates\" : {json.dumps(self.dates)},\n"
        string += f"\"scores\" : {json.dumps(self.scores)},\n"
        string += f"\"movement_file_path\" : \"{self.movement_file_path}\"\n"
        string += "}\n"
        return string

    def save(self) -> None:
        if not self.file_path:
            self.file_path = "res/" + self.name
        with open(self.file_path + utils.patient_file_extension, "w") as file:
            file.write(str(self))
        return

    @staticmethod
    def from_file(patientRecord, file_path: str):
        with open(file_path + utils.patient_file_extension, "r") as file:
            patientRecord_json = json.load(file)

        patientRecord.file_path = file_path
        patientRecord.name = patientRecord_json["name"]
        patientRecord.repeat = int(patientRecord_json["repeat"])
        patientRecord.dates = patientRecord_json["dates"]
        patientRecord.scores = patientRecord_json["scores"]
        patientRecord.movement_file_path = patientRecord_json["movement_file_path"]
        patientRecord.assigned_movement = movement.Movement.from_file(patientRecord.movement_file_path)
        return

# test
if __name__ == "__main__":
    patientRecord = PatientRecord()
    PatientRecord.from_file(patientRecord, "res/RightElbow-Minhas")
    patientRecord.dates.append(str(datetime.today().strftime(PatientRecord._datetime_format)))
    patientRecord.scores.append(str(75))
    print(patientRecord)
    # patientRecord.save()
