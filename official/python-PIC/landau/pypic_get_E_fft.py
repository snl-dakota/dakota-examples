import matplotlib.pyplot as plt
import numpy as np
import subprocess

from pathlib import Path

def plot_fft(times, E, km, w_pi, axis, filename, title=None):

    n_avg = 20

    field_kt = np.fft.fft(E[:, :], axis=axis)

    fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))
    x = times[0:-1-1]*w_pi
    y = np.abs(field_kt[1:-1,km]/np.max(field_kt[1:-1,km]))
    ax1.plot(x, y)
    if n_avg > 1:
        ax1.plot(x, np.convolve(y,np.ones(int(n_avg),dtype=float),mode='same')/int(n_avg), color="black")
    gamma=np.exp(-0.0043*times*w_pi)
    ax1.plot(times[1:-1]*w_pi,1.1*gamma[1:-1])

    if title:
        plt.title(title)
    ax1.set_yscale('log')
    ax1.set_xlabel("$t*\omega_{pi}$");
    ax1.set_ylabel("$E_k$");



    plt.savefig(filename)
    plt.show()


if __name__ == "__main__":

    current_directory = Path.cwd()

    N = 0
    E_vals = {}
    times = {}
    count = 0
    # Populate E (T x X)
    for dat_file in current_directory.glob('E*????[0-9].dat'):
        step = dat_file.stem.split('_')[-1]
        dat = np.genfromtxt(dat_file)
        if N == 0:
            N = dat.shape[0]
            print("Found",N,"nodes.")
        E_vals[step] = dat[:,1]
        if count % 100 == 0:
            print("Finished",count,"steps.")
        count += 1
    print("Found",len(E_vals),"time steps.")

    dt = 7.043835078e-06
    E = np.zeros(shape=(len(E_vals), N))
    times = np.zeros(len(E_vals))
    for step, Ex_dat in enumerate(E_vals):
        E[step] = E_vals[Ex_dat]
        times[step] = step*dt

    km = 16
    axis = 0
    plot_fft(times, E, km=km, w_pi=416.329453, axis=axis, \
             filename=''.join(['E_fft_axis_', str(axis), '.png']), \
             title=''.join(['km=', str(km), ' axis ', str(axis)]))
    axis = 1
    plot_fft(times, E, km=km, w_pi=416.329453, axis=axis, \
             filename=''.join(['E_fft_axis_', str(axis), '.png']), \
             title=''.join(['km=', str(km), ' axis ', str(axis)]))
