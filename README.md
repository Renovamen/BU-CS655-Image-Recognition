# Image Recognition Application

## Team & Division of Labor

- Hanlin Zou (U96634471)
- Xiaohan Zou (U18269004)


&nbsp;

## Tech Stack

- Frontend: [Vue 3](https://vuejs.org/) + [Vite 3](https://vitejs.dev/) + [Ant Design](https://antdv.com/)
- Backend: [Flask](https://flask.palletsprojects.com/)
- Image Recognition: [PyTorch](https://pytorch.org/)
- Socket programming


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
cd backend

chmod +x ./run.sh
sudo ./run.sh
```


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
