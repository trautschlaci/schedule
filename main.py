from time import process_time
from dataloader.dataloader_main import load_data


t1_start = process_time()

loc = "Input.xls"

graph = load_data(loc)

graph.merge_groups("Exam", "Major")
graph.merge_groups("Block", "Major")
graph.delete_group("Major")

t1_stop = process_time()

print("Elapsed time:", t1_stop-t1_start)
print(len(graph.get_group("Exam").nodes))
print(len(graph.get_group("Block").nodes))
