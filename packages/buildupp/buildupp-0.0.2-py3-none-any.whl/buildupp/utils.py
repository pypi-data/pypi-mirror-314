import matplotlib as mpl
import matplotlib.pyplot as plt

def set_plot_theme():
    """Set plot theme"""

    params = {
        "axes.labelsize": 7,
        "axes.titlesize": 6,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "axes.titlepad": 1,
        "axes.labelpad": 1,
        "lines.linewidth": 0.8,
        "lines.markersize": 2.5,
        "legend.fontsize": 5,
        "legend.title_fontsize": 6,
    }
    mpl.rcParams.update(params)


def myplot(
    ax=None,
    x=[0, 1],
    y=[0, 1],
    xlbl="xlbl",
    ylbl="ylbl",
    type="lin",
    s=0,
    e=-1,
    normx=1,
    normy=1,
    lbl=True,
    **kwargs,
):
    if ax is None:
        fig, ax = plt.subplots()

    if type == "lin":
        (line,) = ax.plot(x[s:e] * normx, y[s:e] * normy, **kwargs)
    elif type == "semilogy":
        (line,) = ax.semilogy(x[s:e] * normx, y[s:e] * normy, **kwargs)
    elif type == "semilogx":
        (line,) = ax.semilogx(x[s:e] * normx, y[s:e] * normy, **kwargs)
    elif type == "loglog":
        (line,) = ax.loglog(x[s:e] * normx, y[s:e] * normy, **kwargs)

    if lbl:
        ax.set_xlabel(xlbl)
        ax.set_ylabel(ylbl)

    return line

