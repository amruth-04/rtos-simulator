import time


def round_robin_simulation():

    execution = [

        ("TaskA", "RUNNING"),
        ("TaskB", "RUNNING"),
        ("TaskC", "RUNNING"),

        ("TaskA", "RUNNING"),
        ("TaskB", "RUNNING"),

        ("TaskC", "FINISHED"),

        ("TaskA", "FINISHED"),
        ("TaskB", "FINISHED")
    ]

    for item in execution:

        time.sleep(1)

        yield item


def fcfs_simulation():

    execution = [

        ("TaskA", "RUNNING"),
        ("TaskA", "RUNNING"),
        ("TaskA", "FINISHED"),

        ("TaskB", "RUNNING"),
        ("TaskB", "FINISHED"),

        ("TaskC", "RUNNING"),
        ("TaskC", "FINISHED")
    ]

    for item in execution:

        time.sleep(1)

        yield item


def sjf_simulation():

    execution = [

        ("TaskC", "RUNNING"),
        ("TaskC", "FINISHED"),

        ("TaskB", "RUNNING"),
        ("TaskB", "FINISHED"),

        ("TaskA", "RUNNING"),
        ("TaskA", "FINISHED")
    ]

    for item in execution:

        time.sleep(1)

        yield item


def priority_simulation():

    execution = [

        ("HighTask", "RUNNING"),
        ("HighTask", "FINISHED"),

        ("MediumTask", "RUNNING"),
        ("MediumTask", "FINISHED"),

        ("LowTask", "RUNNING"),
        ("LowTask", "FINISHED")
    ]

    for item in execution:

        time.sleep(1)

        yield item