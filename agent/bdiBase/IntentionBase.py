
# * 意图库
class IntentionBase():
    __action_name = ''          # 意图行动策略的名称
    __action_object = ''        # 意图的行动干预对象
    __action_attribute = ''     # 干预行动
    __action_reason = ''        # 行动原因：数据隐私、算法伦理、AI复杂性
    __action_weights = 0         # 意图行动策略的权重

    # 更新意图
    def update(self, action_name, action_object, action_attribute, action_reason, action_weights):
        self.__action_name = action_name
        self.__action_object = action_object
        self.__action_attribute = action_attribute
        self.__action_reason = action_reason
        self.__action_weights = action_weights

    # 获取当前意图
    def get(self):
        return {
            'name': self.__action_name,
            'object': self.__action_object,
            'attribute': self.__action_attribute,
            'reason': self.__action_reason,
            'weights': self.__action_weights,
        }
