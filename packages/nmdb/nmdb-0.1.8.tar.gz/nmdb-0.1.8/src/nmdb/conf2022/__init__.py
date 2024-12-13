import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

def main():
    """
    plot GLE70 percentage increase to use as coverpage for proceedings
    """

    sns.set_context("paper")
    sns.color_palette("vlag", as_cmap=True)
    download = os.path.join(_ROOT, 'gle70.dat')
    #download = "gle70.dat"
    # data as downloaded from NEST by selecting:
    # - all stations, GLE70, ASCII data
    # manually edited:
    # - STATION NAMES replaced by 'date' plus station names , separated by ";"
    df = pd.read_table(download, sep=";", comment="#")
    df.index = pd.to_datetime(df['date'])
    # drop unused columns
    df.drop(["date"], axis=1, inplace=True)

    # replace '   null' string for missing data with None
    df = df.replace(to_replace=r'null', value=None, regex=True)
    # values in columns that had 'null's need to be converted to float
    df = df.astype(float)

    # average over 5 minutes
    data = df.rolling(5).mean()

    # station names
    stations = data.columns.values.tolist()

    # make baseline
    sbas = data.head(60) # take the first 60 minutes

    # create percentage with offset
    off = 0
    for s in stations:
        data[s] = ((data[s] - sbas[s].mean())/sbas[s].mean())*100 + off
        off += 10

    lw=5
    ls="solid"
    for s in stations:
        ax = sns.lineplot(data=data[s], linestyle=ls, linewidth=lw, legend=False)

    # hide axis labels and numbers
    ax.set(xlabel=None)
    ax.set(xticklabels=[])
    ax.set(ylabel=None)
    ax.set(yticklabels=[])

    # save images in current directory without overwriting existing files:
    i = 0
    filename = "conf2022_coverpage"
    while os.path.exists('{}{:d}.eps'.format(filename, i)):
        i += 1
    plt.savefig('{}{:d}.eps'.format(filename, i))

    i = 0
    filename = "conf2022_coverpage"
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    plt.savefig('{}{:d}.png'.format(filename, i), dpi=300)

    i = 0
    filename = "conf2022_coverpage_transparent"
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    plt.savefig('{}{:d}.png'.format(filename, i), transparent=True, dpi=300)

    return(df)


# --------------------------------------------------------------------------
if __name__ == '__main__':
    df = main()
