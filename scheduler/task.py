from enum import Enum

class TaskState(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    FINISHED = "FINISHED"


class Task:
    def __init__(self, name, priority, burst_time):
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.state = TaskState.READY

    def run(self):

        if self.remaining_time > 0:
            self.remaining_time -= 1

        if self.remaining_time == 0:
            self.state = TaskState.FINISHED