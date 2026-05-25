from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time

from web.socket_handler import run_simulation

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret!"

socketio = SocketIO(app)

# Current scheduling algorithm

current_algorithm = "Round Robin"

# Dummy tasks

tasks = [

    {

        "name": "TaskA",
        "state": "READY"
    },

    {

        "name": "TaskB",
        "state": "READY"
    },

    {

        "name": "TaskC",
        "state": "READY"
    }
]

# Dummy resources

resources = [

    {

        "resource": "Mutex 1",
        "owner": "TaskA"
    },

    {

        "resource": "Mutex 2",
        "owner": "TaskB"
    }
]

# Metrics

metrics = {

    "cpu_utilization": "0%",

    "context_switches": 0,

    "completed_tasks": 0,

    "algorithm": current_algorithm
}


@app.route("/")
def index():

    return render_template(

        "index.html",

        tasks=tasks,

        resources=resources,

        metrics=metrics
    )


# Handle algorithm switching

@socketio.on("algorithm_change")
def algorithm_change(data):

    global current_algorithm

    current_algorithm = data["algorithm"]

    print(

        f"\nSwitched to: {current_algorithm}\n"
    )

    thread = Thread(

        target=run_simulation,

        args=(socketio, current_algorithm)
    )

    thread.start()


# Start initial simulation

def start_background_simulation():

    while True:

        thread = Thread(

            target=run_simulation,

            args=(socketio, current_algorithm)
        )

        thread.start()

        time.sleep(10)


if __name__ == "__main__":

    background_thread = Thread(

        target=start_background_simulation
    )

    background_thread.daemon = True

    background_thread.start()

    socketio.run(

        app,

        host="0.0.0.0",

        port=5000,

        debug=True
    )