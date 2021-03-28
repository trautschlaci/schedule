from possibility_graph.rule import RuleType


def add_rules(graph):
    edge_rules = {frozenset(["Student", "Exam"]): RuleType.Red,
                  frozenset(["Student", "Course"]): RuleType.Pair,
                  frozenset(["Exam", "Course"]): RuleType.Green}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Exam", "Major"]): RuleType.Green,
                  frozenset(["Student", "Major"]): RuleType.Pair,
                  frozenset(["Exam", "Student"]): RuleType.Red}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Exam", "Course"]): RuleType.Green,
                  frozenset(["Course", "Instructor"]): RuleType.Green,
                  frozenset(["Exam", "Instructor"]): RuleType.Normal}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Exam", "Major"]): RuleType.Green,
                  frozenset(["Major", "Instructor"]): RuleType.Green,
                  frozenset(["Exam", "Instructor"]): RuleType.Green}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Exam", "Role"]): RuleType.Pair,
                  frozenset(["Exam", "Instructor"]): RuleType.Normal,
                  frozenset(["Instructor", "Role"]): RuleType.Green}

    node_rules = {"Exam": RuleType.Red,
                  "Instructor": RuleType.Distinct}

    graph.add_rule(edge_rules, node_rules)

    edge_rules = {frozenset(["Exam", "Student"]): RuleType.Normal,
                  frozenset(["Student", "Instructor"]): RuleType.Green,
                  frozenset(["Exam", "Instructor"]): RuleType.Normal}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Exam", "Minute"]): RuleType.Pair,
                  frozenset(["Minute", "Instructor"]): RuleType.Green,
                  frozenset(["Exam", "Instructor"]): RuleType.Red}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Student", "Length"]): RuleType.Normal,
                  frozenset(["Student", "Exam"]): RuleType.Red,
                  frozenset(["Exam", "Length"]): RuleType.Pair}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Student", "Level"]): RuleType.Pair,
                  frozenset(["Student", "Exam"]): RuleType.Red,
                  frozenset(["Exam", "Level"]): RuleType.Green}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Exam", "Block"]): RuleType.Normal,
                  frozenset(["Exam", "Minute"]): RuleType.Normal,
                  frozenset(["Block", "Minute"]): RuleType.Pair}

    node_rules = {"Block": RuleType.Red}

    graph.add_rule(edge_rules, node_rules)

    edge_rules = {frozenset(["Exam", "Block"]): RuleType.Green,
                  frozenset(["Exam", "Major"]): RuleType.Green,
                  frozenset(["Block", "Major"]): RuleType.Green}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Instructor", "Block"]): RuleType.Red,
                  frozenset(["Instructor", "Minute"]): RuleType.Normal,
                  frozenset(["Block", "Minute"]): RuleType.Pair}

    graph.add_rule(edge_rules)

    edge_rules = {frozenset(["Block", "Role"]): RuleType.Pair,
                  frozenset(["Block", "Instructor"]): RuleType.Green,
                  frozenset(["Instructor", "Role"]): RuleType.Normal}

    node_rules = {"Block": RuleType.Red,
                  "Instructor": RuleType.Distinct}

    graph.add_rule(edge_rules, node_rules)

    edge_rules = {frozenset(["Instructor", "Major"]): RuleType.Normal,
                  frozenset(["Instructor", "Block"]): RuleType.Green,
                  frozenset(["Block", "Major"]): RuleType.Green}

    graph.add_rule(edge_rules)
