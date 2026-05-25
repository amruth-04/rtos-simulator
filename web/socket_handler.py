from scheduler.simulator import (
    round_robin_simulation,
    fcfs_simulation,
    sjf_simulation,
    priority_simulation
)


def run_simulation(socketio, algorithm):

    if algorithm == "Round Robin":
        simulation = round_robin_simulation()
    elif algorithm == "FCFS":
        simulation = fcfs_simulation()
    elif algorithm == "SJF":
        simulation = sjf_simulation()
    else:
        simulation = priority_simulation()

    completed_tasks = 0
    context_switches = 0
    cpu_utilization = 0
    previous_task = None

    for task_name, state in simulation:

        if previous_task != task_name:
            context_switches += 1
        previous_task = task_name

        if state == "FINISHED":
            completed_tasks += 1

        cpu_utilization = min(cpu_utilization + 10, 100)

        socketio.emit("task_update", {
            "name": task_name,
            "state": state
        })

        socketio.emit("timeline_update", {
            "task": task_name
        })

        socketio.emit("metrics_update", {
            "cpu_utilization": f"{cpu_utilization}%",
            "context_switches": context_switches,
            "completed_tasks": completed_tasks,
            "algorithm": algorithm
        })

        print(task_name, state)

        socketio.sleep(1)