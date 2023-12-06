
from mesa import Model
from mesa.datacollection import DataCollector
from agent.managerAgent import ManagerAgent
from agent.teacherAgent import TeacherAgent
from agent.studentAgent import StudentAgent
from agent.environment import Environment
from mesa.time import RandomActivation
import numpy as np
import math
from collections import Counter


# ! BUG-解决 教师的AI风险感知是越低越好的, 但是管理者的策略决策时, 是差距越大就解决它, 所以关于AI风险感知的需要做调整
# ! BUG-解决 在消极情况下, 当外部环境各种策略产生消极影响时, 教师的属性依旧是增加的?
# ! 上述BUG发现, 原因更为负责, 但目前已经修正, 核心矛盾为: 教师属性中管理层面的权重不够, 且教师各个属性之间相互独立, 所以出现AI素养高但接纳度低的问题, 另外就是管理者学习策略中更新权重的问题了
# TODO-1-完成 学生update算法更新
# TODO-2-完成 人数增加：管理者-8, 教师-15, 学生/教师-20
# TODO-3-完成 管理者intention_decision加入系统思考system_thinking与积极程度active_degree的干预影响, 影响策略的选择
# TODO-4-完成 管理者群体决策算法的更新, 包括决策后的执行人抽取
# TODO-5-完成 管理者action_execution中加入系统思考system_thinking, 积极程度active_degree, 信念倾向tendency的影响, 影响update的程度
# TODO-6-完成 教师update算法中, 除了管理者对教师的影响之外, 还有我们在教师路径中的研究成果-有限信任KH模型
# TODO-7-完成 在管理者action_execution更新为拥有相同执行策略的管理者一起出一个manager_effect, 取平均之后在model中更新
# TODO-8-完成 管理者学习行为Learning
# TODO-9 管理者learning与教师update中考虑不同管理模式的权重影响, 以影响学校系统的组织学习或沟通为主


# * 产生随机误差数组, 并保证每个值均大于0
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


# * 字典去重
def delete_duplicate_str(data):
    immutable_dict = set([str(item) for item in data])
    data = [eval(i) for i in immutable_dict]
    return data


# * 管理者Agent的群体决策
def manager_group_decision_algorithm(model, actions):
    # 1. 计算管理者群体的平均系统思考能力和积极程度
    managers = model.managers
    num = model.manager_num
    ave_system_thinking = 0
    ave_active_degree = 0
    for manager in managers:
        ave_system_thinking += manager.knowledge.epistemology.get_system_thinking() / \
            num
        ave_active_degree += manager.active_degree / num
    ave_value = 0.7 * ave_system_thinking + 0.3 * ave_active_degree
    # print('ave_value =>', ave_value)
    random_value = np.random.uniform(0, 0.9)
    # print('random_value =>', random_value)
    # 2. 对当前所有管理者各自决策的行为进行统计
    # 2-1. 数组去重
    unique_actions = delete_duplicate_str(actions)
    # 2-2. 计算每种策略的出现频次
    unique_actions_cnt = np.array([])
    index = 0
    for action in unique_actions:
        unique_actions_cnt = np.append(unique_actions_cnt, 0)
        for manager_action in actions:
            if action == manager_action:
                unique_actions_cnt[index] += 1
        index += 1
    # 2-3. 查看是否正确计数
    # print(unique_actions)
    # print('cnt =>', unique_actions_cnt)
    # 3-1. 依据平均系统思考与积极程度进行群体决策
    if ave_value < random_value:
        # 平均系统思考过小, 随机抽取
        final_action = np.random.choice(unique_actions)
        # print('random')
    else:
        # 平均系统思考达标, 按少数服从多数执行
        max_index = np.argmax(unique_actions_cnt)
        final_action = unique_actions[max_index]
        # print('right')
    return final_action


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


# ? model data report: school orga climate
def model_data_school_orga_climate(model):
    school_orga_climate = model.school_orga_climate
    return np.mean([school_orga_climate['private'], school_orga_climate['ethics'], school_orga_climate['complexity']])


