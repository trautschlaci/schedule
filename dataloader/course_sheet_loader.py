from possibility_graph.graph import Graph


def load_course_sheet(graph: Graph, sheet):
    instructor_group = graph.add_group("Instructor")
    course_group = graph.add_group("Course")

    substitutes_info = {}

    for c in range(sheet.ncols):
        course_str = sheet.cell_value(0, c)
        course_node = course_group.add_node(course_str)

        for r in range(2, sheet.nrows):
            instructor_str = sheet.cell_value(r, c)

            if len(instructor_str) == 0:
                continue

            if instructor_str[:2] == "M-":
                instructor_str = instructor_str[2:]
                edge = frozenset([course_str, instructor_str])
                substitutes_info[edge] = True

            instructor_node = instructor_group.add_node(instructor_str)
            graph.add_edge(course_node, instructor_node)

    graph.infos["Substitutes"] = substitutes_info
