from possibility_graph.graph import Graph


def load_instructor_sheet(graph: Graph, sheet):
    load_instructor_info(graph, sheet)
    load_date_info(graph, sheet)


def load_instructor_info(graph, sheet):
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


def load_date_info(graph, sheet):
    minute_group = graph.add_group("Minute")
    hour_group = graph.add_group("Hour")
    instructor_group = graph.get_group("Instructor")

    actual_day = ""
    for c in range(6, sheet.ncols):
        day_str = sheet.cell_value(0, c)
        if len(day_str) > 0:
            actual_day = day_str[:11]

        hour_str = sheet.cell_value(1, c)
        date_hour_str = create_date_hour_str(actual_day, hour_str)
        hour_node = hour_group.add_node(date_hour_str)

        instructor_group.add_edge_to_all_nodes(hour_node)

        for i in range(12):
            minute = i*5
            date_str = create_full_date_str(actual_day, hour_str, minute)
            date_node = minute_group.add_node(date_str)

            graph.add_edge(hour_node, date_node)

            instructor_group.add_edge_to_all_nodes(date_node)


def cross_out_hours(graph: Graph, sheet):
    hour_group = graph.get_group("Hour")
    instructor_group = graph.get_group("Instructor")

    for r in range(2, sheet.nrows):
        name_str = sheet.cell_value(r, 0)
        instructor_node = instructor_group.get_node(name_str)

        actual_day = ""
        for c in range(6, sheet.ncols):
            day_str = sheet.cell_value(0, c)
            if len(day_str) > 0:
                actual_day = day_str[:11]

            if sheet.cell_value(r, c) != 'x':
                hour_str = sheet.cell_value(1, c)
                date_hour_str = create_date_hour_str(actual_day, hour_str)
                hour_node = hour_group.get_node(date_hour_str)

                graph.cross_out_edge(instructor_node, hour_node)


def create_date_hour_str(day_str, hour_str):
    return f'{day_str} {hour_str}'


def create_full_date_str(day_str, hour_str, minute):
    minute_str = '%02d' % minute
    return f'{day_str} {hour_str[:-2]}{minute_str}'