# ? model data report: school ai env
def model_data_school_ai_env(model):
    ai_env = model.ai_env
    return np.mean([ai_env['private'], ai_env['ethics'], ai_env['complexity']])


# ? model data report: school incentive policy
def model_data_school_incentive_policy(model):
    incentive_policy = model.incentive_policy
    return np.mean([incentive_policy['private'], incentive_policy['ethics'], incentive_policy['complexity']])


# ? model data report: 政府政策支持
def model_data_env_policy_support(model):
    policy_support = model.env.get('policy_support')
    return np.mean([policy_support['private'], policy_support['ethics'], policy_support['complexity']])


# ? model data report: 企业技术支持
def model_data_env_enterprise_support(model):
    enterprise_support = model.env.get('enterprise_support')
    return np.mean([enterprise_support['private'], enterprise_support['ethics'], enterprise_support['complexity']])


# ? model data report: 高校科研支持
def model_data_env_research_support(model):
    research_support = model.env.get('research_support')
    return np.mean([research_support['private'], research_support['ethics'], research_support['complexity']])


# ? model data report: 教师AI接纳度
def model_data_teachers_ai_acceptance(model):
    teachers_ai_acceptance = 0
    teachers = model.teachers
    for teacher in teachers:
        teacher_ai_acceptance = teacher.get('ai_acceptance')
        teachers_ai_acceptance += (teacher_ai_acceptance['private'] +
                                   teacher_ai_acceptance['ethics'] + teacher_ai_acceptance['complexity']) / 3
    teachers_ai_acceptance /= len(teachers)
    return teachers_ai_acceptance


# ? model data report: 教师AI风险感知
def model_data_teachers_ai_risk_perception(model):
    teachers_ai_risk_perception = 0
    teachers = model.teachers
    for teacher in teachers:
        teacher_ai_risk_perception = teacher.get('ai_risk_perception')
        teachers_ai_risk_perception += (teacher_ai_risk_perception['private'] +
                                        teacher_ai_risk_perception['ethics'] + teacher_ai_risk_perception['complexity']) / 3
    teachers_ai_risk_perception /= len(teachers)
    return teachers_ai_risk_perception


# ? model data report: 教师AI素养
def model_data_teachers_ai_literacy(model):
    teachers_ai_literacy = 0
    teachers = model.teachers
    for teacher in teachers:
        teacher_ai_literacy = teacher.get('ai_literacy')
        teachers_ai_literacy += (teacher_ai_literacy['private'] +
                                 teacher_ai_literacy['ethics'] + teacher_ai_literacy['complexity']) / 3
    teachers_ai_literacy /= len(teachers)
    return teachers_ai_literacy


# ? model data report: 教师教学绩效
def model_data_teachers_performance(model):
    teachers_performance = 0
    teachers = model.teachers
    for teacher in teachers:
        teacher_performance = teacher.get('performance')
        teachers_performance += teacher_performance
    teachers_performance /= len(teachers)
    return teachers_performance


# ? model data report: 学生AI素养
def model_data_studnets_ai_literacy(model):
    students_ai_literacy = 0
    students = model.students
    for student in students:
        student_ai_literacy = student.get()['stu_ai_literacy']
        students_ai_literacy += student_ai_literacy
    students_ai_literacy /= len(students)
    return students_ai_literacy


# ? model data report: 学生学习动机
def model_data_studnets_motivation(model):
    students_motivation = 0
    students = model.students
    for student in students:
        student_motivation = student.get()['stu_motivation']
        students_motivation += student_motivation
    students_motivation /= len(students)
    return students_motivation


# ? model data report: 学生学习压力
def model_data_studnets_pressure(model):
    students_pressure = 0
    students = model.students
    for student in students:
        student_pressure = student.get()['stu_pressure']
        students_pressure += student_pressure
    students_pressure /= len(students)
    return students_pressure


