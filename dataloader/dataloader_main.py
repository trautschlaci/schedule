import xlrd
from possibility_graph.graph import Graph
from dataloader.student_sheet_loader import load_student_sheet, cross_out_lengths
from dataloader.instructor_sheet_loader import load_instructor_sheet, cross_out_hours
from dataloader.course_sheet_loader import load_course_sheet
from dataloader.weak_group_generator import generate_weak_groups
from dataloader.ruleloader import add_rules
from time import process_time


def load_data(excel_path):
    t1_start = process_time()

    graph = Graph()

    wb = xlrd.open_workbook(excel_path)
    student_sheet = wb.sheet_by_index(0)
    instructor_sheet = wb.sheet_by_index(1)
    course_sheet = wb.sheet_by_index(2)

    load_student_sheet(graph, student_sheet)
    load_instructor_sheet(graph, instructor_sheet)
    load_course_sheet(graph, course_sheet)

    generate_weak_groups(graph)
    add_rules(graph)

    t1_stop = process_time()
    print("Load time:", t1_stop - t1_start)
    t1_start = process_time()

    cross_out_lengths(graph)
    graph.delete_group("Length")

    cross_out_hours(graph, instructor_sheet)
    graph.delete_group("Hour")

    t1_stop = process_time()
    print("Cross-out time:", t1_stop - t1_start)

    return graph
