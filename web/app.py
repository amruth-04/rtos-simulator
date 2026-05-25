from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time
import os

from web.socket_handler import run_simulation

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret!"

socketio = SocketIO(

    app,

    cors_allowed_origins="*"
)

# Current algorithm

current_algorithm = "Round Robin"

# Tasks

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

# Resources

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


# Handle algorithm changes

@socketio.on("algorithm_change")
def algorithm_change(data):

    global current_algorithm

    current_algorithm = data["algorithm"]

    print(

        f"\nSwitched to: {current_algorithm}\n"
    )

    simulation_thread = Thread(

        target=run_simulation,

        args=(socketio, current_algorithm)
    )

    simulation_thread.start()


# Background simulation loop

def start_background_simulation():

    while True:

        simulation_thread = Thread(

            target=run_simulation,

            args=(socketio, current_algorithm)
        )

        simulation_thread.start()

        time.sleep(10)


if __name__ == "__main__":

    background_thread = Thread(

        target=start_background_simulation
    )

    background_thread.daemon = True

    background_thread.start()

    # IMPORTANT:
    # Use Render dynamic port

    port = int(

        os.environ.get("PORT", 5000)
    )

    socketio.run(

        app,

        host="0.0.0.0",

        port=port,

        debug=False
    )