# ? model data report: 管理者系统思考能力
def model_data_manager_system_thinking(model):
    return model.manager_ave_system_thinking


# ? model data report: 管理者积极程度
def model_data_manager_active_degree(model):
    return model.manager_ave_active_degree


# ? model data report: 干预策略影响对象-学校组织气氛
def model_data_strategy_school_orga_climate(model):
    return model.strategy_school_orga_climate


# ? model data report: 干预策略影响对象-AI技术环境
def model_data_strategy_ai_env(model):
    return model.strategy_ai_env


# ? model data report: 干预策略影响对象-激励政策
def model_data_strategy_incentive_policy(model):
    return model.strategy_incentive_policy


# ? model data report: 干预策略影响对象-政策支持
def model_data_strategy_policy_support(model):
    return model.strategy_policy_support


# ? model data report: 干预策略影响对象-科研支持
def model_data_strategy_research_support(model):
    return model.strategy_research_support


# ? model data report: 干预策略影响对象-企业技术支持
def model_data_strategy_enterprise_support(model):
    return model.strategy_enterprise_support


# * 学校AI组织变革研究模型
class SchoolModel(Model):
    # 构造函数: 初始化学校模型中的所有对象和属性
    def __init__(
        self, school_ai_vision, env, pattern, initial_manager_value, initial_teacher_value
    ):
        self.pattern = pattern
        self.school_ai_vision = {
            'ai_acceptance': school_ai_vision,
            'ai_risk_perception': school_ai_vision,
            'ai_literacy': school_ai_vision,
        }                                                   # 学校AI变革愿景
        self.school_orga_climate = {
            'private': env,
            'ethics': env,
            'complexity': env,
        }                                                   # 学校组织气氛
        self.ai_env = {
            'private': env,
            'ethics': env,
            'complexity': env,
        }                                                   # AI技术环境
        self.incentive_policy = {
            'private': env,
            'ethics': env,
            'complexity': env,
        }                                                   # 激励政策
        self.managers = np.array([])                        # 管理者集合-初始化空数组
        self.teachers = np.array([])                        # 教师集合-初始化空数组
        self.students = np.array([])                        # 学生集合-初始化空数组
        self.env = Environment(                             # 学校所处外部环境
            env, env, env
        )
        self.current_id = 0                                 # Agent ID
        self.running = True                                 # 可以让后台自动运行
        self.count = 0                                      # 仿真步骤
        self.manager_num = 8                                # 管理者Agent数量
        self.teacher_num = 15                               # 教师Agent数量
        self.student_per_teacher = 20                       # 每位教师的学生数量
        self.student_num = self.teacher_num * self.student_per_teacher
        # 管理者策略筛选情况统计-干预对象
        self.strategy_school_orga_climate = 0
        self.strategy_ai_env = 0
        self.strategy_incentive_policy = 0
        self.strategy_policy_support = 0
        self.strategy_research_support = 0
        self.strategy_enterprise_support = 0
        # 管理者策略筛选情况统计-具体策略
        self.strategy_private_ai_acceptance = 0
        self.strategy_private_ai_risk = 0
        self.strategy_private_ai_literacy = 0
        self.strategy_ethics_ai_acceptance = 0
        self.strategy_ethics_ai_risk = 0
        self.strategy_ethics_ai_literacy = 0
        self.strategy_complexity_ai_acceptance = 0
        self.strategy_complexity_ai_risk = 0
        self.strategy_complexity_ai_literacy = 0
        # 管理者平均系统思考能力与活跃程度
        self.manager_ave_system_thinking = 0
        self.manager_ave_active_degree = 0
        # 记录最终选择的策略
        self.managers_final_action = np.array([])
        self.schedule = RandomActivation(self)

        # Step 1 : 创建管理者Agent
        # 随机生成管理者Agent的系统思考systemThinking水平, mu=0.5, sigma=0.15, n=3
        random_system_thinking = random_error(
            initial_manager_value, 0.1, self.manager_num)
        random_active_degree = random_error(
            initial_manager_value, 0.1, self.manager_num)
        # 实例化管理者Agent
        for i in range(self.manager_num):
            new_manager = ManagerAgent(
                self.next_id(), self, random_system_thinking[i], random_active_degree[i])
            self.managers = np.append(self.managers, new_manager)
            self.manager_ave_system_thinking += random_system_thinking[i] / \
                self.manager_num
            self.manager_ave_active_degree += random_active_degree[i] / \
                self.manager_num
            # self.schedule.add(new_manager)

        # Step 2 : 创建学生Agent
        # 随机生成学生gent的学习动机、学习压力与AI素养水平
        random_motivation = random_error(0.5, 0.15, self.student_num)
        random_pressure = random_error(0.5, 0.15, self.student_num)
        random_stu_ai_literacy = random_error(0.5, 0.15, self.student_num)
        # 实例化学生Agent
        for i in range(self.student_num):
            new_student = StudentAgent(
                self.next_id(), self,
                random_motivation[i], random_pressure[i], random_stu_ai_literacy[i]
            )
            self.students = np.append(self.students, new_student)

        # Step 3 : 创建教师Agent
        # 随机生成教师Agent的AI接纳度、AI风险感知与AI素养水平
        random_ai_acceptance = random_error(
            initial_teacher_value, 0.15, self.teacher_num)
        random_ai_risk_perception = random_error(
            initial_teacher_value, 0.15, self.teacher_num)
        random_teacher_ai_literacy = random_error(
            initial_teacher_value, 0.15, self.teacher_num)
        # 教师所教学生的index(遍历self.students[])
        stu_index = 0
        # 实例化教师Agent
        for i in range(self.teacher_num):
            student_list = np.array([])
            for j in range(self.student_per_teacher):
                student_list = np.append(
                    student_list, self.students[j+stu_index])
            new_teacher = TeacherAgent(
                self.next_id(), self,
                random_ai_acceptance[i], random_ai_risk_perception[i], random_teacher_ai_literacy[i],
                0, student_list)
            self.teachers = np.append(self.teachers, new_teacher)
            # 增加学生index
            stu_index += self.student_per_teacher

        # School Model 每回合要采集的统计分析数据
        self.datacollector = DataCollector(
            model_reporters={
                # 学校层面关键变量-管理者调控
                "school_orga_climate": model_data_school_orga_climate,
                "ai_env": model_data_school_ai_env,
                "incentive_policy": model_data_school_incentive_policy,
                # 环境因素关键变量-管理者调控
                "env.policy_support": model_data_env_policy_support,
                "env.research_support": model_data_env_research_support,
                "env.enterprise_support": model_data_env_enterprise_support,
                # 教师关键变量
                "teachers.ai_acceptance": model_data_teachers_ai_acceptance,
                "teachers.ai_risk_perception": model_data_teachers_ai_risk_perception,
                "teachers.ai_literacy": model_data_teachers_ai_literacy,
                "teachers.total_performance": model_data_teachers_performance,
                # 学生关键变量
                "students.ai_literacy": model_data_studnets_ai_literacy,
                "students.motivation": model_data_studnets_motivation,
                "students.pressure": model_data_studnets_pressure,
                # 干预策略对象
                "strategy_school_orga_climate": model_data_strategy_school_orga_climate,
                "strategy_ai_env": model_data_strategy_ai_env,
                "strategy_incentive_policy": model_data_strategy_incentive_policy,
                "strategy_policy_support": model_data_strategy_policy_support,
                "strategy_research_support": model_data_strategy_research_support,
                "strategy_enterprise_support": model_data_strategy_enterprise_support,
                # 干预策略名称
                "strategy_private_ai_acceptance": "strategy_private_ai_acceptance",
                "strategy_private_ai_risk": "strategy_private_ai_risk",
                "strategy_private_ai_literacy": "strategy_private_ai_literacy",
                "strategy_ethics_ai_acceptance": "strategy_ethics_ai_acceptance",
                "strategy_ethics_ai_risk": "strategy_ethics_ai_risk",
                "strategy_ethics_ai_literacy": "strategy_ethics_ai_literacy",
                "strategy_complexity_ai_acceptance": "strategy_complexity_ai_acceptance",
                "strategy_complexity_ai_risk": "strategy_complexity_ai_risk",
                "strategy_complexity_ai_literacy": "strategy_complexity_ai_literacy",
                # 管理者系统思考与积极程度
                "manager_system_thinking": model_data_manager_system_thinking,
                "manager_active_degree": model_data_manager_active_degree,
            }
        )

    # 获取学校系统中的属性
    def get(self, target_attribute):
        target_value = 0
        if target_attribute == 'school_orga_climate':
            # 学校组织气氛
            target_value = self.school_orga_climate
        elif target_attribute == 'ai_env':
            # 学校AI技术环境
            target_value = self.ai_env
        elif target_attribute == 'incentive_policy':
            # 学校激励政策
            target_value = self.incentive_policy
        return target_value

    # 更新学校系统中的属性
    def update(self, update_attribute, update_value):
        if update_attribute == 'school_orga_climate':
            # 学校组织气氛
            self.school_orga_climate = update_value
        elif update_attribute == 'ai_env':
            # 学校AI技术环境
            self.ai_env = update_value
        elif update_attribute == 'incentive_policy':
            # 学校激励政策
            self.incentive_policy = update_value

    # 获取学校系统中指定属性的属性值
    def get_specific_attribute(self, attribute_name):
        if attribute_name == 'school_ai_vision':
            return self.school_ai_vision

    # 获取学校系统中全局关键属性的平均值: 与愿景挂钩
    def get_ave_attribute(self):
        # 1. 当前与愿景相关变量的取值情况
        current_vision_value = {
            'ai_acceptance': 0.00,
            'ai_risk_perception': 0.00,
            'ai_literacy': 0.00,
        }
        # 2. 获取当前教师AI接纳度、教师AI风险感知、教师AI素养
        for teacher in self.teachers:
            teacher_ai_acceptance = teacher.get('ai_acceptance')
            teacher_ai_risk_perception = teacher.get('ai_risk_perception')
            teacher_ai_literacy = teacher.get('ai_literacy')
            current_vision_value['ai_acceptance'] += (teacher_ai_acceptance['private'] +
                                                      teacher_ai_acceptance['ethics'] + teacher_ai_acceptance['complexity'])/3
            current_vision_value['ai_risk_perception'] += (teacher_ai_risk_perception['private'] +
                                                           teacher_ai_risk_perception['ethics'] + teacher_ai_risk_perception['complexity'])/3
            current_vision_value['ai_literacy'] += (teacher_ai_literacy['private'] +
                                                    teacher_ai_literacy['ethics'] + teacher_ai_literacy['complexity'])/3
        # 3. 计算平均情况
        current_vision_value['ai_acceptance'] /= len(self.teachers)
        current_vision_value['ai_risk_perception'] /= len(self.teachers)
        current_vision_value['ai_literacy'] /= len(self.teachers)
        # 4. 返回
        return current_vision_value

    # 管理者干预策略的统计
    def static_strategies(self, final_action):
        # 干预策略对象统计
        if final_action['attribute'] == 'school_orga_climate':
            self.strategy_school_orga_climate += 1
        elif final_action['attribute'] == 'ai_env':
            self.strategy_ai_env += 1
        elif final_action['attribute'] == 'incentive_policy':
            self.strategy_incentive_policy += 1
        elif final_action['attribute'] == 'policy_support':
            self.strategy_policy_support += 1
        elif final_action['attribute'] == 'research_support':
            self.strategy_research_support += 1
        elif final_action['attribute'] == 'enterprise_support':
            self.strategy_enterprise_support += 1
        # 干预策略统计
        if final_action['name'] == '外部监督':
            self.strategy_private_ai_acceptance += 1
        elif final_action['name'] == '内部审查':
            self.strategy_private_ai_risk += 1
        elif final_action['name'] == '教师培训-数据素养':
            self.strategy_private_ai_literacy += 1
        elif final_action['name'] == '算法透明与公开':
            self.strategy_ethics_ai_acceptance += 1
        elif final_action['name'] == '校内反馈':
            self.strategy_ethics_ai_risk += 1
        elif final_action['name'] == '教师培训-AI基础':
            self.strategy_ethics_ai_literacy += 1
        elif final_action['name'] == 'AI设计优化与迭代':
            self.strategy_complexity_ai_acceptance += 1
        elif final_action['name'] == '组织支持与激励':
            self.strategy_complexity_ai_risk += 1
        elif final_action['name'] == 'AI教学实践培训':
            self.strategy_complexity_ai_literacy += 1

    # 管理者群体对学校系统3变量与外界环境3变量进行更新
    def managers_group_action(self, manager_effect, target_object, attribute, reason):
        # print('manager effect:', manager_effect)
        # print('object', target_object)
        # print('attribute', attribute)
        # print('reason', reason)
        if target_object == 'school':
            # 2-1. 更新学校组织变量
            if reason == 'private':
                old_value = self.get(attribute)
                # print('old_value:', old_value)
                update_value = number_limit(
                    old_value['private'] + manager_effect)
                new_value = old_value
                new_value['private'] = update_value
                self.update(attribute, new_value)
                # print('new_value:', new_value)
            elif reason == 'ethics':
                old_value = self.get(attribute)
                # print('old_value:', old_value)
                update_value = number_limit(
                    old_value['ethics'] + manager_effect)
                new_value = old_value
                new_value['ethics'] = update_value
                self.update(attribute, new_value)
                # print('new_value:', new_value)
            elif reason == 'complexity':
                old_value = self.get(attribute)
                # print('old_value:', old_value)
                update_value = number_limit(
                    old_value['complexity'] + manager_effect)
                new_value = old_value
                new_value['complexity'] = update_value
                self.update(attribute, new_value)
                # print('new_value:', new_value)
        elif target_object == 'environment':
            # 2-2. 寻求外部环境支持
            if reason == 'private':
                old_value = self.env.get(attribute)
                # print('old_value:', old_value)
                update_value = number_limit(
                    old_value['private'] + manager_effect)
                new_value = old_value
                new_value['private'] = update_value
                self.env.update(attribute, new_value)
                # print('new_value:', new_value)
            elif reason == 'ethics':
                old_value = self.env.get(attribute)
                # print('old_value:', old_value)
                update_value = number_limit(
                    old_value['ethics'] + manager_effect)
                new_value = old_value
                new_value['ethics'] = update_value
                self.env.update(attribute, new_value)
                # print('new_value:', new_value)
            elif reason == 'complexity':
                old_value = self.env.get(attribute)
                # print('old_value:', old_value)
                update_value = number_limit(
                    old_value['complexity'] + manager_effect)
                new_value = old_value
                new_value['complexity'] = update_value
                self.env.update(attribute, new_value)
                # print('new_value:', new_value)

    # 获取管理者平均系统思考与活跃程度
    def get_managers_ave_value(self):
        ave_system_thinking = 0
        ave_active_degree = 0
        for manager in self.managers:
            ave_system_thinking += manager.knowledge.epistemology.get_system_thinking() / \
                self.manager_num
            ave_active_degree += manager.active_degree / self.manager_num
        return ave_system_thinking, ave_active_degree

    # 系统仿真步骤
    def step(self):
        self.count += 1
        if self.count == 1:
            # print('---------- 第 1 轮仿真 ----------')
            # --- step : 教师直接开展教学活动 ---
            # print('1. 教师开展教学活动')
            # 教师Agent的行为
            for teacher in self.teachers:
                teacher.teaching()
        else:
            # print('---------- 第 ', self.count, ' 轮仿真 ----------')
            # print('model_ai_env:', self.ai_env, )
            # print('model_incentive_policy', self.incentive_policy)
            # print('ai_orga_climate', self.school_orga_climate)
            # --- step 1: 管理者Agent的BDI感知与决策过程 ---
            manager_cnt = 1
            for manager in self.managers:
                manager.step()
                manager_cnt += 1
            # --- step 2: 管理者Agents进行群体观点决策 ---
            manager_actions = np.array([])
            for manager in self.managers:
                action = manager.intention.get()
                manager_actions = np.append(manager_actions, action)
            # print('managers actions =>', manager_actions)
            final_action = manager_group_decision_algorithm(
                self, manager_actions)
            # print('final =>', final_action)
            self.static_strategies(final_action)
            self.managers_final_action = final_action
            # --- step 3: 管理者Agent实施行为干预 ---
            # 3-1. 从与final_action相同的所有管理者
            managers_effect_list = np.array([])
            for manager in self.managers:
                action = manager.intention.get()
                if action['name'] == final_action['name'] and action['attribute'] == final_action['attribute']:
                    # 管理者进行action_execution()获取其manager_effect
                    manager_effect = manager.action_execution()
                    managers_effect_list = np.append(
                        managers_effect_list, manager_effect)
            # print('managers_effect_list=>', managers_effect_list)
            # print('ave_effect', np.mean(managers_effect_list))
            # 3-2. 计算平均的影响程度
            ave_managers_effect = np.mean(managers_effect_list)
            # 3-3. 对学校系统变量或外界环境变量进行更新
            self.managers_group_action(
                ave_managers_effect, final_action['object'], final_action['attribute'], final_action['reason']
            )
            # # --- step 4: 更新教师Agent的状态 ---
            for teacher in self.teachers:
                # ai_acceptance: 企业技术培训 + 学校AI技术环境
                teacher.update('ai_acceptance', np.array([
                    self.env.enterprise_support, self.env.policy_support, self.ai_env
                ]), self.teachers, self.pattern)
                # ai_risk_perception: 企业技术更新 + 学校激励政策
                teacher.update('ai_risk_perception', np.array([
                    self.env.policy_support, self.incentive_policy, self.ai_env, self.school_orga_climate
                ]), self.teachers, self.pattern)
                # ai_literacy: 高校教师培训 + 学校组织气氛
                teacher.update('ai_literacy', np.array([
                    self.env.research_support, self.school_orga_climate, self.ai_env
                ]), self.teachers, self.pattern)
            # --- step 5: 教师开展教学活动 ---
            # 教师Agent的行为
            for teacher in self.teachers:
                teacher.teaching()
            # --- step 6: 管理者学习行为
            # print('6. 管理者Agent学习行为')
            ave_system_thinking = 0
            ave_active_degree = 0
            for manager in self.managers:
                active_degree, system_thinking = manager.learning()
                ave_system_thinking += system_thinking / self.manager_num
                ave_active_degree += active_degree / self.manager_num
            self.manager_ave_system_thinking = ave_system_thinking
            # print('ave_system_thinking =>', ave_system_thinking)
            self.manager_ave_active_degree = ave_active_degree
            # print('ave_active_degree =>', ave_active_degree)
        # 采集数据
        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == '__main__':
    # 初始化
    model = SchoolModel(
        0.8, 0.5, 'pattern1', 0.5, 0.5
    )
    # 查看教师学生匹配关系
    # for teacher in model.teachers:
    #     print('I am teacher', teacher.unique_id)
    #     students = teacher.get_students()
    #     for student in students:
    #         print('-> student', student.unique_id)
    # 仿真循环
    for i in range(5):
        model.step()
    # 获取仿真结果
    # print("--------------仿真结果--------------")
    # model_result = model.data_collector.get_model_vars_dataframe()
    # print(model_result)
    # 分析结果；
    # 1. 统计各类变量的变化情况
    # 2. 统计管理者在一个学期内更注重什么策略
