from possibility_graph.graph import Graph


def load_student_sheet(graph: Graph, sheet):
    student_group = graph.add_group("Student")
    level_group = graph.add_group("Level")
    major_group = graph.add_group("Major")
    instructor_group = graph.add_group("Instructor")
    course_group = graph.add_group("Course")
    length_group = graph.add_group("Length")

    length_node_1 = length_group.add_node("40")
    length_node_2 = length_group.add_node("45")

    for r in range(1, sheet.nrows):
        neptun_str = sheet.cell_value(r, 1)
        student_node = student_group.add_node(neptun_str)

        graph.add_edge(student_node, length_node_1)
        graph.add_edge(student_node, length_node_2)

        level_str = sheet.cell_value(r, 2)
        level_node = level_group.add_node(level_str)
        graph.add_edge(student_node, level_node)

        major_str = sheet.cell_value(r, 3)
        if major_str == "mérnökinformatikus":
            major_str = "CS"
        elif major_str == "villamosmérnöki":
            major_str = "EE"
        major_node = major_group.add_node(major_str)
        graph.add_edge(student_node, major_node)

        supervisor_str = sheet.cell_value(r, 4)
        supervisor_node = instructor_group.add_node(supervisor_str)
        graph.add_edge(student_node, supervisor_node)

        course_str_1 = sheet.cell_value(r, 6)
        course_node_1 = course_group.add_node(course_str_1)
        graph.add_edge(student_node, course_node_1)

        course_str_2 = sheet.cell_value(r, 8)
        if len(course_str_2) > 0:
            course_node_2 = course_group.add_node(course_str_2)
            graph.add_edge(student_node, course_node_2)


def cross_out_lengths(graph: Graph):
    student_group = graph.get_group("Student")
    length_group = graph.get_group("Length")

    length_node_40 = length_group.get_node("40")
    length_node_45 = length_group.get_node("45")

    for student_node in student_group.nodes.values():
        if len(student_node.edges["Course"]) == 2:
            graph.cross_out_edge(student_node, length_node_40)
        else:
            graph.cross_out_edge(student_node, length_node_45)
