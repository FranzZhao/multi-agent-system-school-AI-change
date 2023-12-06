from mesa import Agent, Model
from agent.bdiBase.KnowledgeBase import KnowledgeBase
from agent.bdiBase.BeliefBase import BeliefBase
from agent.bdiBase.DesireBase import DesireBase
from agent.bdiBase.IntentionBase import IntentionBase
import numpy as np
import math


# * Rasch模型
def rasch_model(x, a=-8, b=4, c=0):
    #  y = 1 / (1 + e^(ax+b)) + c
    # 默认: y = 1 / (1 + e^-(8x-4))
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


# * 影响程度限制在: [-0.1, 0.1]
def env_affect_format(num, a=0.2, b=-0.1):
    return a*num + b


# * 信念推理算法1: 根据gap与系统思考能力，排出处理gap的优先级
# TODO 还没有添加系统思考的干扰
def gap_priority_rank(perceptions, system_thinking):
    np_gap = np.array([])
    # 1. 先抽取出perceptions中的gap信息
    for i in range(len(perceptions)):
        np_gap = np.append(np_gap, perceptions[i]['gap'])
    # 2. 对np_gap进行排序, 由小到大排序, 由于gap是"当前-愿景"的, 因此值越小表示(越负)表示离愿景很远, 最终返回由小到大的下标索引
    priority = np.argsort(np_gap)
    # 3. 返回优先处理的gap最大的perception信息
    return perceptions[priority[0]]


# * 信念推理算法2: 剖析问题原因
# TODO 还没添加系统思考、积极程度与心智模式的干扰
def find_reason(first_priority, teachers):
    # reason_list => [private, ethics, complexity]
    reason_list = [0, 0, 0]
    reason = ''
    # teachers = self.model.teachers
    for teacher in teachers:
        target_attribute = teacher.get(first_priority['attribute'])
        # print('teacher =>',target_attribute)
        target_array = np.array([
            target_attribute['private'],  target_attribute['ethics'],  target_attribute['complexity']
        ])
        reason_priority = np.argsort(target_array)
        if reason_priority[0] == 0:
            # private数据隐私的问题
            reason_list[0] += 1
        elif reason_priority[0] == 1:
            # ethics算法伦理的问题
            reason_list[1] += 1
        else:
            # complexity技术复杂性的问题
            reason_list[2] += 1
    reason_list_priority = np.argsort(reason_list)
    reason = ''
    if reason_list_priority[len(reason_list_priority)-1] == 0:
        reason = 'private'
    elif reason_list_priority[len(reason_list_priority)-1] == 1:
        reason = 'ethics'
    else:
        reason = 'complexity'
    return reason


# * 信念推理算法3: 计算信念倾向
# TODO 还没添加系统系统、积极程度与心智模式的干扰 -> 不过这个好像不需要……
def computing_tendency(active_degree, system_thinking):
    tendency = rasch_model((active_degree + system_thinking)/2)
    return tendency


