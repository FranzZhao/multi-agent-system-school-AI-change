from model import *
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import TextElement, ChartModule, BarChartModule
from mesa.visualization.UserParam import UserSettableParameter

RED = "#ff8e8e"
BLUE = "#4682b4"
GREEN = "#5f9f5f"
ORANGE = "#ffb54a"
SKY = "#65b1c7"
YELLOW = "#ffff82"
BROWN = "#8a6d3b"
GREY = "#767676"
BLACK = "black"
PURPLE = "purple"

# 管理者控制的变量
chart_control = ChartModule([
    {"Label": "school_orga_climate", "Color": BLUE},
    {"Label": "ai_env", "Color": ORANGE},
    {"Label": "incentive_policy", "Color": GREEN},
    {"Label": "env.policy_support", "Color": RED},
    {"Label": "env.research_support", "Color": BROWN},
    {"Label": "env.enterprise_support", "Color": SKY},
])

# 教师属性变化折线图
chart_teacher = ChartModule([
    {"Label": "teachers.ai_acceptance", "Color": BLUE},
    {"Label": "teachers.ai_risk_perception", "Color": ORANGE},
    {"Label": "teachers.ai_literacy", "Color": GREEN},
    {"Label": "teachers.total_performance", "Color": RED},
])

# 学生属性变化
chart_student = ChartModule([
    {"Label": "students.ai_literacy", "Color": BLUE},
    {"Label": "students.motivation", "Color": RED},
    {"Label": "students.pressure", "Color": GREEN},
])

# 管理者属性变化
chart_manager = ChartModule([
    {"Label": "manager_system_thinking", "Color": BLUE},
    {"Label": "manager_active_degree", "Color": RED},
])

# 干预策略对象-柱状图
strategy_target_bar_chart = BarChartModule([
    {"Label": "strategy_school_orga_climate", "Color": BLUE},
    {"Label": "strategy_ai_env", "Color": ORANGE},
    {"Label": "strategy_incentive_policy", "Color": RED},
    {"Label": "strategy_policy_support", "Color": GREEN},
    {"Label": "strategy_research_support", "Color": BROWN},
    {"Label": "strategy_enterprise_support", "Color": SKY},
])

# 干预策略-柱状图
strategy_name_bar_chart = BarChartModule([
    {"Label": "strategy_private_ai_acceptance", "Color": BLUE},
    {"Label": "strategy_private_ai_risk", "Color": RED},
    {"Label": "strategy_private_ai_literacy", "Color": GREEN},
    {"Label": "strategy_ethics_ai_acceptance", "Color": ORANGE},
    {"Label": "strategy_ethics_ai_risk", "Color": SKY},
    {"Label": "strategy_ethics_ai_literacy", "Color": BROWN},
    {"Label": "strategy_complexity_ai_acceptance", "Color": GREY},
    {"Label": "strategy_complexity_ai_risk", "Color": BLACK},
    {"Label": "strategy_complexity_ai_literacy", "Color": PURPLE},
])

# 模型参数
# school_ai_vision, env, pattern, initial_manager_value, initial_teacher_value
model_params = {
    "school_ai_vision": UserSettableParameter("slider", "school AI vision", 0.8, 0.00, 1.00, 0.01),
    "env": UserSettableParameter("slider", "environment support", 0.5, 0.00, 1.00, 0.01),
    "initial_manager_value": UserSettableParameter("slider", "manager initial", 0.5, 0.00, 1.00, 0.01),
    "initial_teacher_value": UserSettableParameter("slider", "teacher initial", 0.5, 0.00, 1.00, 0.01),
    "pattern": UserSettableParameter('choice', 'top-down:bottom:up pattern', value='pattern1',
                                     choices=['pattern1', 'pattern2', 'pattern3', 'pattern4', 'pattern5'])
}


# 文本信息输出
class Text(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "管理者系统思考能力：" + str(model.manager_ave_system_thinking) + \
            "<br> 管理者活跃程度：" + str(model.manager_ave_active_degree)


# 实例化文本信息
text = Text()

# 实例化服务器
server = ModularServer(
    SchoolModel,
    [chart_teacher, chart_student, chart_manager,
        strategy_target_bar_chart, strategy_name_bar_chart, chart_control],
    "School AI Change",
    model_params
)

server.port = 8522
server.launch()
