def log_execution(schedule, filename="execution_log.txt"):
    with open(filename, "w") as f:
        f.write("Task\tStart\tEnd\tDuration\n")
        for task_name, start, end in schedule:
            duration = end - start
            f.write(f"{task_name}\t{start}\t{end}\t{duration}\n")