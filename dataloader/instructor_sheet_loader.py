from possibility_graph.graph import Graph


def load_instructor_sheet(graph: Graph, sheet):
    instructor_group = graph.add_group("Instructor")
    major_group = graph.add_group("Major")
    role_group = graph.add_group("Role")

    cs_node = major_group.add_node("CS")
    ee_node = major_group.add_node("EE")

    president_node = role_group.add_node("President")
    member_node = role_group.add_node("Member")
    secretary_node = role_group.add_node("Secretary")

    for r in range(2, sheet.nrows):
        name_str = sheet.cell_value(r, 0)
        instructor_node = instructor_group.add_node(name_str)

        if sheet.cell_value(r, 1) == 'x':
            graph.add_edge(instructor_node, president_node)

        if sheet.cell_value(r, 2) == 'x':
            graph.add_edge(instructor_node, member_node)

        if sheet.cell_value(r, 3) == 'x':
            graph.add_edge(instructor_node, secretary_node)

        if sheet.cell_value(r, 4) == 'x':
            graph.add_edge(instructor_node, cs_node)

        if sheet.cell_value(r, 5) == 'x':
            graph.add_edge(instructor_node, ee_node)

    minute_group = graph.add_group("Minute")

    actual_day = ""
    for c in range(6, sheet.ncols):
        day_str = sheet.cell_value(0, c)
        if len(day_str) > 0:
            actual_day = day_str[:11]

        hour_str = sheet.cell_value(1, c)[:-2]
        for i in range(12):
            minute = i*5
            minute_str = '%02d' % minute
            date_str = f'{actual_day} {hour_str}{minute_str}'
            date_node = minute_group.add_node(date_str)

            for instructor_node in instructor_group.nodes.values():
                graph.add_edge(instructor_node, date_node)
