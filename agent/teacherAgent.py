from mesa import Agent, Model
import numpy as np
import math


# * Rasch Model
def rasch_model(a, b, c, x):
    #  y = 1 / (1 + e^(ax+b)) + c
    e_x = math.e ** (a*x + b)
    y = 1 / (1 + e_x) + c
    return y


# * 数值限制模型: [0, 1]
def number_limit(num):
    positive_random = np.random.uniform(0.9, 1.0, 1)[0]
    negative_random = np.random.uniform(0.0, 0.1, 1)[0]
    if num >= 1:
        return positive_random
    elif num <= 0:
        return negative_random
    else:
        return num


# * 产生随机误差 且保证大于0
def random_error(mu, sigma, n):
    is_negative = 1
    # 只要有负negative的就一直循环
    while is_negative == 1:
        random_result = np.random.normal(mu, sigma, n)
        none_negative_num = 0
        for number in random_result:
            if number < 0:
                is_negative = 1
                break
            else:
                none_negative_num += 1
        if none_negative_num == n:
            is_negative = 0
            return random_result


# * 外界影响控制在[-0.1,0.1]
def env_affect_format(num):
    negative_random = np.random.uniform(0, 0.01, 1)[0]
    positive_random = np.random.uniform(0.09, 0.1, 1)[0]
    if num >= 0 and num <= 1:
        return 0.2*num - 0.1
    if num < 0:
        return negative_random
    else:
        return positive_random
    # return 0.2 * num - 0.1

# * 教师Agent


