import numpy as np


class ProKnowledgeBase():
    # 程序性知识描述了管理者Agent在解决特定问题时的路径是什么
    __pro_knowledge_private = np.array([
        {
            'pro_knowledge_name': '外部监管',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'enterprise_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'environment',
                    'action_attribute': 'policy_support',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'private',
            'target_object': 'teacher',
            'target_attribute': 'ai_acceptance',
            'weight': {
                'pattern1': 0.6,
                'pattern2': 0.3,
                'pattern3': 0.1,
                'pattern4': 0.8,
            },
        },
        {
            'pro_knowledge_name': '内部审查',
            'actions': [
                {
                    'action_object': 'school',
                    'action_attribute': 'ai_env',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'incentive_policy',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'private',
            'target_object': 'teacher',
            'target_attribute': 'ai_risk_perception',
            'target_attribute_weight': {
                'ai_acceptance': 0.1,
                'ai_risk_perception': 0.6,
                'ai_literacy': 0.3,
            },
        },
        {
            'pro_knowledge_name': '教师培训-数据素养',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'research_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'school_orga_climate',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'private',
            'target_object': 'teacher',
            'target_attribute': 'ai_literacy',
            'target_attribute_weight': {
                'ai_acceptance': 0.3,
                'ai_risk_perception': 0.1,
                'ai_literacy': 0.6,
            },
        },
    ])
    __pro_knowledge_ethics = np.array([
        {
            'pro_knowledge_name': '算法透明与公开',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'enterprise_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'environment',
                    'action_attribute': 'policy_support',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'ethics',
            'target_object': 'teacher',
            'target_attribute': 'ai_acceptance',
            'target_attribute_weight': {
                'ai_acceptance': 0.6,
                'ai_risk_perception': 0.3,
                'ai_literacy': 0.1,
            },
        },
        {
            'pro_knowledge_name': '校内反馈',
            'actions': [
                {
                    'action_object': 'school',
                    'action_attribute': 'school_orga_climate',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'incentive_policy',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'ethics',
            'target_object': 'teacher',
            'target_attribute': 'ai_risk_perception',
            'target_attribute_weight': {
                'ai_acceptance': 0.1,
                'ai_risk_perception': 0.6,
                'ai_literacy': 0.3,
            },
        },
        {
            'pro_knowledge_name': '教师培训-AI基础',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'research_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'ai_env',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'ethics',
            'target_object': 'teacher',
            'target_attribute': 'ai_literacy',
            'target_attribute_weight': {
                'ai_acceptance': 0.3,
                'ai_risk_perception': 0.1,
                'ai_literacy': 0.6,
            },
        },
    ])
    __pro_knowledge_complexity = np.array([
        {
            'pro_knowledge_name': 'AI设计优化与迭代',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'enterprise_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'ai_env',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'complexity',
            'target_object': 'teacher',
            'target_attribute': 'ai_acceptance',
            'target_attribute_weight': {
                'ai_acceptance': 0.6,
                'ai_risk_perception': 0.3,
                'ai_literacy': 0.1,
            },
        },
        {
            'pro_knowledge_name': '组织支持与激励',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'policy_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'incentive_policy',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'complexity',
            'target_object': 'teacher',
            'target_attribute': 'ai_risk_perception',
            'target_attribute_weight': {
                'ai_acceptance': 0.1,
                'ai_risk_perception': 0.6,
                'ai_literacy': 0.3,
            },
        },
        {
            'pro_knowledge_name': 'AI教学实践培训',
            'actions': [
                {
                    'action_object': 'environment',
                    'action_attribute': 'research_support',
                    'action_experience': 0.5,
                },
                {
                    'action_object': 'school',
                    'action_attribute': 'school_orga_climate',
                    'action_experience': 0.5,
                },
            ],
            'reason': 'complexity',
            'target_object': 'teacher',
            'target_attribute': 'ai_literacy',
            'target_attribute_weight': {
                'ai_acceptance': 0.3,
                'ai_risk_perception': 0.1,
                'ai_literacy': 0.6,
            },
        },
    ])

    # 获取特定行为策略
    def get(self, reason, target_attribute, personal_value):
        # 0. 判断是否能够正确决策出策略
        is_right = 1
        # 1-1. 随机数[0,1], 若personal_value<random_value则行为决策无法按照reason进行, 大于则可以
        random_value = np.random.uniform(0, 0.8)
        # 1-2. 不使用随机数, 而是使用阈值, 如0.5作为分割线, 大于0.5的可以正确, 小于0.5的不能
        # random_value = 0.5
        # print('personal value:', personal_value)
        if personal_value < random_value:
            is_right = 0  # 不是正确决策, 而是随机的
            reason = np.random.choice(['private', 'ethics', 'complexity'])
        pro_knowledge = np.array([])
        # 2. 若问题为数据隐私private
        if reason == 'private':
            # 1-1. 获取所有的程序性知识
            pro_knowledge = self.__pro_knowledge_private
            # 1-2. 在所有程序性知识中获取对应attribute的（教师三属性之一）
            for knowledge in pro_knowledge:
                if knowledge['target_attribute'] == target_attribute:
                    return knowledge, is_right
        elif reason == 'ethics':
            # 2-1
            pro_knowledge = self.__pro_knowledge_ethics
            # 2-2
            for knowledge in pro_knowledge:
                if knowledge['target_attribute'] == target_attribute:
                    return knowledge, is_right
        elif reason == 'complexity':
            # 3-1
            pro_knowledge = self.__pro_knowledge_complexity
            # 3-2
            for knowledge in pro_knowledge:
                if knowledge['target_attribute'] == target_attribute:
                    return knowledge, is_right
