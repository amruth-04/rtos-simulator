from scheduler.task import TaskState


class Scheduler:

    def __init__(self):

        self.tasks = []
        self.time = 0
        self.quantum = 2

        # Keeps track of current task index
        self.current_index = 0
        self.timeline = []

    def add_task(self, task):

        self.tasks.append(task)

    def get_next_task(self):

        ready_tasks = [

            task for task in self.tasks

            if task.state != TaskState.FINISHED
        ]

        if not ready_tasks:
            return None

        # Round Robin rotation
        task = ready_tasks[self.current_index % len(ready_tasks)]

        self.current_index += 1

        return task

    def run(self):

        while True:

            current_task = self.get_next_task()

            if current_task is None:

                print("\nAll tasks completed.")
                print("\nCPU Timeline:")
                for i, task in enumerate(self.timeline):

                    print(f"Time {i}: {task}")
                break

            current_task.state = TaskState.RUNNING

            print(f"\nRunning: {current_task.name}")

            # Run task for quantum
            for _ in range(self.quantum):

                if current_task.remaining_time == 0:
                    break

                current_task.run()
                self.timeline.append(current_task.name)

                print(
                    f"Time: {self.time} | "
                    f"{current_task.name} | "
                    f"Remaining: {current_task.remaining_time}"
                )

                self.time += 1

            # Return task to READY state
            if current_task.state != TaskState.FINISHED:

                current_task.state = TaskState.READY