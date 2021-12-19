from matplotlib import pyplot as plt


def plot_memberships(variables):
    total = len(variables)
    plt.figure(figsize=(6.4, 4.8 * (total - 1)))
    for idx, variable in enumerate(variables):
        ax = plt.subplot(total, 1, idx + 1)
        ax.set_title(variable.name)
        for k, v in variable.mfs.items():
            plt.plot(variable.range, v, label=k, marker="")
            if k in variable.fuzzified_variable:
                plt.plot(variable.crisp_value, variable.fuzzified_variable[k],
                         label=f"_nolegend_", marker="o")
            plt.legend(loc="upper left")


def plot_aggregations(aggregations, ranges):
    total = len(aggregations)
    plt.figure(figsize=(6.4, 4.8 * (total - 1)))
    for idx, (k, v) in enumerate(aggregations.items()):
        ax = plt.subplot(total, 1, idx + 1)
        ax.set_title(k)
        plot_aggregation(v, ranges[k])


def plot_aggregation(aggr, range, name=""):
    plt.plot(range, aggr, label=name, marker="")
