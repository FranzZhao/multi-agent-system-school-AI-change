import numpy as np

# * 认识论基础


class Epistemology():
    __systemThinking = 0                                        # 系统思考
    __mentalModel = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])       # 心智模式: 9种系统基模

    def __init__(self, systemThinking):
        self.__systemThinking = systemThinking

    # 获取当前管理者Agent的系统思考水平
    def get_system_thinking(self):
        return self.__systemThinking

    # 更新系统思考水平
    def update_system_thinking(self, new_value):
        self.__systemThinking = new_value

    # 获取符合当前系统思考水平的心智模式(9大系统基模)
    def getMentalModel(self, perception, system_thinking):
        pass
