import json
import random
import socket
import argparse
import numpy as np
import torch
from torchvision import models, transforms
from PIL import Image

BUFFER_SIZE = 1024

# load model
model = models.googlenet(pretrained=True)
model.eval()

# load class names (labels)
with open("./labels.json", "r", encoding="utf8") as f:
    labels = json.load(f)


def rcv_message(skt: socket) -> str:
    """Receive a meesage via a given socket"""
    msg = ""

    while True:
        feedback = skt.recv(BUFFER_SIZE)
        msg += feedback.decode("utf-8")
        if msg[-1] == '\n':  # end of the message
            break

    return msg

def inference(h: int, w: int, c: int, image: str) -> str:
    """Forward the image to model for prediction"""
    image = np.array(image.split()).astype(np.uint8)
    image = image.reshape(h, w, c)
    image = Image.fromarray(image)
    image = transforms.ToTensor()(image).unsqueeze(0)

    scores = model(image)[0]
    pred = labels[str(torch.argmax(scores).item())]

    return pred

def run_worker(hostname: str, port: int, fail: float = 0.0):
    last_seqnum, last_result = "", ""

    skt = socket.create_connection((hostname, port))
    print(f"""Worker is running on {hostname}:{port}""")

    while True:
        print("Waiting for message...")
        image_msg = rcv_message(skt)

        if random.uniform(0, 1) < fail:  # node fails
            print("Worker failed, disconnecting from web interface node...")
            skt.send("404\n".encode("utf-8"))
            skt.close()
            break

        seqnum, h, w, c, image = tuple(image_msg.split(" ", 4))

        if seqnum != last_seqnum:  # not duplicate, use model to predict
            print("Recognizing image...")
            last_result = inference(int(h), int(w), int(c), image)
            last_seqnum = seqnum

        print("Sending recognition result to web interface node...")
        result_msg = str(last_seqnum) + " " + last_result + "\n"
        skt.send(result_msg.encode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image recognition worker")
    parser.add_argument("--hostname", type=str, help="Worker's hostname")
    parser.add_argument("--port", type=int, help="Worker's port")
    parser.add_argument("--fail", type=float, default=0, help="Worker's probability to fail (0-1)")

    opts = parser.parse_args()

    run_worker(opts.hostname, opts.port, fail=opts.fail)
