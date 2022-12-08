import os
import time
import random
import argparse
import socket
import numpy as np
from PIL import Image

IMAGE_DIR = "temp"
BUFFER_SIZE = 1024

def get_opts():
    parser = argparse.ArgumentParser(description="Image Recognition Web Interface")
    parser.add_argument("--hostname", type=str, default="0.0.0.0", help="Web interface's hostname")
    parser.add_argument("--port", type=int, default=80, help="Web interface's port")
    parser.add_argument("--workers", type=int, default=3, help="Number of avaliable workers, maximum is 3")
    parser.add_argument("--images", type=int, default=4, help="Compute throughput after uploading ? images")
    parser.add_argument("--delay", type=float, default=0, help="Delay (seconds)")
    parser.add_argument("--loss", type=float, default=0, help="Loss rate (0-1)")

    opts = parser.parse_args()
    return opts.hostname, opts.port, opts.workers, opts.images, opts.delay, opts.loss

def get_image_path(filename: str):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    return os.path.join(IMAGE_DIR, filename)

def load_image(image_id: str):
    """Load an image and convert it to string"""
    img = Image.open(os.path.join(IMAGE_DIR, image_id)).convert('RGB')
    img = np.asarray(img)  # (h, w, c)

    h, w, c = img.shape[0], img.shape[1], img.shape[2]
    img = img.flatten()

    img_s = " ".join([str(i) for i in img])
    img_s = image_id + " " + str(h) + " " + str(w) + " " + str(c) + " " + img_s

    return img_s

def rcv_message(skt: socket, delay: float = 0.) -> str:
    """Receive a message via a given socket"""
    msg = ""

    while True:
        feedback = skt.recv(BUFFER_SIZE)
        msg += feedback.decode("utf-8")
        if msg[-1] == "\n":
            break

    time.sleep(delay)  # delay simulation
    return msg

def send_message(
    skt: socket, msg: str, loss: float = 0., timeout: int = 5
):
    """Send a message via a given socket"""
    skt.send(msg.encode("utf-8"))

    # loss simulation
    if random.uniform(0, 1) < loss:
        # wait for timeout
        time.sleep(timeout)

        # re-send the image
        print("Timeout, response lost, re-sending message...")
        send_message(skt, msg, loss, timeout)


class Throughput:
    """A class for computing throughput."""
    def __init__(self, max_n_msg: int) -> None:
        self.max_n_msg = max_n_msg
        self.reset()

    def reset(self) -> None:
        self.msg_num = 0
        self.msg_size = 0  # bits
        self.start_time = 0.0  # seconds
        self.total_time = 0.0

    def send(self) -> None:
        if self.msg_num == 0:
            self.start_time = time.time()

    def rcv(self, msg: str) -> None:
        self.msg_size += len(msg.encode("utf-8")) * 8
        self.msg_num += 1

        if self.msg_num == self.max_n_msg:
            self.total_time = time.time() - self.start_time
            self.compute()
            self.reset()

    def compute(self) -> None:
        """Compute throughput and print it"""
        tput = self.msg_size / self.total_time

        print("--------------------------------------")
        print("Message size: " + str(self.msg_size) + " bits")
        print("Time: " + str(self.total_time) + " seconds")
        print("Throughput: " + str(tput) + " bps")
        print("--------------------------------------")
