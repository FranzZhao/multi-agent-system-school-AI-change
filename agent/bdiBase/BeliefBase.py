
# * 信念库
class BeliefBase():
    __object = ''           # 感知对象
    __attribute = ''        # 感知对象的属性
    __value = 0             # 感知对象属性值
    __gap = 0               # 属性与愿景的差距
    __reason = ''           # 问题出现的原因
    __tendency = 0          # 信念倾向值

    # 更新信念
    def update(self, object, attribute, value, gap, reason, tendency):
        self.__object = object
        self.__attribute = attribute
        self.__value = value
        self.__gap = gap
        self.__reason = reason
        self.__tendency = tendency

    # 获取当前信念
    def get(self):
        return {
            'object': self.__object,
            'attribute': self.__attribute,
            'value': self.__value,
            'gap': self.__gap,
            'reason': self.__reason,
            'tendency': self.__tendency,
        }