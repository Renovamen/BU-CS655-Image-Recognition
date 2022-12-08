import matplotlib.pyplot as plt

x_n_workers = [1, 2, 3]
x_loss = [0, 0.4, 0.8]
x_delay = [0, 5, 10]
x_fail = [0, 0.4, 0.8]

y_n_workers = [6167982.6327, 8222225.6971, 14193197.1429]
y_loss = [14193197.1429, 9221141.8049, 2943601.3002]
y_delay = [14193197.1429, 9594891.2064, 7953135.7798]
y_fail = [14193197.1429, 15040344.8562, 15177870.0491]

figure, ax = plt.subplots()

# ax.plot(x_n_workers, y_n_workers)
# ax.set_xlabel("Number of workers")
# ax.set_xticks(x_n_workers)

# ax.plot(x_loss, y_loss)
# ax.set_xlabel("Loss rate")
# ax.set_xticks(x_loss)

# ax.plot(x_delay, y_delay)
# ax.set_xlabel("Delay time (s)")
# ax.set_xticks(x_delay)

ax.plot(x_fail, y_fail)
ax.set_xlabel("Failure rate")
ax.set_xticks(x_fail)
ax.set_ylim(bottom=10000000, top=20000000)

ax.set_ylabel("Average Throughput (bps)")

plt.show()
