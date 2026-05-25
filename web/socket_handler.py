from scheduler.simulator import (
    round_robin_simulation,
    fcfs_simulation,
    sjf_simulation,
    priority_simulation
)


def run_simulation(socketio, algorithm):

    # Select scheduler
    if algorithm == "Round Robin":

        simulation = round_robin_simulation()

    elif algorithm == "FCFS":

        simulation = fcfs_simulation()

    elif algorithm == "SJF":

        simulation = sjf_simulation()

    else:

        simulation = priority_simulation()

    # Metrics
    completed_tasks = 0
    context_switches = 0
    cpu_utilization = 0

    previous_task = None

    for task_name, state in simulation:

        # Context switch tracking
        if previous_task != task_name:

            context_switches += 1

        previous_task = task_name

        # Completed task tracking
        if state == "FINISHED":

            completed_tasks += 1

        # Fake CPU utilization growth
        cpu_utilization = min(

            cpu_utilization + 10,

            100
        )

        # Task state update
        socketio.emit(

            "task_update",

            {

                "name": task_name,
                "state": state
            }
        )

        # Timeline update
        socketio.emit(

            "timeline_update",

            {

                "task": task_name[0]
            }
        )

        # Live metrics update
        socketio.emit(

            "metrics_update",

            {

                "cpu_utilization": f"{cpu_utilization}%",

                "context_switches": context_switches,

                "completed_tasks": completed_tasks,

                "algorithm": algorithm
            }
        )

        print(task_name, state)