import xml.dom.minidom as xmldom


class DecKnowledgeBase():
    __dec_knowledge = {}

    # 在陈述性知识XML中检索特定的陈述性知识
    # def get(self):
    #     xml_tree = xmldom.parse('./manage-multi-agent/agent/bdiBase/knowledge/knowledgeXML/conKnowledgeXML.xml')
    #     root = xml_tree.documentElement
    #     note_list = root.getElementsByTagName('note')
    #     for note in note_list:
    #         print('----- Note -----')
    #         # 获取每个属性
    #         title = note.getElementsByTagName('heading')[0]
    #         print('Title:', title.childNodes[0].data)
    #         writer = note.getElementsByTagName('from')[0]
    #         print('From:', writer.firstChild.data)
    #         getter = note.getElementsByTagName('to')[0]
    #         print('To:', getter.firstChild.data)
    #         body = note.getElementsByTagName('body')[0]
    #         print('Content:', body.firstChild.data)
    #         print('----- End Note -----')
    def get(self):
        return self.__dec_knowledge


    # 更新陈述性知识XML中的信息: 感知行为(一般信息的感知+反馈信息的感知)
    def update(self, new_dec_knowledge):
        self.__dec_knowledge = new_dec_knowledge
        # print('new dec knowledge =>', self.__dec_knowledge)
        # for new_info in new_dec_knowledge:
        #     already_exist_knowledge = 0
        #     for old_info in self.__dec_knowledge:
        #         # 如果该知识点已经存在已有的陈述性知识中，则替换
        #         if new_info == old_info:
        #             already_exist_knowledge = 1
        #             self.__dec_knowledge[old_info] = new_dec_knowledge[new_info]
        #         # 如果已经发现存在且替换了，则停止循环
        #         if already_exist_knowledge == 1:
        #             break
        #     # 如果该知识点没有存在现有的陈述性知识中，则新增一个键值对
        #     if already_exist_knowledge == 0:
        #         self.__dec_knowledge[new_info] = new_dec_knowledge[new_info]
                