# * 管理者Agent
class ManagerAgent(Agent):
    def __init__(
        self, unique_id: int, model: Model, system_thinking, active_degree
    ):
        super().__init__(unique_id, model)
        self.active_degree = active_degree                      # 管理者积极程度
        self.knowledge = KnowledgeBase(system_thinking)         # 管理者知识库
        self.belief = BeliefBase()                              # 管理者信念库
        self.desire = DesireBase()                              # 管理者愿望库
        self.intention = IntentionBase()                        # 管理者意图库
        self.intention_is_right = 1                             # 管理者意图决策是否与问题一致

    # 感知器
    def perceive(self):
        # 1. 获取当前全局状态
        # 教师AI接纳度、教师AI风险感知、教师AI素养 {'ai_acceptance', 'ai_risk_perception', 'ai_literacy'}
        info = self.model.get_ave_attribute()
        # 2. 获取学校AI变革愿景
        school_ai_vision = self.model.get_specific_attribute(
            'school_ai_vision')
        # 3. 计算当前状态与愿景之间的差距
        gap = {
            'ai_acceptance': 0.00,
            'ai_risk_perception': 0.00,
            'ai_literacy': 0.00,
        }
        gap['ai_acceptance'] = info['ai_acceptance'] - \
            school_ai_vision['ai_acceptance']
        # 风险risk的计算必须反过来，因为风险是越低越好的, 所以是用愿景-当前情况
        gap['ai_risk_perception'] = school_ai_vision['ai_risk_perception'] - \
            info['ai_risk_perception']
        gap['ai_literacy'] = info['ai_literacy'] - \
            school_ai_vision['ai_literacy']
        # 4. 更新/存储到陈述性知识中
        self.knowledge.dec_knowledge.update([
            {
                'object': 'teacher',
                'attribute': 'ai_acceptance',
                'value': info['ai_acceptance'],
                'gap': gap['ai_acceptance']
            },
            {
                'object': 'teacher',
                'attribute': 'ai_risk_perception',
                'value': info['ai_risk_perception'],
                'gap': gap['ai_risk_perception']
            },
            {
                'object': 'teacher',
                'attribute': 'ai_literacy',
                'value': info['ai_literacy'],
                'gap': gap['ai_literacy']
            },
        ])

    # 信念推理器
    def belief_reasoning(self):
        # 1-1. 从陈述性知识中获取感知器获取的信息
        perceptions = self.knowledge.dec_knowledge.get()
        # 1-2. 获取当前该管理者Agent的系统思考能力
        system_thinking = self.knowledge.epistemology.get_system_thinking()
        # 2. 依据系统思考能力，判断感知器获取的信息中，优先处理哪个gap：推理算法1
        first_priority = gap_priority_rank(perceptions, system_thinking)
        # 3. 依据系统思考能力与其对应的心智模式, 剖析问题原因与意图倾向
        # 3-1. 首先, 发现问题原因
        reason = find_reason(first_priority, self.model.teachers)
        # 3-2. 其次，计算解决问题的倾向
        tendency = computing_tendency(self.active_degree, system_thinking)
        # 4. 组建形成管理者Agent的信念
        belief = {
            'perception': first_priority,
            'reason': reason,
            'tendency': tendency,
            'system thinking': system_thinking,
            'active degree': self.active_degree,
        }
        # 5. 更新信念库
        self.belief.update(
            object=belief['perception']['object'],
            attribute=belief['perception']['attribute'],
            value=belief['perception']['value'],
            gap=belief['perception']['gap'],
            reason=belief['reason'],
            tendency=belief['tendency']
        )

    # 愿望推理器
    def desire_reasoning(self):
        # 1. 获取信念
        belief = self.belief.get()
        # print('belief =>', belief)
        # 2. 根据tendency倾向强调, 以及value和gap的大小, 计算Agent期望达成的目标goal
        goal = belief['value'] + rasch_model(
            x=belief['tendency']+belief['gap']/2,
            c=0,
        )/12
        # print('belief =>', belief)
        # print('goal =>', goal)
        # 3. 更新愿望库
        self.desire.update(
            belief['object'], belief['attribute'], belief['reason'], goal)
        # print('manage', self.unique_id, ', desire =>',
        #       self.desire.get(), '=>', belief['value'])

    # 意图决策器
    def intention_decision(self):
        # 1-1. 获取愿望
        desire = self.desire.get()
        # print('id', self.unique_id, 'desire =>', desire)
        # 1-2. 获取系统思考
        system_thinking = self.knowledge.epistemology.get_system_thinking()
        # 1-3. 获取积极程度
        active_degree = self.active_degree
        # 1-4. 计算管理者在进行策略决策时的个体倾向
        personal_value = 0.7 * system_thinking + 0.3 * active_degree
        # print('id', self.unique_id, 'personal value =>', personal_value)
        # 2. 获取知识库中的程序性知识
        pro_knowledge, is_right = self.knowledge.pro_knowledge.get(
            desire['reason'], desire['attribute'], personal_value)
        # print('id', self.unique_id, 'pro knowledge =>', pro_knowledge)
        # print('is_right =>', is_right)
        self.intention_is_right = is_right
        # 3. 筛选出管理者Agent认为最佳的行动策略
        # 初版以随机筛选行动策略为主
        best_action = np.random.choice(pro_knowledge['actions'], 1)[0]
        # 4. 更新意图
        self.intention.update(
            action_name=pro_knowledge['pro_knowledge_name'],
            action_object=best_action['action_object'],
            action_attribute=best_action['action_attribute'],
            action_reason=pro_knowledge['reason'],
            action_weights=best_action['action_experience']
        )
        # print(self.intention.get())

    # 执行器
    def action_execution(self):
        # 1-1. 获取行为意图
        intention = self.intention.get()
        # print('manager', self.unique_id, ' intention execution =>', intention)
        # 1-2. 获取信念倾向tendency
        tendency = self.belief.get()['tendency']
        # 1-3. 获取系统思考能力
        system_thinking = self.knowledge.epistemology.get_system_thinking()
        # 1-4. 获取积极程度
        active_degree = self.active_degree
        # 1-5. 获取行动原因
        reason = intention['reason']
        # 1-6. 获取行动目标
        goal = self.desire.get()['goal']
        # print('tendency:', tendency)
        # print('system_thinking:', system_thinking)
        # print('active_degree:', active_degree)
        # print('goal:', goal)
        # ? 2. 管理者依据system_thinking, active_degree, tendency决定update的具体程度
        manager_effect = env_affect_format(
            (system_thinking + active_degree + tendency)/3)
        # print('manager_effect:', manager_effect)
        return manager_effect

    # 学习行为
    def learning(self):
        # 1. Learning 1 根据自身达成情况进行判断
        belief = self.belief.get()
        # 1-1. 获取目标愿望等信息
        desire = self.desire.get()
        intention = self.intention.get()
        # print('manager id:', self.unique_id)
        # print('belief :', belief)
        # print('desire :', desire)
        # print('intention :', intention)
        # 1-2. intention决策出的pro knowledge与实际问题是一致的
        # print('is_right=>', self.intention_is_right)
        # 如果决策正确, 则权重为1.2; 错误的话, 影响权重为0.8 --> 这个权重和管理模式挂钩
        is_right_weight = 1.2 if self.intention_is_right == 1 else 0.8
        # print('is_right_weight =>', is_right_weight)
        # 2. Learning 2 管理者团队的组织学习
        # print('system thinking', self.knowledge.epistemology.get_system_thinking())
        # print('active degree', self.active_degree)
        ave_managers_system_thinking = self.model.manager_ave_system_thinking
        ave_managers_active_degree = self.model.manager_ave_active_degree
        # print('ave_managers_system_thinking =>', ave_managers_system_thinking)
        # print('ave_managers_active_degree =>', ave_managers_active_degree)
        ave_manager_value = (ave_managers_active_degree +
                             ave_managers_system_thinking)/2
        # print('ave_manager =>', ave_manager_value)
        # 3. Learning 3 根据教师的反馈
        ave_teacher = self.model.get_ave_attribute()
        ave_teacher_value = (ave_teacher['ai_acceptance'] - ave_teacher['ai_risk_perception'] +
                             ave_teacher['ai_literacy'])/2
        # print('ave_teacher =>', ave_teacher_value)
        # 4. 根据管理模式, 确定3中learning策略各自的权重
        # 权重比 他组织:自组织
        pattern1_weights = [0.2, 0.8]
        pattern2_weights = [0.35, 0.65]
        pattern3_weights = [0.5, 0.5]
        pattern4_weights = [0.65, 0.35]
        pattern5_weights = [0.8, 0.2]
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
        # 5. 根据权重与学习率, 确定系统思考与积极程度的更新值
        # print('old active degree =>', self.active_degree)
        # print('old system thinking =>',
        #       self.knowledge.epistemology.get_system_thinking())
        # print('---------- manager ', self.unique_id, '----------')
        # print('is right ', is_right_weight)
        random_value = np.random.uniform(-0.1, 0.1, 1)[0]
        if is_right_weight == 1.2:
            affect1 = env_affect_format(
                number_limit(ave_teacher_value), 0.12, -0.03)
            affect2 = env_affect_format(
                number_limit(ave_manager_value), 0.12, -0.03)
            # print('teacher ai acceptance ', ave_teacher['ai_acceptance'])
            # print('teacher ai risk perception ',
            #       ave_teacher['ai_risk_perception'])
            # print('teacher ai literacy ', ave_teacher['ai_literacy'])
            # print('teacher value ', ave_teacher_value)
            # print('manager value ', ave_manager_value)
            # print('randon value =>', random_value)
            # print('teacher affect ', affect1)
            # print('manager affect ', affect2)
            manager_update_value = (
                current_weights[1] * affect1 + current_weights[0] * affect2 + random_value) * 0.3
        else:
            affect1 = env_affect_format(
                number_limit(ave_teacher_value), 0.2, -0.12)
            affect2 = env_affect_format(
                number_limit(ave_manager_value), 0.2, -0.12)
            # print('teacher ai acceptance ', ave_teacher['ai_acceptance'])
            # print('teacher ai risk perception ',
            #       ave_teacher['ai_risk_perception'])
            # print('teacher ai literacy ', ave_teacher['ai_literacy'])
            # print('teacher value ', ave_teacher_value)
            # print('manager value ', ave_manager_value)
            # print('randon value =>', random_value)
            # print('teacher affect ', affect1)
            # print('manager affect ', affect2)
            manager_update_value = (
                current_weights[1] * affect1 + current_weights[0] * affect2 + random_value) * 0.3
        # print('manager update value =>', manager_update_value)
        # print('old active degree =>', self.active_degree)
        new_active_degree = number_limit(
            self.active_degree + manager_update_value * 1)
        self.active_degree = new_active_degree
        # print('old system thinking =>',
        #       self.knowledge.epistemology.get_system_thinking())
        new_system_thinking = number_limit(
            self.knowledge.epistemology.get_system_thinking() + manager_update_value * 1)
        self.knowledge.epistemology.update_system_thinking(new_system_thinking)
        # print('new active degree =>', self.active_degree)
        # print('new system thinking =>',
        #       self.knowledge.epistemology.get_system_thinking())
        return new_active_degree, new_system_thinking

    # 管理者Agent的行为步骤
    def step(self):
        self.perceive()
        self.belief_reasoning()
        self.desire_reasoning()
        self.intention_decision()
