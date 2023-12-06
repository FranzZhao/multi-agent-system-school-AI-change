
# * 外部环境
class Environment():
    def __init__(self, policy_support, research_support, enterprise_support):
        self.policy_support = {
            'private': policy_support,
            'ethics': policy_support,
            'complexity': policy_support,
        }                                           # 政府支持政策
        self.research_support = {
            'private': research_support,
            'ethics': research_support,
            'complexity': research_support,
        }                                           # 高校科研支持
        self.enterprise_support = {
            'private': enterprise_support,
            'ethics': enterprise_support,
            'complexity': enterprise_support,
        }                                           # 企业技术支持

    # 获取外部环境中属性的值
    def get(self, target_attribute):
        target_value = 0
        if target_attribute == 'policy_support':
            target_value = self.policy_support
        elif target_attribute == 'research_support':
            target_value = self.research_support
        elif target_attribute == 'enterprise_support':
            target_value = self.enterprise_support
        return target_value

    # 更新外部环境中属性的值: 学校寻求外部系统的支持
    def update(self, update_attribute, update_value):
        if update_attribute == 'policy_support':
            self.policy_support = update_value
        elif update_attribute == 'research_support':
            self.research_support = update_value
        elif update_attribute == 'enterprise_support':
            self.enterprise_support = update_value
