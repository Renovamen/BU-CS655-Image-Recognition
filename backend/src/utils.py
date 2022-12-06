import os
import argparse
import torchvision.transforms as transforms
from PIL import Image

IMAGE_DIR = "temp"


def get_opts():
    parser = argparse.ArgumentParser(description="Image Recognition")
    parser.add_argument("--hostname", type=str, default="0.0.0.0", help="Web interface's hostname")
    parser.add_argument("--port", type=int, default=80, help="Web interface's port")

    opts = parser.parse_args()
    return opts.hostname, opts.port

def get_image_path(filename: str):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    return os.path.join(IMAGE_DIR, filename)

def load_image(image_id: str):
    """Load an image and convert it to string."""
    img = Image.open(os.path.join(IMAGE_DIR, image_id)).convert('RGB')
    img = transforms.ToTensor()(img).numpy()

    n, m = img.shape[1], img.shape[2]

    img = img.flatten()
    img_s = " ".join([str(i) for i in img])
    img_s = image_id + " " + str(n) + " " + str(m) + " " + img_s

    return img_s
