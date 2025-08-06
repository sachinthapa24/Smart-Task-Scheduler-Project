import threading
import time

def round_robin(tasks, time_quantum):
    tasks.sort(key=lambda t: t.arrival_time)
    time_elapsed = 0
    result = []
    queue = []
    i = 0
    n = len(tasks)

    while i < n or queue:
        while i < n and tasks[i].arrival_time <= time_elapsed:
            queue.append(tasks[i])
            i += 1
        if queue:
            current_task = queue.pop(0)
            exec_time = min(time_quantum, current_task.remaining_time)
            thread = threading.Thread(target=current_task.run)
            thread.start()
            thread.join(exec_time)
            current_task.remaining_time -= exec_time
            result.append((current_task.name, time_elapsed, time_elapsed + exec_time))
            time_elapsed += exec_time
            while i < n and tasks[i].arrival_time <= time_elapsed:
                queue.append(tasks[i])
                i += 1
            if current_task.remaining_time > 0:
                queue.append(current_task)
        else:
            if i < n:
                time_elapsed = tasks[i].arrival_time
    return result

def sjf(tasks):
    tasks.sort(key=lambda t: t.arrival_time)
    time_elapsed = 0
    result = []
    ready_queue = []

    while tasks or ready_queue:
        while tasks and tasks[0].arrival_time <= time_elapsed:
            ready_queue.append(tasks.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda t: t.burst_time)
            current_task = ready_queue.pop(0)
            thread = threading.Thread(target=current_task.run)
            thread.start()
            thread.join(current_task.burst_time)
            result.append((current_task.name, time_elapsed, time_elapsed + current_task.burst_time))
            time_elapsed += current_task.burst_time
        else:
            time_elapsed = tasks[0].arrival_time
    return result

def priority_scheduling(tasks):
    tasks.sort(key=lambda t: t.arrival_time)
    time_elapsed = 0
    result = []
    ready_queue = []

    while tasks or ready_queue:
        # Move tasks that have arrived into the ready queue
        while tasks and tasks[0].arrival_time <= time_elapsed:
            ready_queue.append(tasks.pop(0))

        if ready_queue:
            # Apply aging: Increase priority (i.e., decrease priority value) for tasks waiting in ready queue
            for task in ready_queue:
                task.waiting_time += 1
                if task.waiting_time % 5 == 0:  # aging interval: every 5 units of wait time
                    task.priority = max(task.priority - 1, 1)

            # Sort by priority (lower number = higher priority)
            ready_queue.sort(key=lambda t: t.priority)
            current_task = ready_queue.pop(0)

            # Reset waiting time since it's being executed now
            current_task.waiting_time = 0

            # Execute the task (simulate thread)
            thread = threading.Thread(target=current_task.run)
            thread.start()
            thread.join(current_task.burst_time)

            result.append((current_task.name, time_elapsed, time_elapsed + current_task.burst_time))
            time_elapsed += current_task.burst_time
        else:
            time_elapsed = tasks[0].arrival_time

    return result
