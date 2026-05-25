from scheduler.task import TaskState


class Scheduler:

    def __init__(self):

        self.tasks = []
        self.time = 0
        self.quantum = 2

        # Round Robin index
        self.current_index = 0

        # CPU execution history
        self.timeline = []

    def add_task(self, task):

        self.tasks.append(task)

    def get_next_task(self):

        # Ignore finished and blocked tasks
        ready_tasks = [

            task for task in self.tasks

            if task.state != TaskState.FINISHED
            and task.state != TaskState.BLOCKED
        ]

        if not ready_tasks:
            return None

        # Round Robin scheduling
        task = ready_tasks[self.current_index % len(ready_tasks)]

        self.current_index += 1

        return task

    def run(self):

        while True:

            current_task = self.get_next_task()

            # Nothing runnable
            if current_task is None:

                blocked_tasks = [

                    task for task in self.tasks

                    if task.state == TaskState.BLOCKED
                ]

                # Deadlock detection
                if len(blocked_tasks) > 0:

                    print("\nDEADLOCK DETECTED!")

                else:

                    print("\nAll runnable tasks completed.")

                print("\nCPU Timeline:")

                for i, task in enumerate(self.timeline):

                    print(f"Time {i}: {task}")

                print("\nFinal Task States:")

                for task in self.tasks:

                    print(
                        f"{task.name} | "
                        f"State: {task.state.value} | "
                        f"Remaining: {task.remaining_time}"
                    )

                break

            current_task.state = TaskState.RUNNING

            print(f"\nRunning: {current_task.name}")

            # Run task for quantum
            for _ in range(self.quantum):

                if current_task.remaining_time == 0:
                    break

                current_task.run()

                # Store execution history
                self.timeline.append(current_task.name)

                print(
                    f"Time: {self.time} | "
                    f"{current_task.name} | "
                    f"Remaining: {current_task.remaining_time}"
                )

                self.time += 1

            # Return unfinished tasks to READY
            if current_task.state != TaskState.FINISHED:

                current_task.state = TaskState.READY