from pylab import *
from scipy.ndimage import filters
import cv2

def plot_s(p, labels, data2, data3, title):
    fig = p.gcf()
    ax = p.gca()#subplots(figsize=(9,6),dpi=300)
    width_1 = 0.4
    ax.bar(np.arange(len(data2)),data2,width=width_1,tick_label=labels,color='b',label = "strick")
    ax.bar(np.arange(len(data3))+width_1,data3,width=width_1,tick_label=labels,color='r',label="fuzzy")
    ax.set_ylim([0.0,1.0])
    p.title(title)
    p.ylabel('v')
    ax.legend()
    p.tight_layout()
        
def edge_bi(img):
    bi_img = cv2.bilateralFilter(img, 0, 100, 5)
    return bi_img

def edge_shift(img):
    try:
        shift_img = cv2.pyrMeanShiftFiltering(img, 10, 50)
        return shift_img
    except Exception as e:
        return None


def histeq_grey(im, nbr_bins=128):
    imhist, bins = histogram(im.flatten(), nbr_bins)
    cdf = imhist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    im2 = interp(im.flatten(), bins[:-1], cdf)
    return (im2.reshape(im.shape), cdf)

def histeq_rgb(im, nbr_bins=128):
    image = zeros(im.shape)
    for i in range(3):
        image[:, :, i] = histeq_grey(im[:, :, i].astype('uint8'))[0].astype('uint8')
    return image #.astype('uint8')

def gaussian_grey(img, delta):
    img2 = zeros(img.shape)
    img2 = filters.gaussian_filter(img, delta)
    return img2 #.astype('uint8')

def gaussian_rgb(img, delta):
    image = zeros(img.shape)
    for i in range(3):
        image[:, :, i] = gaussian_grey(img[:, :, i], delta)
    return image #.astype('uint8')

    
def sobel(img):
    x=cv2.Sobel(img,cv2.CV_16S,1,0)
    y=cv2.Sobel(img,cv2.CV_16S,0,1)
    
    absx=cv2.convertScaleAbs(x)
    absy=cv2.convertScaleAbs(y)

    dist=cv2.addWeighted(absx,0.5,absy,0.5,0)
    return dist

def denoise_grey(im, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
    m,n = im.shape
    U = U_init
    Px = im
    Py = im
    error = 1
    while(error > tolerance):
        Uold = U
        GradUx = roll(U, -1, axis=1)- U
        GradUy = roll(U, -1, axis=0) - U
        PxNew = Px + (tau / tv_weight) * GradUx
        PyNew = Py + (tau / tv_weight) * GradUy
        NormNew = maximum(1, sqrt(PxNew**2 + PyNew**2))
        Px = PxNew / NormNew
        Py = PyNew / NormNew
        RxPx = roll(Px, 1, axis=1)
        RyPy = roll(Py, 1, axis=0)
        
        DivP = (Px - RxPx) + (Py - RyPy)
        U = im + tv_weight*DivP
        
        error = linalg.norm(U - Uold) / sqrt(n*m)
    return U, im-U

def denoise_rgb(im, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
    images = zeros(im.shape)
    noise = zeros(im.shape)

    for i in range(3):
        images[:,:,i], noise[:,:,i] = denoise_grey(im[:,:,i], im[:,:,i], tolerance, tau, tv_weight)

    return images, noise



def color_denoise_cv(img):
    imgx = zeros(img.shape)
    img2 = cv2.fastN1MeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    return img2

def m_denoise_grey(img):
    img2 = zeros(img.shape)
    img2 = cv2.fastN1MeansDenoising(img, None, 10, 10, 7, 21)
    return img2 #.astype('uint8')

def m_denoise_color(img):
    image = zeros(img.shape)
    for i in range(3):
        image[:, :, i] = m_denoise_grey(img[:, :, i])
    return image #.astype('uint8')

def gaussian_rgb(img, delta):
    image = zeros(img.shape)
    for i in range(3):
        image[:, :, i] = gaussian_grey(img[:, :, i], delta)
    return image #.astype('uint8')

def fft_filter_grey(img):
    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    rows, cols = img.shape
    crow,ccol = int(rows/2) , int(cols/2)

    # create a mask first, center square is 1, remaining all zeros
    mask = np.zeros((rows,cols,2),np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 1

    # apply mask and inverse DFT
    fshift = dft_shift*mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    return img_back, 