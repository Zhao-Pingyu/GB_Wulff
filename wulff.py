import glob
import os
import numpy as np
import re
from natsort import natsorted
import matplotlib.pyplot as plt

def get_energy(angle,files):
    # Initialize lists for storing N and ecoh
    N = []
    ecoh = []

    # Open a file for writing the output
    filename = f'{angle}-inc.txt'
    with open(filename, 'w') as output_file:
        for f in files:
            # Split the filename into parts
            nms = f[:-7].split("-")

            try:
                # Open the file and read its lines
                with open(f, 'r') as infile:
                    data = infile.readlines()

                    # Extract the desired values using regular expressions
                    n = re.findall(r"[-+]?(?:\d*\.*\d+)", data[-4])[0] 
                    e = re.findall(r"[-+]?(?:\d*\.*\d+)", data[-6])[0] 

                    # Write the extracted data to the output file
                    output_file.write(f"{nms[2]} {e} {n}\n")

                    # Append the values to the lists
                    N.append(n)
                    ecoh.append(e)
            except Exception as ex:
                output_file.write(f"Error processing file {f}: {ex}\n")
                print(f"Error processing file {f}: {ex}")

def get_full_range(En):
    theta = np.arange(0,361)
    # Load the energy data from the specified file
    try:
        E = np.loadtxt(f'{angle}-inc.txt')[:, 1]  # Assuming the second column contains energy values
    except Exception as e:
        print(f"Error loading file {angle}-inc.txt: {e}")
        return None
    En = np.zeros(361)
    for i in range(0,361):
        if i<=45:
            En[i] = E[i]
        elif i>45 and i<=90:
            En[i] = En[90-i]
        elif i>90 and i <=180:
            En[i] = En[180-i]
        elif i>180 and i<=270:
            En[i] = En[360-i]
        else:
            En[i] = En[540-i]
    return En
        
def plot_wulff(En):
    fi = np.arange(0,361)
    r = En*20
    x = r*np.cos(fi*np.pi/180)
    y = r*np.sin(fi*np.pi/180)
    incs = np.arange(0,361)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # Wulff construction
    for i, p in zip(fi, fi*np.pi/180):
        t = np.linspace(-1, 1, 100)
        x1 = -1.5*np.sin(p)*t + x[i]
        y1 = 1.5*np.cos(p)*t + y[i]
        ax.plot(x1, y1, "r--", linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')

    ax.plot(x,y)
    plt.tick_params(left = False, right = False , labelleft = False,labelbottom = False, bottom = False)
    #plt.savefig(f'{angle}.png',bbox_inches="tight",dpi=300)
    plt.show()

    # Generate mask
    incs = np.append(incs, np.argsort(r))
    mask = np.zeros(shape=(1000, 1000))
    xx, yy = np.meshgrid(np.arange(-500, 500), np.arange(-500, 500))
    r0 = 250
    ratio = 1.2
    for i, p in zip(chosen, fi*np.pi/180):
        xx1 = (xx*np.cos(p) - yy*np.sin(p))
        mask[xx1 >= (r[i]*r0/np.min(r)/ratio)] = 1

    plt.axis('off')
    plt.imshow(mask, cmap='gray')
    #plt.savefig(f'{angle}.png',bbox_inches="tight",dpi=300)
    plt.show()
   
if __name__ == "__main__":
    angle = 20
    os.chdir(f'{angle}')
    files = natsorted(glob.glob(f'log-{angle}-*.lammps'))
    En = get_energy(angle,files)
    get_full_range(En)
    plot_wulff(En)
    os.chdir('..')