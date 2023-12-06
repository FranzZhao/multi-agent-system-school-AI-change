import xml.dom.minidom as xmldom

# python的基础路径是这个项目的根目录, 所以在引入的时候要从那里开始引入
xml_tree = xmldom.parse(
    './manage-multi-agent/agent/bdiBase/knowledge/knowledgeXML/conKnowledgeXML.xml')
root = xml_tree.documentElement

note_list = root.getElementsByTagName('note')

note1 = note_list[0]
# 标签名
print(note1.nodeName)
# 标签属性
note1_id = note1.getAttribute('id')
print(note1_id)
# 标签内的数据, 其中body只有一个, 所以是[0] -> getElementsByTagName返回的都是一个列表
note1_body = note1.getElementsByTagName('body')[0]
print(note1_body.firstChild.data)


# 遍历
for note in note_list:
    print('----- Note -----')
    # 获取每个属性
    title = note.getElementsByTagName('heading')[0]
    print('Title:', title.childNodes[0].data)
    writer = note.getElementsByTagName('from')[0]
    print('From:', writer.firstChild.data)
    getter = note.getElementsByTagName('to')[0]
    print('To:', getter.firstChild.data)
    body = note.getElementsByTagName('body')[0]
    print('Content:', body.firstChild.data)
