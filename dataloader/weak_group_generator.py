from possibility_graph.graph import Graph


def generate_weak_groups(graph: Graph):
    generate_exams(graph)
    generate_blocks(graph)


def generate_exams(graph: Graph):
    length_group = graph.get_group("Length")

    possible_lengths = []
    for length_node in length_group.nodes.values():
        length = int(length_node.name)
        possible_lengths.append(length)

    exam_group = graph.add_group("Exam", True)

    generate_length_entities(graph, exam_group, possible_lengths)

    all_to_all_groups = [
        graph.get_group("Role"),
        graph.get_group("Course"),
        graph.get_group("Instructor"),
        graph.get_group("Major"),
        graph.get_group("Student"),
        graph.get_group("Level")
    ]

    for exam_node in exam_group.nodes.values():
        for group in all_to_all_groups:
            group.add_edge_to_all_nodes(exam_node)

        for length_node in length_group.nodes.values():
            length = int(length_node.name)
            if len(exam_node.edges["Minute"])*5 == length:
                graph.add_edge(exam_node, length_node)


def generate_blocks(graph: Graph):
    min_exam_number = 1
    max_exam_number = 6
    am_block_max_end_time = (13, 00)
    pm_block_min_start_time = (12, 10)

    block_group = graph.add_group("Block", True)

    role_group = graph.get_group("Role")
    major_group = graph.get_group("Major")

    president_node = role_group.get_node("President")
    secretary_node = role_group.get_node("Secretary")

    possible_block_lengths = generate_block_lengths(graph, min_exam_number, max_exam_number)
    generate_length_entities(graph, block_group, possible_block_lengths, min_start_time=pm_block_min_start_time)
    generate_length_entities(graph, block_group, possible_block_lengths, max_end_time=am_block_max_end_time)

    addable_instructors = get_block_instructors(graph, president_node, secretary_node)

    for block_node in block_group.nodes.values():
        graph.add_edge(block_node, president_node)
        graph.add_edge(block_node, secretary_node)

        for instructor_node in addable_instructors:
            graph.add_edge(block_node, instructor_node)

        major_group.add_edge_to_all_nodes(block_node)

        add_exams_to_block_node(graph, block_node)


def generate_length_entities(graph, group, possible_lengths, min_start_time=None, max_end_time=None):
    minute_group = graph.get_group("Minute")

    for length in possible_lengths:
        for start_node in minute_group.nodes.values():
            start_name = start_node.name
            start_split = start_name.split(" ")
            start_min_str = start_split[1]

            minute = int(start_min_str[-2:])
            hour = int(start_min_str[:-3])
            end_hour, end_minute = step_minute(hour, minute, length)

            if min_start_time is not None and compare_times((hour, minute), min_start_time) < 0:
                continue
            if max_end_time is not None and compare_times((end_hour, end_minute), max_end_time) > 0:
                continue

            can_be_held = True
            minute_nodes = [start_node]
            for _ in range(length // 5 - 1):
                hour, minute = step_minute(hour, minute, 5)
                next_min_str = create_min_str(hour, minute)
                next_name = f'{start_split[0]} {next_min_str}'
                minute_node = minute_group.nodes.get(next_name, None)
                if minute_node is None:
                    can_be_held = False
                    break
                minute_nodes.append(minute_node)

            if not can_be_held:
                continue

            end_min_str = create_min_str(end_hour, end_minute)
            node_name = f'{start_name}-{end_min_str}'
            node = group.add_node(node_name)

            for minute_node in minute_nodes:
                graph.add_edge(node, minute_node)


def generate_block_lengths(graph, min_exam_number, max_exam_number):
    length_group = graph.get_group("Length")

    block_lengths_dict = {0: {0}}

    for i in range(1, max_exam_number+1):
        block_lengths_dict[i] = set()
        for length in length_group.nodes.values():
            exam_length = int(length.name)
            for b_l in block_lengths_dict[i-1]:
                block_lengths_dict[i].add(b_l + exam_length)

    possible_block_lengths = set()
    for i in range(min_exam_number, max_exam_number + 1):
        possible_block_lengths.update(block_lengths_dict[i])

    return possible_block_lengths


def get_block_instructors(graph, president_node, secretary_node):
    instructor_group = graph.get_group("Instructor")
    addable_instructors = []
    for instructor_node in instructor_group.nodes.values():
        roles = instructor_node.edges.get("Role", set())
        if president_node in roles or secretary_node in roles:
            addable_instructors.append(instructor_node)
    return addable_instructors


def add_exams_to_block_node(graph, block_node):
    exam_group = graph.get_group("Exam")

    own_minutes = block_node.edges.get("Minute", set())
    for exam_node in exam_group.nodes.values():
        exam_minutes = exam_node.edges.get("Minute", set())
        intersect = True
        for minute in exam_minutes:
            if minute not in own_minutes:
                intersect = False
                break
        if intersect:
            graph.add_edge(block_node, exam_node)


def step_minute(hour, minute, step):
    minute += step
    while minute >= 60:
        hour += 1
        minute -= 60
    return hour, minute


def compare_times(time1, time2):
    if time1[0] == time2[0]:
        return time1[1] - time2[1]
    else:
        return time1[0] - time2[0]


def create_min_str(hour, minute):
    minute_str = '%02d' % minute
    return f'{hour}:{minute_str}'
