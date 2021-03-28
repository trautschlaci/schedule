import xlrd
from time import process_time
from possibility_graph.graph import Graph
from dataloader.student_sheet_loader import load_student_sheet
from dataloader.instructor_sheet_loader import load_instructor_sheet
from dataloader.course_sheet_loader import load_course_sheet
from dataloader.weak_group_generator import generate_weak_groups
from dataloader.ruleloader import add_rules

t1_start = process_time()

graph = Graph()

loc = "Input.xls"
wb = xlrd.open_workbook(loc)
student_sheet = wb.sheet_by_index(0)
instructor_sheet = wb.sheet_by_index(1)
course_sheet = wb.sheet_by_index(2)

load_student_sheet(graph, student_sheet)
load_instructor_sheet(graph, instructor_sheet)
load_course_sheet(graph, course_sheet)
generate_weak_groups(graph)
add_rules(graph)

group = graph.get_group("Level")

t1_stop = process_time()

print("Elapsed time:", t1_stop-t1_start)
