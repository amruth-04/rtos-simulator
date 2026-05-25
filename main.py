from scheduler.task import Task, TaskState
from scheduler.scheduler import Scheduler
from scheduler.mutex import Mutex


# Create scheduler
scheduler = Scheduler()

# Create tasks
task1 = Task("TaskA", priority=1, burst_time=5)
task2 = Task("TaskB", priority=2, burst_time=5)

# Create resources
uart_mutex = Mutex("UART")
spi_mutex = Mutex("SPI")


# Initial ownership
uart_mutex.acquire(task1)
spi_mutex.acquire(task2)

print(f"{task1.name} acquired UART")
print(f"{task2.name} acquired SPI")


# Deadlock condition
print("\nDeadlock Scenario:")

# TaskA wants SPI
if not spi_mutex.acquire(task1):

    print(f"{task1.name} BLOCKED waiting for SPI")

    task1.state = TaskState.BLOCKED


# TaskB wants UART
if not uart_mutex.acquire(task2):

    print(f"{task2.name} BLOCKED waiting for UART")

    task2.state = TaskState.BLOCKED


# Add tasks
scheduler.add_task(task1)
scheduler.add_task(task2)

# Run scheduler
scheduler.run()