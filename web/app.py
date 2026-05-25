from flask import Flask, render_template
from flask_socketio import SocketIO

import threading

from web.socket_handler import run_simulation


app = Flask(__name__)

socketio = SocketIO(app, async_mode="threading")


# Default algorithm
selected_algorithm = "Round Robin"


@app.route("/")
def index():

    tasks = [

        {"name": "TaskA", "state": "READY"},
        {"name": "TaskB", "state": "READY"},
        {"name": "TaskC", "state": "READY"}
    ]

    resources = [

        {"resource": "UART", "owner": "TaskA"},

        {"resource": "SPI", "owner": "TaskB"}
    ]

    # Scheduler metrics
    metrics = {

        "cpu_utilization": "87%",

        "context_switches": 12,

        "completed_tasks": 0,

        "algorithm": selected_algorithm
    }

    return render_template(

        "index.html",

        tasks=tasks,

        resources=resources,

        metrics=metrics,

        timeline=[],

        deadlock=False
    )


# Handle algorithm change
@socketio.on("algorithm_change")
def handle_algorithm(data):

    global selected_algorithm

    selected_algorithm = data["algorithm"]

    print("Selected Algorithm:", selected_algorithm)

    # Start selected simulation
    threading.Thread(

        target=run_simulation,

        args=(socketio, selected_algorithm),

        daemon=True

    ).start()


if __name__ == "__main__":

    socketio.run(

        app,

        debug=True,

        allow_unsafe_werkzeug=True
    )