class TeacherAgent(Agent):
    __ai_acceptance = {
        'private': 0,
        'ethics': 0,
        'complexity': 0
    }
    __ai_risk_perception = {
        'private': 0,
        'ethics': 0,
        'complexity': 0
    }
    __ai_literacy = {
        'private': 0,
        'ethics': 0,
        'complexity': 0
    }
    __performance = 0
    __students = np.array([])

    def __init__(
        self, unique_id: int, model: Model,
        ai_acceptance, ai_risk_perception, ai_literacy, performance, students
    ):
        super().__init__(unique_id, model)
        # 随机误差
        random_ai_acceptance = random_error(ai_acceptance, 0.05, 3)
        self.__ai_acceptance = {            # 教师AI接纳度
            'private': random_ai_acceptance[0],
            'ethics': random_ai_acceptance[1],
            'complexity': random_ai_acceptance[2]
        }
        random_ai_risk_perception = random_error(ai_risk_perception, 0.05, 3)
        self.__ai_risk_perception = {       # 教师AI风险感知
            'private': random_ai_risk_perception[0],
            'ethics': random_ai_risk_perception[1],
            'complexity': random_ai_risk_perception[2]
        }
        random_ai_literacy = random_error(ai_literacy, 0.05, 3)
        self.__ai_literacy = {              # 教师AI素养
            'private': random_ai_literacy[0],
            'ethics': random_ai_literacy[1],
            'complexity': random_ai_literacy[2]
        }
        self.__performance = performance              # 教师教学绩效
        self.__students = students                    # 教师所教学生

    """
    教师属性状态更新: 受到其他Agent的影响
    :param source: string 教师具体受到何种因素的影响
    :param value: float 受到影响的因素的具体强度
    """

    def update(self, update_attribute, affect_value_list, teachers, pattern):
        # 确定权重 - 他组织:自组织
        pattern1_weights = [0.25, 0.65]
        pattern2_weights = [0.35, 0.55]
        pattern3_weights = [0.45, 0.45]
        pattern4_weights = [0.55, 0.35]
        pattern5_weights = [0.65, 0.25]
        current_weights = [0, 0]
        if self.model.pattern == 'pattern1':
            current_weights = pattern1_weights
        elif self.model.pattern == 'pattern2':
            current_weights = pattern2_weights
        elif self.model.pattern == 'pattern3':
            current_weights = pattern3_weights
        elif self.model.pattern == 'pattern4':
            current_weights = pattern4_weights
        else:
            current_weights = pattern5_weights
        # 1. 外部影响：计算教师受到的外部环境与学校系统的影响 —— 他组织
        # print('---- teacher ', self.unique_id)
        random = np.random.normal(0, 0.05, 3)
        private_affect = 0
        ethics_affect = 0
        complexity_affect = 0
        affect_len = len(affect_value_list)
        for affect in affect_value_list:
            private_affect += affect['private'] / affect_len + random[0]
            ethics_affect += affect['ethics'] / affect_len + random[1]
            complexity_affect += affect['complexity'] / affect_len + random[2]
        # print('ave env private :', private_affect)
        # print('ave env ethics :', ethics_affect)
        # print('ave env complexity :', complexity_affect)
        private_affect = env_affect_format(private_affect)
        ethics_affect = env_affect_format(ethics_affect)
        complexity_affect = env_affect_format(complexity_affect)
        # print('env private affect :', private_affect)
        # print('env ethics affect :', ethics_affect)
        # print('env complexity affect :', complexity_affect)
        # 2. 教师群体自组织的有限信任模型 —— 自组织
        group_acceptance_private = 0
        group_acceptance_ethics = 0
        group_acceptance_complexity = 0
        group_risk_private = 0
        group_risk_ethics = 0
        group_risk_complexity = 0
        group_literacy_private = 0
        group_literacy_ethics = 0
        group_literacy_complexity = 0
        teacher_len = len(teachers)
        # 2-1. 计算所有教师AI接受度、AI风险感知与AI素养的均值
        for teacher in teachers:
            group_acceptance_private += teacher.__ai_acceptance['private'] / teacher_len
            group_acceptance_ethics += teacher.__ai_acceptance['ethics'] / teacher_len
            group_acceptance_complexity += teacher.__ai_acceptance['complexity'] / teacher_len
            group_risk_private += teacher.__ai_risk_perception['private'] / teacher_len
            group_risk_ethics += teacher.__ai_risk_perception['ethics'] / teacher_len
            group_risk_complexity += teacher.__ai_risk_perception['complexity'] / teacher_len
            group_literacy_private += teacher.__ai_literacy['private'] / teacher_len
            group_literacy_ethics += teacher.__ai_literacy['ethics'] / teacher_len
            group_literacy_complexity += teacher.__ai_literacy['complexity'] / teacher_len
        # 2-2. 计算偏向程度
        group_acceptance_private_affect = env_affect_format(
            group_acceptance_private)
        group_acceptance_ethics_affect = env_affect_format(
            group_acceptance_ethics)
        group_acceptance_complexity_affect = env_affect_format(
            group_acceptance_complexity)
        group_risk_private_affect = env_affect_format(group_risk_private)
        group_risk_ethics_affect = env_affect_format(group_risk_ethics)
        group_risk_complexity_affect = env_affect_format(group_risk_complexity)
        group_literacy_private_affect = env_affect_format(
            group_literacy_private)
        group_literacy_ethics_affect = env_affect_format(group_literacy_ethics)
        group_literacy_complexity_affect = env_affect_format(
            group_literacy_complexity)
        # print('ave teacher self-organize acceptance private :',
        #       group_acceptance_private)
        # print('ave teacher self-organize acceptance ethics :',
        #       group_acceptance_ethics)
        # print('ave teacher self-organize acceptance complexity :',
        #       group_acceptance_complexity)
        # print('ave teacher self-organize risk private :', group_risk_private)
        # print('ave teacher self-organize risk ethics :', group_risk_ethics)
        # print('ave teacher self-organize risk complexity :',
        #       group_risk_complexity)
        # print('ave teacher self-organize literacy private :',
        #       group_literacy_private)
        # print('ave teacher self-organize literacy ethics :',
        #       group_literacy_ethics)
        # print('ave teacher self-organize literacy complexity :',
        #       group_literacy_complexity)

        # print('teacher self-organize acceptance private :',
        #       group_acceptance_private_affect)
        # print('teacher self-organize acceptance ethics :',
        #       group_acceptance_ethics_affect)
        # print('teacher self-organize acceptance complexity :',
        #       group_acceptance_complexity_affect)
        # print('teacher self-organize risk private :', group_risk_private_affect)
        # print('teacher self-organize risk ethics :', group_risk_ethics_affect)
        # print('teacher self-organize risk complexity :',
        #       group_risk_complexity_affect)
        # print('teacher self-organize literacy private :',
        #       group_literacy_private_affect)
        # print('teacher self-organize literacy ethics :',
        #       group_literacy_ethics_affect)
        # print('teacher self-organize literacy complexity :',
        #       group_literacy_complexity_affect)
        # 3. 更新教师属性
        if update_attribute == 'ai_acceptance':
            # print('ai_acceptance =>', affect_value_list)
            # print('self affect acceptance private:',
            #       self.__ai_acceptance['private'])
            # print('self affect acceptance private:',
            #       self.__ai_acceptance['ethics'])
            # print('self affect acceptance private:',
            #       self.__ai_acceptance['complexity'])
            self.__ai_acceptance['private'] = number_limit(
                self.__ai_acceptance['private'] + env_affect_format(1-self.__ai_risk_perception['private'])*0.1 + private_affect*current_weights[0] + group_acceptance_private_affect*current_weights[1] + random[0])
            self.__ai_acceptance['ethics'] = number_limit(
                self.__ai_acceptance['ethics'] + env_affect_format(1-self.__ai_risk_perception['ethics'])*0.1 + ethics_affect*current_weights[0] + group_acceptance_ethics_affect*current_weights[1] + random[1])
            self.__ai_acceptance['complexity'] = number_limit(
                self.__ai_acceptance['complexity'] + env_affect_format(1-self.__ai_risk_perception['complexity'])*0.1 + complexity_affect*current_weights[0] + group_acceptance_complexity_affect*current_weights[1] + random[2])
        elif update_attribute == 'ai_risk_perception':
            # print('ai_risk_perception =>', affect_value_list)
            # print('self affect risk private:',
            #       self.__ai_risk_perception['private'])
            # print('self affect risk ethics:',
            #       self.__ai_risk_perception['ethics'])
            # print('self affect risk complexity:',
            #       self.__ai_risk_perception['complexity'])
            self.__ai_risk_perception['private'] = number_limit(
                self.__ai_risk_perception['private'] - env_affect_format(self.__ai_literacy['private'])*0.1 - private_affect*current_weights[0] - group_risk_private_affect*current_weights[1] + random[0])
            self.__ai_risk_perception['complexity'] = number_limit(
                self.__ai_risk_perception['complexity'] - env_affect_format(self.__ai_literacy['ethics'])*0.1 - complexity_affect*current_weights[0] - group_risk_complexity_affect*current_weights[1] + random[1])
            self.__ai_risk_perception['ethics'] = number_limit(
                self.__ai_risk_perception['ethics'] - env_affect_format(self.__ai_literacy['complexity'])*0.1 - ethics_affect*current_weights[0] - group_risk_ethics_affect*current_weights[1] + random[2])
        elif update_attribute == 'ai_literacy':
            # print('self affect literacy private:',
            #       self.__ai_literacy['private'])
            # print('self affect literacy private:',
            #       self.__ai_literacy['ethics'])
            # print('self affect literacy private:',
            #       self.__ai_literacy['complexity'])
            self.__ai_literacy['private'] = number_limit(
                self.__ai_literacy['private'] + env_affect_format(self.__ai_acceptance['private'])*0.1 + private_affect*current_weights[0] + group_literacy_private_affect*current_weights[1] + random[0])
            self.__ai_literacy['complexity'] = number_limit(
                self.__ai_literacy['complexity'] + env_affect_format(self.__ai_acceptance['ethics'])*0.1 + complexity_affect*current_weights[0] + group_literacy_complexity_affect*current_weights[1] + random[1])
            self.__ai_literacy['ethics'] = number_limit(
                self.__ai_literacy['ethics'] + env_affect_format(self.__ai_acceptance['complexity'])*0.1 + ethics_affect*current_weights[0] + group_literacy_ethics_affect*current_weights[1] + random[2])

    """
    教师教学活动: 
    1. 更新学生认知状态student.update()
    2. 计算总体的教学成效, 更新self.__performance
    """

    def teaching(self):
        student_performance = np.array([])
        teacher_ai_acceptance = (
            self.__ai_acceptance['private'] + self.__ai_acceptance['ethics'] + self.__ai_acceptance['complexity'])/3
        teacher_ai_risk_perception = (
            self.__ai_risk_perception['private'] + self.__ai_risk_perception['ethics'] + self.__ai_risk_perception['complexity'])/3
        teacher_ai_literacy = (
            self.__ai_literacy['private'] + self.__ai_literacy['ethics'] + self.__ai_literacy['complexity'])/3
        # 1. 更新学生认知状态, 同时计算student_performance
        for student in self.__students:
            student.update(teacher_ai_acceptance,
                           teacher_ai_risk_perception, teacher_ai_literacy)
            student_attribute = student.get()
            student_i_performance_x = student_attribute['stu_ai_literacy'] * (student_attribute['stu_motivation'] / (
                student_attribute['stu_motivation'] + student_attribute['stu_pressure']))
            student_i_performance = rasch_model(-8,
                                                4, 0, student_i_performance_x)
            student_performance = np.append(
                student_performance, student_i_performance)
        # print('student performance', student_performance)

        # 2. 计算教师教学成效
        teacher_performance_x = teacher_ai_literacy * \
            (teacher_ai_acceptance / (teacher_ai_acceptance + teacher_ai_risk_perception))
        teacher_performance = rasch_model(-8, 4, 0, teacher_performance_x)
        # print('teacher performance', teacher_performance)

        # 3. 计算总体的教学绩效
        self.__performance = 0.5 * teacher_performance + \
            0.5 * np.mean(student_performance)
        # print('total performance', self.__performance)

    # 获取教师内部属性值
    def get(self, attribute_name):
        # ai_acceptance, ai_risk_perception, ai_literacy, performance
        if attribute_name == 'ai_acceptance':
            return self.__ai_acceptance
        elif attribute_name == 'ai_risk_perception':
            return self.__ai_risk_perception
        elif attribute_name == 'ai_literacy':
            return self.__ai_literacy
        else:
            return self.__performance

    # 访问教师的学生
    def get_students(self):
        return self.__students
