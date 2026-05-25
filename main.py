from scheduler.task import Task
from scheduler.scheduler import Scheduler

scheduler = Scheduler()

scheduler.add_task(Task("TaskA", priority=1, burst_time=5))
scheduler.add_task(Task("TaskB", priority=3, burst_time=8))
scheduler.add_task(Task("TaskC", priority=2, burst_time=4))

scheduler.run()