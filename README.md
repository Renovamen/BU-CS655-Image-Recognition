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

Then, log in to **web-interface** node and install dependencies:

```bash
cd backend

chmod +x ./install.sh
./install.sh
```

After that, log in to **node-1**, **node-2** and **node-3**, respectively:

```bash
cd worker

chmod +x ./install.sh
./install.sh
```


### Run Web Interface

```bash
chmod +x ./run.sh
./run.sh
```


### Run workers

**node-1** (10.10.1.1):

```bash
python3 main.py --hostname 0.0.0.0 --port 1001 --fail 0
```

**node-2** (10.10.2.2):

```bash
python3 main.py --hostname 0.0.0.0 --port 1002 --fail 0
```

**node-3** (10.10.3.2):

```bash
python3 main.py --hostname 0.0.0.0 --port 1003 --fail 0
```
