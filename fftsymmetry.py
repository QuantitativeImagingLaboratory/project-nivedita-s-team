import numpy as np
import time
def DFT_slow(x):
    """Compute the discrete Fourier Transform of the 1D array x"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)

def FFT(img):

    img = np.asarray(x, dtype=float)
    N = x.shape[0]

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return DFT_slow(img)
    else:
        img_even = FFT(img[::2])
        img_odd = FFT(img[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)

        return np.concatenate([img_even + factor[:int(N / 2)] * img_odd,
                               img_even + factor[int(N / 2):] * img_odd])


x = np.random.random(1024)
start=time.clock()
print(start)
FFT(x)
end=time.clock()
print(end-start)
start1=time.clock()
#print(start1)
np.fft.fft(x)
end1=time.clock()
print(end1-start1)


