import numpy as np
import math as math

import cv2
def get_ideal_low_pass_filter( shape, cutoff):
    [h, w] = shape

    mask_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            distance = math.sqrt((i - (h / 2)) * (i - (h / 2)) + (j - (w / 2)) * (j - (w / 2)))
            if distance <= cutoff:
                mask_image[i][j] = 1
            else:
                mask_image[i][j] = 0

    return mask_image

def get_ideal_high_pass_filter( shape, cutoff):

    mask_image = 1 - get_ideal_low_pass_filter(shape, cutoff)
    return mask_image

def get_butterworth_low_pass_filter( shape, cutoff,order):

    [h, w] = shape
    mask_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            distance = math.sqrt((i - (h / 2)) ** 2 + ((j - (w / 2)) ** 2))
            mask_image[i][j] = 1 / (1 + ((distance / cutoff) ** (2 * order)))


    return mask_image

def get_butterworth_high_pass_filter( shape, cutoff,order):
    mask_image = 1 - get_butterworth_low_pass_filter(shape, cutoff,order)
    return mask_image

def get_gaussian_low_pass_filter(shape, cutoff):

    [h, w] = shape

    mask_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            distance = math.sqrt((i - (h/ 2)) ** 2 + ((j - (w / 2)) ** 2))
            mask_image[i][j] = 1 / math.exp((distance * distance) / (2 * cutoff * cutoff))


    return mask_image

def get_gaussian_high_pass_filter( shape, cutoff):

    mask_image = 1 - get_gaussian_low_pass_filter(shape, cutoff)
    return mask_image

def post_process_image( image):

    c_min = np.min(image)
    c_max = np.max(image)
    new_min = 0
    new_max = 255
    stretch_image = np.zeros((np.shape(image)), dtype=np.uint8)
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            stretch_image[i][j] = (image[i][j] - c_min) * ((new_max - new_min) / (c_max - c_min)) + new_min

    return stretch_image


def filtering(image,cutoff,filtertype):
    given_image = image
    s = given_image.shape

    fft_image = np.fft.fft2(image)
    shift_image = np.fft.fftshift(fft_image)
    #dft_image = np.uint8(np.log(np.absolute(shift_image)) * 10)

    if filtertype=='Ideal Low Pass' :
        mask = get_ideal_low_pass_filter(s, cutoff)
    elif filtertype=='Ideal High Pass' :
        mask=get_ideal_high_pass_filter(s, cutoff)
    elif filtertype=='Gaussain Low Pass':
        mask=get_gaussian_low_pass_filter(s,cutoff)
    elif filtertype=='Gaussian High Pass':
        mask=get_gaussian_high_pass_filter(s,cutoff)
    elif filtertype=='Butterworth Low Pass':
        mask=get_butterworth_low_pass_filter(s,cutoff,order=2)
    else:
        mask=0
    #cv2.imshow('image', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    filter_image = shift_image * mask
    filter_finalimg = np.uint8(np.log(np.absolute(filter_image)) * 10)

    ishift_image = np.fft.ifftshift(filter_image)
    ifft_image = np.fft.ifft2(ishift_image)
    mag_image = np.absolute(ifft_image)
    f = post_process_image(mag_image)
    #cv2.imshow('image',f)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return [f,filter_finalimg]
def filtering_order(image,cutoff,filtertype,order):
    given_image = image
    s = given_image.shape

    fft_image = np.fft.fft2(image)
    shift_image = np.fft.fftshift(fft_image)
    dft_image = np.uint8(np.log(np.absolute(shift_image)) * 10)


    if filtertype=='Butterworth Low Pass':
        mask=get_butterworth_low_pass_filter(s,cutoff,order)
    else:
        mask=get_butterworth_high_pass_filter(s,cutoff,order)
    #cv2.imshow('image', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    filter_image = shift_image * mask
    filter_finalimg = np.uint8(np.log(np.absolute(filter_image)) * 10)

    ishift_image = np.fft.ifftshift(filter_image)
    ifft_image = np.fft.ifft2(ishift_image)
    mag_image = np.absolute(ifft_image)
    f = post_process_image(mag_image)
    #cv2.imshow('image',f)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return [f,filter_finalimg]

