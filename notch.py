import cv2
import numpy as np

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
       if drawing == True:
            if mode == True:
                cv2.rectangle(notch_filter.dft_image,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(notch_filter.dft_image,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(notch_filter.dft_image,(ix,iy),(x,y),(0,255,0),-1)
        else:
           cv2.circle(notch_filter.dft_image,(x,y),5,(0,0,255),-1)
def notch_filter(img):

    fft_image = np.fft.fft2(img)
    shift_image = np.fft.fftshift(fft_image)
    notch_filter.dft_image = np.uint8(np.log(np.absolute(shift_image)) * 10)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)

    while(1):
        cv2.imshow('image',notch_filter.dft_image)
        cv2.imwrite('noisereducedimage.png',notch_filter.dft_image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('x'):
            cv2.destroyAllWindows()
            break

    mask=cv2.imread('noisereducedimage.png',0)

    shift_image=(mask*100)*shift_image
    ishift_image = np.fft.ifftshift(shift_image)
    ifft_image = np.fft.ifft2(ishift_image)
    mag_image = np.absolute(ifft_image)
    def post_process_image(image):

        c_min = np.min(image)
        c_max = np.max(image)
        new_min = 0
        new_max = 255
        stretch_image = np.zeros((np.shape(image)), dtype=np.uint8)
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                stretch_image[i][j] = (image[i][j] - c_min) * ((new_max - new_min) / (c_max - c_min)) + new_min

        return stretch_image

    f = post_process_image(mag_image)
    return f,mask