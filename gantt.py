import matplotlib.pyplot as plt

def draw_gantt_chart(schedule, output_file=None):
    fig, gnt = plt.subplots()
    gnt.set_title("Gantt Chart - Task Execution Timeline")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Tasks")

    task_names = list(set([task[0] for task in schedule]))
    yticks = [i*10 for i in range(len(task_names))]
    gnt.set_yticks(yticks)
    gnt.set_yticklabels(task_names)
    gnt.grid(True)

    color_map = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']

    for i, task in enumerate(schedule):
        task_name, start, end = task
        y = yticks[task_names.index(task_name)]
        gnt.broken_barh([(start, end - start)], (y - 4, 8),
                        facecolors=color_map[i % len(color_map)])

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()