# Experimental results

We compute throughput (bps) using different parameters. For each group of parameters, we upload 4 [images](images) and run 5 experiments.

GENI site: Clemson InstaGENI


&nbsp;

## Different number of workers

Other parameters: 

- Worker delay: 0
- Worker loss rate: 0
- Worker failure rate: 0

### Number of workers: 3

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 3 --images 4 --delay 0 --loss 0  # web-interface
```

- 14236062.151323903
- 18069646.38210088
- 14528836.943093367
- 12018148.687296676
- 12113291.550477952

### Number of workers: 2

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 2 --images 4 --delay 0 --loss 0  # web-interface
```

- 12215982.4621256
- 8385454.489114087
- 7260621.367790201
- 6319580.413989907
- 6929489.752331601

### Number of workers: 1

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 1 --images 4 --delay 0 --loss 0  # web-interface
```

- 9143509.689882671
- 5061233.049537599
- 5285867.426616494
- 5445877.599173843
- 5903425.398450934


&nbsp;

## Different loss rate

Other parameters: 

- Worker number: 3
- Worker delay: 0
- Worker failure rate: 0

### Loss rate: 0

See [here](#number-of-workers-3)

### Loss rate: 0.4

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 3 --images 4 --delay 0 --loss 0.4  # web-interface
```

- 12300186.26539436
- 10042948.646788275
- 8086145.111512533
- 9724041.990045251
- 5952387.010746283

### Loss rate: 0.8

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 3 --images 4 --delay 0 --loss 0.8  # web-interface
```

- 2810680.698453671
- 3853498.092480232
- 2903485.302942034
- 2029402.203940243
- 3120940.203409234


&nbsp;

## Different delay

Other parameters: 

- Worker number: 3
- Worker loss rate: 0
- Worker failure rate: 0

### Delay: 0

See [here](#number-of-workers-3)

### Delay: 5s

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 3 --images 4 --delay 5 --loss 0  # web-interface
```

- 12287385.697190542
- 13467951.823733756
- 11701883.184375245
- 5383709.236574674
- 5133526.090101776


### Delay: 10s

```bash
sudo python3 main.py --hostname 0.0.0.0 --port 80 --workers 3 --images 4 --delay 10 --loss 0  # web-interface
```

- 10649404.31942207
- 8214020.424246823
- 10938081.361847911
- 5449601.585039886
- 4514571.208375813


&nbsp;

## Different failure rate

Other parameters: 

- Worker number: 3
- Worker delay: 0
- Worker loss rate: 0

### Failure rate: 0

See [here](#number-of-workers-3)

### Failure rate: 0.4

```bash
python3 main.py --hostname 10.10.1.2 --port 2001 --fail 0.4  # node-1
```

- 15235830.658754025
- 18420662.713371494 
- 11993646.426910425
- 14013012.021931202
- 15538572.460225407


### Failure rate: 0.8

```bash
python3 main.py --hostname 10.10.1.2 --port 2001 --fail 0.8  # node-1
```

- 17230423.210394820
- 15021948.102934023
- 10934902.123904102
- 14023404.130912302
- 18678672.677461978
