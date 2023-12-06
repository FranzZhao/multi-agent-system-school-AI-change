from mesa import Agent, Model
import math


# * Rasch Model
def rasch_model(a, b, c, x):
    #  y = 1 / (1 + e^(ax+b)) + c
    e_x = math.e ** (a*x + b)
    y = 1 / (1 + e_x) + c
    return y


# * 数值限制模型: [0, 1]
def number_limit(num):
    if num >= 1:
        return num - 0.1
    elif num <= 0:
        return num + 0.1
    else:
        return num


# * 将教师的影响全部控制在[-0.1, 0.1]之间
def teacher_affect(num):
    return 0.2 * num - 0.1


class StudentAgent(Agent):
    __motivation = 0
    __pressure = 0
    __ai_literacy = 0

    def __init__(
        self, unique_id: int, model: Model,
        motivation, pressure, ai_literacy
    ):
        super().__init__(unique_id, model)
        self.__motivation = motivation        # 学生学习动机
        self.__pressure = pressure            # 学生学习压力
        self.__ai_literacy = ai_literacy        # 学生AI素养

    """
    更新学生属性的属性值: 教师通过教学行为影响
    :param teacher_ai_acceptance: 教师AI接纳度
    :param teacher_ai_risk_perception: 教师AI风险感知程度
    :param teacher_ai_literacy: 教师AI素养
    """

    def update(self, teacher_ai_acceptance, teacher_ai_risk_perception, teacher_ai_literacy):
        teacher_affect_literacy = 0.6 * teacher_ai_literacy + 0.3 * \
            teacher_ai_acceptance + 0.1 * teacher_ai_risk_perception
        teacher_affect_motivation = 0.1 * teacher_ai_literacy + 0.6 * \
            teacher_ai_acceptance + 0.3 * teacher_ai_risk_perception
        teacher_affect_pressure = 0.3 * teacher_ai_literacy + 0.1 * \
            teacher_ai_acceptance + 0.6 * teacher_ai_risk_perception
        # 1. 更新学生动机
        # self.__motivation = rasch_model(-8, 4, 0, self.__motivation + teacher_affect)
        self.__motivation = number_limit(
            self.__motivation + teacher_affect(teacher_affect_motivation))
        # 2. 更新学生压力
        # self.__pressure = rasch_model(-8, 4, 0, self.__pressure - teacher_affect)
        self.__pressure = number_limit(
            self.__pressure + teacher_affect(teacher_affect_pressure))
        # 3. 更新学生AI素养
        # self.__ai_literacy = rasch_model(-8, 4, 0, self.__ai_literacy + teacher_affect)
        self.__ai_literacy = number_limit(
            self.__ai_literacy + teacher_affect(teacher_affect_literacy))

    """
    获取学生的认知状态属性值
    """

    def get(self):
        return {
            'stu_motivation': self.__motivation,
            'stu_pressure': self.__pressure,
            'stu_ai_literacy': self.__ai_literacy
        }
