import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

def plot_vals(x, vals, filename, ylabel=None, title=None, yrange=None):

    #plt.figure()
    #plt.yscale('log')
    if yrange:
        plt.ylim(bottom=yrange[0], top=yrange[1])
    plt.xlabel('x (m)')
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.plot(x, vals)
    plt.savefig(filename)
    plt.clf()


if __name__ == "__main__":

    current_directory = Path.cwd()

    # Loop over all .dat files in the current directory
    for dat_file in current_directory.glob('*.dat'):
        # Process the .dat file (replace this with your actual processing logic)
        print(f"Processing file: {dat_file.name}")
        dat = np.genfromtxt(dat_file)
        fname=''.join([dat_file.stem, ".png"])
        step = dat_file.stem.split('_')[-1]
        # For E
        #yrng = [-15, 15]
        # For V
        yrng = [-0.25, 0.05]
        # For rho
        #yrng = [-0.25, 0.05]

        plot_vals(dat[:,0], dat[:,1], yrange=yrng, title=''.join(["step = ", step]), filename=fname)
        #plot_vals(dat[:,0], dat[:,1]-dat[:,1][0], yrange=yrng, title=''.join(["step = ", step]), filename=fname)
        #plot_vals(dat[:,0], dat[:,1], filename=fname)
        print("Finished ", fname)

