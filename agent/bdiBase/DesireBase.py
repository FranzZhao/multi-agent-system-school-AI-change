
# * 愿望库
class DesireBase():
    __object = ''           # 愿望所致对象
    __attribute = ''        # 希望改变对象的属性
    __reason = ''           # 问题的原因, 即愿望所要解决的问题的原因所在
    __goal = 0              # 目标, 即改变对象属性值的情况

    # 更新愿望
    def update(self, object, attribute, reason, goal):
        self.__object = object
        self.__attribute = attribute
        self.__reason = reason
        self.__goal = goal

    # 获取当前愿望
    def get(self):
        return {
            'object': self.__object,
            'attribute': self.__attribute,
            'reason': self.__reason,
            'goal': self.__goal
        }