import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import os

from web.socket_handler import run_simulation

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

socketio = SocketIO(
    app,
    async_mode="eventlet",
    cors_allowed_origins="*"
)

current_algorithm = "Round Robin"

tasks = [
    {"name": "TaskA", "state": "READY"},
    {"name": "TaskB", "state": "READY"},
    {"name": "TaskC", "state": "READY"},
]

resources = [
    {"resource": "Mutex 1", "owner": "TaskA"},
    {"resource": "Mutex 2", "owner": "TaskB"},
]

metrics = {
    "cpu_utilization": "0%",
    "context_switches": 0,
    "completed_tasks": 0,
    "algorithm": current_algorithm,
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        tasks=tasks,
        resources=resources,
        metrics=metrics,
    )


@socketio.on("algorithm_change")
def algorithm_change(data):
    global current_algorithm
    current_algorithm = data["algorithm"]
    print(f"\nSwitched to: {current_algorithm}\n")
    socketio.start_background_task(run_simulation, socketio, current_algorithm)


def background_simulation_loop():
    while True:
        socketio.start_background_task(run_simulation, socketio, current_algorithm)
        eventlet.sleep(10)


socketio.start_background_task(background_simulation_loop)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False,
    )