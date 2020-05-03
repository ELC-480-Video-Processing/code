"""
Phase correlation implementation in Python using cv2 and numpy
"""

import cv2
from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import numpy as np


def phase_correlation(a, b):

    delta = 0.1

    G_a = np.fft.fft2(a,s=b.shape)
    G_b = np.fft.fft2(b)

    conj_b = np.ma.conjugate(G_b)
    r = np.multiply(G_a,conj_b)

    r = np.divide(r,np.absolute(r+delta))
    r = np.fft.ifft2(r).real
    return r


def plot_results(map):

    """
        Plots the output of phase correlation in a 3D Meshgrid 
        @param map: a 2D np array consisting of real phase correlation data 

    """

    # Create axis vectors for matplotlib
    X = np.arange(0, 360, step=1)
    Y = np.arange(0, 360, step=1)
    X, Y = np.meshgrid(X, Y)

    # Plot 3D Meshplot of Phase corrleation data
    fig = plt.figure()
    ax  = fig.gca(projection = '3d')
    surf = ax.plot_surface(X,Y, map, cmap = cm.coolwarm, linewidth=0, antialiased=False)

    plt.show()

def pad_image (obj_frame, master_vid_shape):

    """
    - Zero pads the object frame to match the dimensions of the video frame

    @param obj_frame: an ndarray of pixel values corresponding to the object to be tracked
    @param master_vid_shape : a tuple containing the dimensions of the video-frame to be analyzed 

    """
    
    diff_x, diff_y = tuple(map(lambda i,j: i - j, master_vid_shape, obj_frame.shape)) 

    if ( int(diff_x/2) * 2 != diff_x):
        pad_ax_0_left  = int(diff_x/2)
        pad_ax_0_right = int(diff_x/2) + 1

    else: 
        pad_ax_0_left, pad_ax_1_right = (int(diff_x/2),)*2


    if ( int(diff_y/2)*2 != diff_y):
        pad_ax_1_left  = int(diff_y/2)
        pad_ax_1_right = int(diff_y/2) + 1
    else: 
        pad_ax_1_left,pad_ax_1_right = (int(diff_y/2),)*2

    pad_args = ((pad_ax_0_left,pad_ax_0_right),(pad_ax_1_left,pad_ax_1_right))
    return np.pad(obj_frame,pad_args,'constant',constant_values = (0,))



def main():
    
    """
    Tracking flow: 
    - load video 
    - specify ROI/bounding box through user input
    - for each frame:
        - take previous bounding box coordinates and create 4 candidate blocks
        - do phase correlation for each of them 
        - whichever one has the highest peak probably corresponds to the new object
        - redraw the bounding box
    

    """
    

    road1 = cv2.imread('test_frame.PNG')
    road2 = cv2.imread('test_img_full.png')

    road1 = cv2.cvtColor(road1,cv2.COLOR_BGR2GRAY)
    road2 = cv2.cvtColor(road2,cv2.COLOR_BGR2GRAY)

    padded_frame = pad_image(road1,road2.shape)
  
    result = phase_correlation(road1, road2)
    plot_results(result)

    peak = np.amax(result)
    idx = np.where(result == peak)
    print(idx)
    print(result[227,236])
    print(peak)

if __name__=="__main__":
    main()
