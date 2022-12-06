import os
import socket
import time
import uuid
from base58 import b58encode
from multiprocessing import Queue
from threading import Thread, Semaphore
from flask import Flask, request, abort, send_file
from flask_socketio import SocketIO
from flask_cors import CORS

from utils import get_opts, get_image_path, load_image

# constants
FLICKR_ALPHABET = b"123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
BUFFER_SIZE = 1024
IMAGE_DIR = "temp"
N_IMAGES = 3
N_WORKERS = 3

# flask app for backend
app = Flask(__name__)
CORS(app)  # allow cross-origin for frontend
app.secret_key = os.urandom(16)  # random secret key

# socket server
socketio = SocketIO(app, cors_allowed_origins="*")


semaphore = Semaphore(N_WORKERS)
workers_limit = N_WORKERS + 1
conn_pool = []
images = Queue(maxsize=20)
idle_workers = Queue(maxsize=5)

last_img_id = {
    0: "",
    1: "",
    2: ""
}

img_num = 0
img_size = 0  # bit
start_time = 0.0
total_time = 0.0  # second


def print_metrics():
    throughput = img_size / total_time

    print("--------------------------------------")
    print("Message size: " + str(img_size) + " bits")
    print("Time: " + str(total_time) + " seconds")
    print("Throughput: " + str(throughput) + " bps")
    print("--------------------------------------")

def send_img_to_worker(img_id: str):
    global start_time, total_time, img_num, img_size, last_img_id, workers_limit, \
        images, conn_pool, idle_workers

    semaphore.acquire()
    id = idle_workers.get()
    worker = conn_pool[id]
    img_msg = load_image(img_id) + "\n"

    try:
        while True:
            worker.send(img_msg.encode("utf-8"))
            print("Sending the image to worker #" + str(id + 1) + "...")

            msg = ""
            while True:
                feedback = worker.recv(BUFFER_SIZE)
                msg += feedback.decode("utf-8")
                if msg[-1] == "\n":
                    break

            if msg == "404\n":
                print("Worker #" + str(id + 1) + " disconnected")
                images.put(img_id)
                raise Exception

            # receive recognition result
            msg = msg.split(" ", 1)
            this_img_id, this_result = msg[0], msg[1].split("\n")[0]

            if this_img_id != last_img_id[id]:
                socketio.emit("result", {
                    "task_id": this_img_id,
                    "result": this_result,
                })

                img_size += len(img_msg.encode("utf-8")) * 8
                img_num += 1

                if img_num == N_IMAGES:
                    total_time = time.time() - start_time
                    print_metrics()
                    img_num = 0

                last_img_id[id] = this_img_id

                break

        idle_workers.put(id)
        semaphore.release()

    except Exception as e:  # a worker failed
        conn_pool[id].close()

        if workers_limit < 4:  # set 5
            idle_workers.put(workers_limit - 1)
            print("Assigning to worker #" + str(workers_limit) + "...")
            workers_limit += 1
            semaphore.release()
        else:
            print("No more available workers")

        print(e)

@app.route("/api/task", methods=["POST", "OPTIONS"])
def receive_img():
    global start_time

    # generate a task id = saved temp image name
    task_id = b58encode(uuid.uuid4().bytes, FLICKR_ALPHABET).decode()

    # save temp image
    file = request.files["file"]
    file.save(get_image_path(task_id))

    # create new thread, send image to worker
    if img_num == 0:
        start_time = time.time()

    worker_thread = Thread(target=send_img_to_worker, args=(task_id,))
    worker_thread.setDaemon(True)
    worker_thread.start()

    return task_id

@app.route("/upload/<task_id>", methods=["GET"])
def send_img_to_frontend(task_id: str):
    img_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        get_image_path(task_id)
    )

    if os.path.exists(img_path) and os.path.isfile(img_path):
        return send_file(img_path, task_id)
    else:
        abort(404)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>", methods=["GET"])
def index(path: str):
    return app.send_static_file(path)

def connect_to_workers():
    global conn_pool, idle_workers, N_WORKERS, images, start_time, img_num

    # Build connection with workers
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket1.bind(("10.10.1.1", 1001))
    socket2.bind(("10.10.2.2", 1002))
    socket3.bind(("10.10.3.2", 1003))

    # socket1.bind(("localhost", 1001))
    # socket2.bind(("localhost", 1002))
    # socket3.bind(("localhost", 1003))

    socket1.listen(5)
    socket2.listen(5)
    socket3.listen(5)

    print("Connecting to worker #1...")
    i = 0
    worker, _ = socket1.accept()
    conn_pool.append(worker)
    if i < N_WORKERS:
        idle_workers.put(i)
    i += 1

    print("Connecting to worker #2...")
    worker2, _ = socket2.accept()
    conn_pool.append(worker2)
    if i < N_WORKERS:
        idle_workers.put(i)
    i += 1

    print("Connecting to worker #3...")
    worker3, _ = socket3.accept()
    conn_pool.append(worker3)
    if i < N_WORKERS:
        idle_workers.put(i)
    i += 1

    print("Successfully connected to all workers")

if __name__ == "__main__":
    hostname, port = get_opts()

    connect_to_workers()

    print(f"""Server is running on {hostname}:{port}...""")
    socketio.run(app, host=hostname, port=port)
