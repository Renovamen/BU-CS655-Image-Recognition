import os
import uuid
import socket
from multiprocessing import Queue
from threading import Thread, Semaphore
from flask import Flask, request, send_file
from flask_socketio import SocketIO
from flask_cors import CORS

from utils import Throughput, get_opts, get_image_path, load_image, rcv_message, send_message

# arguments
HOSTNAME, PORT, N_WORKERS, N_IMAGES, DELAY, LOSS = get_opts()

# throughput computer
throughput = Throughput(N_IMAGES)


def create_app():
    """Create Flask app and socket server"""
    app = Flask(__name__)  # flask app for backend
    CORS(app)  # allow cross-origin for frontend (only for development)
    app.secret_key = os.urandom(16)  # random secret key

    socketio = SocketIO(app, cors_allowed_origins="*")  # socket server

    return app, socketio

app, socketio = create_app()


class WorkerPool:
    """A class for maintaining worker sockets."""
    def __init__(self, n_workers: int) -> None:
        self.n_workers = n_workers
        self.semaphore = Semaphore(n_workers)
        self.worker_list = []
        self.idle_worker_id_list = Queue(maxsize=5)

    def add(self, worker: socket):
        """Add a worker to pool"""
        self.worker_list.append(worker)

        id = len(self.worker_list) - 1
        if id < self.n_workers:
            self.idle_worker_id_list.put(id)

    def reassign(self, id: int):
        """Worker #id failed, re-assign the task to another worker"""
        self.worker_list[id].close()

        id2, worker2 = self.busy()
        print("Assigning to worker #" + str(id2) + "...")

        return id2, worker2

    def busy(self) -> socket:
        """Assign a task to a worker"""
        self.semaphore.acquire()
        id = self.idle_worker_id_list.get()  # the worker is busy now, remove from idle work list
        worker = self.worker_list[id]
        return id, worker

    def idle(self, id: int):
        """Make the given worker idle"""
        self.idle_worker_id_list.put(id)
        self.semaphore.release()

worker_pool = WorkerPool(N_WORKERS)


def send_img_to_worker(img_id: str):
    """Assign and send the current image to a worker"""

    # load image from temp dir
    img_msg = load_image(img_id) + "\n"

    def to_worker(id: int, worker: socket):
        print("Sending the image to worker #" + str(id + 1) + "...")
        send_message(worker, img_msg, loss=LOSS)

        print("Receiving result from worker #" + str(id + 1) + "...")
        msg = rcv_message(worker, delay=DELAY)

        # node fail simulation
        if msg == "404\n":
            print("Worker #" + str(id + 1) + " disconnected")
            raise Exception

        msg = msg.split(" ", 1)
        cur_img_id, result = msg[0], msg[1].split("\n")[0]

        print("Sending the result to frontend...")
        socketio.emit("result", {
            "task_id": cur_img_id,
            "result": result,
        })

        # maybe compute throughput
        throughput.rcv(img_msg)

        # task finished, make this worker idle
        worker_pool.idle(id)

    # assign this task to a worker
    id1, worker1 = worker_pool.busy()

    try:
        to_worker(id1, worker1)
    except Exception as e:
        # worker #id1 failed, re-assign this task to another worker
        id2, worker2 = worker_pool.reassign(id1)
        to_worker(id2, worker2)
        print(e)

@app.route("/api/task", methods=["POST", "OPTIONS"])
def rcv_img_from_frontend():
    # generate a task id = saved temp image name
    task_id = str(uuid.uuid1())

    # save temp image
    file = request.files["file"]
    file.save(get_image_path(task_id))

    # maybe record send time for computing throughput
    throughput.send()

    # create new thread, send image to worker
    worker_thread = Thread(target=send_img_to_worker, args=(task_id,))
    worker_thread.daemon = True
    worker_thread.start()

    return task_id

@app.route("/upload/<task_id>", methods=["GET"])
def send_img_to_frontend(task_id: str):
    img_path = get_image_path(task_id)
    return send_file(img_path, task_id)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>", methods=["GET"])
def index(path: str):
    return app.send_static_file(path)

def connect_to_worker(h: str, p: int):
    """Given the hostname and port, build connection with the worker"""
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    skt.bind((h, p))
    skt.listen(5)

    worker, _ = skt.accept()
    worker_pool.add(worker)  # add to worker pool

def connect_to_workers():
    print("Connecting to worker #1...")
    connect_to_worker("10.10.1.2", 2001)
    # connect_to_worker("localhost", 2001)

    print("Connecting to worker #2...")
    connect_to_worker("10.10.2.1", 2002)
    # connect_to_worker("localhost", 2002)

    print("Connecting to worker #3...")
    connect_to_worker("10.10.3.1", 2003)
    # connect_to_worker("localhost", 2003)

    print("Successfully connected to all workers")

if __name__ == "__main__":
    connect_to_workers()

    print(f"""Server is running on {HOSTNAME}:{PORT}""")
    socketio.run(app, host=HOSTNAME, port=PORT)
