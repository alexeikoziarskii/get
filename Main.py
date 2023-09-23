import math
import os
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import cv2
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err
def psnr(original, contrast):
    mse = np.mean((original - contrast) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    PSNR = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return PSNR 

def compare_image(imageA, imageB, title):
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    p = psnr(imageA, imageB)
    fig = plt.figure(title)
    plt.suptitle("MSE: %.6f, SSIM: %.6f, PSNR: %.6f" % (m, s, p))
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis("off")
    
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis("off")
    plt.show()
img_orig = cv2.imread('pictures/originals/kodim09.png')
img_decomp = cv2.imread('pictures/decompressed/kodim9-art-scale-1_00x.png')
img_comp = cv2.imread('pictures/compressed/kodim09.jpg')
img_orig = cv2.resize(img_orig, (512, 512))
img_decomp = cv2.resize(img_decomp, (512, 512))
img_comp = cv2.resize(img_comp, (512, 512))
img_orig = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
img_decomp = cv2.cvtColor(img_decomp, cv2.COLOR_BGR2GRAY)
img_comp = cv2.cvtColor(img_comp, cv2.COLOR_BGR2GRAY)
compare_image(img_orig, img_decomp, 'ORIGINAL VS AI')
compare_image(img_orig, img_comp, 'ORIGINAL VS JPEG')



print('Hi')
