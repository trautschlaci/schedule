import xlrd
from possibility_graph.graph import Graph
from possibility_graph.rule import RuleType


loc = "Input.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

graph = Graph()
groups = ["Lecturer", "Exam", "Course", "Major", "Student", "Length", "Level", "Role", "Block", "Minute"]
graph.add_groups(groups)

"""student_group = graph.get_group("Student")
neptun_list = sheet.col_values(1, 1)
student_group.add_nodes(neptun_list)

major_group = graph.get_group("Major")
major_list = sheet.col_values(2, 1)
major_group.add_nodes(major_list)

for i in range(1, sheet.nrows):
    neptun_str = sheet.cell_value(i, 1)
    major_str = sheet.cell_value(i, 2)
    student_node = student_group.get_node(neptun_str)
    major_node = major_group.get_node(major_str)
    graph.add_edge(student_node, major_node)"""


exam_group = graph.get_group("Exam")
exam_node = exam_group.add_node("Test")

"""for s_n in student_group.nodes.values():
    graph.add_edge(s_n, exam_node)

for m_n in major_group.nodes.values():
    graph.add_edge(m_n, exam_node)"""

edge_rules = {frozenset(["Exam", "Major"]): RuleType.Green,
              frozenset(["Student", "Major"]): RuleType.Pair,
              frozenset(["Exam", "Student"]): RuleType.Red}

graph.add_rule(edge_rules)

edge_rules = {frozenset(["Exam", "Role"]): RuleType.Pair,
              frozenset(["Exam", "Lecturer"]): RuleType.Normal,
              frozenset(["Lecturer", "Role"]): RuleType.Green}

node_rules = {"Exam": RuleType.Red,
              "Lecturer": RuleType.Pair}

graph.add_rule(edge_rules, node_rules)


role_group = graph.get_group("Role")
role_node_1 = role_group.add_node("President")
role_node_2 = role_group.add_node("Major")
role_node_3 = role_group.add_node("Secretary")

lecturer_group = graph.get_group("Lecturer")
lecturer_node_1 = lecturer_group.add_node("A")
lecturer_node_2 = lecturer_group.add_node("B")
lecturer_node_3 = lecturer_group.add_node("C")
lecturer_node_4 = lecturer_group.add_node("D")

for r_n in role_group.nodes.values():
    graph.add_edge(r_n, exam_node)

for l_n in lecturer_group.nodes.values():
    graph.add_edge(l_n, exam_node)

graph.add_edge(role_node_1, lecturer_node_1)
graph.add_edge(role_node_1, lecturer_node_2)
graph.add_edge(role_node_2, lecturer_node_1)
graph.add_edge(role_node_2, lecturer_node_2)
graph.add_edge(role_node_3, lecturer_node_1)
graph.add_edge(role_node_3, lecturer_node_2)
graph.add_edge(role_node_1, lecturer_node_4)

graph.cross_out_edge(lecturer_node_4, exam_node)

print(exam_node.edges)
