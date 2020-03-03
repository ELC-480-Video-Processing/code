"""
Phase Correlation implementation in Python
Michael Ting
Created 25 June 2013
Updated 8 July 2013

Algorithm:
    Given two input images A and B:
    Apply window function on both A and B to reduce edge effects
    Calculate the discrete 2D Fourier transform of both A and B
        G_a = F{A}
        G_b = F{B}
    Calculate the cross-power spectrum by taking the complex conjugate of G_b,
        multiplying the Fourier transforms together elementwise, and normalizing
        the product elementwise
        R = (G_a %*% G_B*) / (|G_a G_b*|)
            %*% is the Hadamard (entry-wise) product
    Obtain normalized cross-correlation by applying the inverse Fourier transform
        r = F^-1{R}
    Determine the location of the peak in r:
        (del_x, del_y) = argmax over (x,y) of {r}
"""


import numpy as np
from scipy import misc

import cv2

from argparse import ArgumentParser

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt 


# a and b are numpy arrays
def phase_correlation(a, b):

    G_a = np.fft.fft2(a)
    G_b = np.fft.fft2(b)

    conj_b = np.ma.conjugate(G_b)
    
    R = G_a*conj_b

    R /= np.absolute(R)
    r = np.fft.ifft2(R).real
    return r

def main():
    
    parser = ArgumentParser(description="Set parameters phase correlation calculation")
    
    parser.add_argument("infile1", metavar="in1", help="input image 1")    
    parser.add_argument("infile2", metavar="in2", help="input image 2")
    parser.add_argument("outfile", metavar="out", help="output image file name")
    
    args = parser.parse_args()
    
    # infile1 = open(args.infile1)
    # infile2 = open(args.infile2)
    # outfile = args.outfile
    # newfile = open(outfile, 'w')
    
    # road1 = misc.imread(infile1)
    # road2 = misc.imread(infile2)

    road1 = cv2.imread(args.infile1, 0)
    road2 = cv2.imread(args.infile2, 0)

    print (road1.shape)
    print (road2.shape)

    result = phase_correlation(road1, road2)

    fig = plt.figure()
    ax  = fig.add_subplot(111, projection = '3d')
    ax.plot(result[:,0], result[:,1],result[:,3])
    plt.show()

    result = np.multiply(result, 10^3)

    # cv2.imshow('result',result)
    # cv2.imwrite(args.outfile,result)


if __name__=="__main__":
    main()
