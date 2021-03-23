import xlrd
from possibility_graph.graph import Graph
from possibility_graph.rule import RuleType


loc = "Input.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

graph = Graph()
groups = ["Lecturer", "Exam", "Course", "Major", "Student", "Length", "Level", "Role", "Block", "Minute"]
graph.add_groups(groups)

student_group = graph.get_group("Student")
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
    graph.add_edge(student_node, major_node)


exam_group = graph.get_group("Exam")
exam_node = exam_group.add_node("Test")

major_node = major_group.get_node("BSc")
#student_node = student_group.get_node("")

for s_n in student_group.nodes.values():
    graph.add_edge(s_n, exam_node)

for m_n in major_group.nodes.values():
    graph.add_edge(m_n, exam_node)

edge_rules = {frozenset(["Exam", "Major"]): RuleType.Green,
              frozenset(["Student", "Major"]): RuleType.Pair,
              frozenset(["Exam", "Student"]): RuleType.Red}

graph.add_rule(edge_rules)

graph.cross_out_edge(exam_node, major_node)
#graph.cross_out_edge(exam_node, student_node)

print(exam_node.edges)

