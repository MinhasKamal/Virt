# Minhas Kamal (minhaskamal024@gmail.com)
# 18 Mar 24


class Skeleton:
    joints = [
            ["SR", 11],
            ["SL", 12],
            ["ER", 13],
            ["EL", 14],
            ["WR", 15],
            ["WL", 16],
            ["HR", 23],
            ["HL", 24],
            ["KR", 25],
            ["KL", 26],
            ["AR", 27],
            ["AL", 28]
        ]
    
    @classmethod
    def get_mediapipe_index(cls, str):
        for joint in cls.joints:
            if str == joint[0]:
                return joint[1]
        return -1
    
    @classmethod
    def get_mediapipe_index_list(cls, str_list):
        mediapipe_index_list = []
        for str in str_list:
            mediapipe_index_list.append(cls.get_mediapipe_index(str))
        return mediapipe_index_list
    
