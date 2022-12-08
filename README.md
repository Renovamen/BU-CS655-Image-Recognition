# Image Recognition Application

GENI public routable IP: http://130.127.215.146:80


&nbsp;

## Team

- Hanlin Zou (U96634471)
- Xiaohan Zou (U18269004)


&nbsp;

## Tech Stack

- Frontend: [Vue 3](https://vuejs.org/) + [Vite 3](https://vitejs.dev/) + [Ant Design](https://antdv.com/)
- Backend: [Flask](https://flask.palletsprojects.com/)
- Image Recognition: [PyTorch](https://pytorch.org/)
- Socket


&nbsp;

## Demo Video

https://user-images.githubusercontent.com/29454156/206197721-3ddd04a1-50f2-4eca-9b85-26cddef595b3.mp4


&nbsp;

## Usage

### Prerequisites

Fisrt, use [`geni.xml`](geni.xml) to reserve resources on GENI.

Then, log in to **web-interface** node, clone Github repo and install dependencies:

```bash
git clone https://github.com/Renovamen/BU-CS655-Image-Recognition.git
cd BU-CS655-Image-Recognition/backend

chmod +x ./install.sh
./install.sh
```

After that, log in to **node-1**, **node-2** and **node-3**, respectively:

```bash
git clone https://github.com/Renovamen/BU-CS655-Image-Recognition.git
cd BU-CS655-Image-Recognition/worker

chmod +x ./install.sh
./install.sh
```


&nbsp;

### Run Web Interface

Log in to **web-interface** node and:

```bash
cd backend/src
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 3 --images 4 --delay 0 --loss 0
```

**Options**:

- `hostname`: web interface hostname
- `port`: web interface port number
- `workers`: number of avaliable workers, maximum is 3
- `images`: compute throughput after uploading how many number of images
- `delay`: worker delay (delay of all workers are the same)
- `loss`: worker loss rate (loss rate of all workers are the same)


&nbsp;

### Run workers

**node-1**:

```bash
cd worker
python3 main.py --hostname 10.10.1.2 --port 2001 --fail 0
```

**node-2**:

```bash
python3 main.py --hostname 10.10.2.1 --port 2002 --fail 0
```

**node-3**:

```bash
python3 main.py --hostname 10.10.3.1 --port 2003 --fail 0
```

**Options**:

- `hostname`: worker hostname
- `port`: worker port number
- `fail`: worker failure rate


&nbsp;

### Upload Images

Open the URL given by the **web-interface** node in your browser, then you can upload images.


&nbsp;

## Experiments

See [`experiments`](experiments) folder for raw experimental results and the images we used during our experiments.
