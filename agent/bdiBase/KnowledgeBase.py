from agent.bdiBase.knowledge.epistemology import Epistemology
from agent.bdiBase.knowledge.decKnowledgeBase import DecKnowledgeBase
from agent.bdiBase.knowledge.proKnowledgeBase import ProKnowledgeBase
from agent.bdiBase.knowledge.conKnowledgeBase import ConKnowledgeBase

# * 知识库
class KnowledgeBase():
    epistemology = Epistemology(0)                      # 认识论基础
    dec_knowledge = DecKnowledgeBase()                  # 陈述性知识
    pro_knowledge = ProKnowledgeBase()                  # 程序性知识
    con_knowledge = ConKnowledgeBase()                  # 条件性知识

    def __init__(self, system_thinking):
        self.epistemology = Epistemology(system_thinking)
