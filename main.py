from time import process_time
from dataloader.dataloader_main import load_data

loc = "Input.xls"

graph, load_time, cross_time = load_data(loc)

t1_start = process_time()

graph.merge_groups("Exam", "Level")
graph.delete_rules_with_group("Level")

graph.merge_groups("Exam", "Major")
graph.merge_groups("Block", "Major")
graph.delete_group("Major")

t1_stop = process_time()
clone_time = t1_stop-t1_start-graph.t_merge_cross

print(len(graph.get_group("Exam").nodes))
print(len(graph.get_group("Block").nodes))
print("Load time:", load_time)
print("Cross-out time:", cross_time)
print("Clone creation time:", clone_time)
print("Merge cross-out time:", graph.t_merge_cross)
print("All time:", load_time+cross_time+clone_time+graph.t_merge_cross)
