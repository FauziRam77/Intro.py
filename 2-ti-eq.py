

import math
import cv2
import numpy as np

L = 256  

def clamp(v):
    v = int(round(v))
    if v < 0:
        return 0
    if v > L - 1:
        return L - 1
    return v


def to_gray(img_bgr):
    h, w = img_bgr.shape[:2]
    gray = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            b, g, r = img_bgr[i, j]
            gray[i, j] = clamp(0.299 * r + 0.587 * g + 0.114 * b)
    return gray


def apply_lut(img, lut):
    h, w = img.shape
    out = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            out[i, j] = lut[img[i, j]]
    return out



def hitung_histogram(img):
    hist = [0] * L
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            hist[img[i, j]] += 1
    return hist



def lut_negatif():
   
    return [clamp((L - 1) - r) for r in range(L)]


def lut_log(c=None):
    
    if c is None:
        c = (L - 1) / math.log(L)
    return [clamp(c * math.log(1 + r)) for r in range(L)]


def lut_gamma(gamma, c=1.0):
    
    return [clamp((L - 1) * c * ((r / (L - 1)) ** gamma)) for r in range(L)]


def lut_contrast_stretching(hist):
    
    rmin = 0
    while rmin < L - 1 and hist[rmin] == 0:
        rmin += 1
    rmax = L - 1
    while rmax > 0 and hist[rmax] == 0:
        rmax -= 1
    if rmax == rmin:
        return list(range(L))
    return [clamp((r - rmin) / (rmax - rmin) * (L - 1)) for r in range(L)]


def lut_threshold(T=128):
    
    return [(L - 1) if r >= T else 0 for r in range(L)]



def ekualisasi_histogram(img):

    h, w = img.shape
    total = h * w

    hist = hitung_histogram(img)

    pdf = [hist[k] / total for k in range(L)]

    cdf = [0.0] * L
    kumulatif = 0.0
    for k in range(L):
        kumulatif += pdf[k]
        cdf[k] = kumulatif

    lut = [clamp((L - 1) * cdf[k]) for k in range(L)]
    hasil = apply_lut(img, lut)
    return hasil, hist, cdf



def tampil(nama, citra, lebar=600, tinggi=600):
   
    tinggi = int(citra.shape[0] * lebar / citra.shape[1])
    cv2.namedWindow(nama, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(nama, lebar, tinggi)
    cv2.imshow(nama, citra)


def main():
    path = r"C:\Users\hi\OneDrive\Pictures\1643681004972.jpg"  
    img = cv2.imread(path)
    if img is None:
        print(f"Gambar '{path}' tidak ditemukan. Ganti variabel 'path'.")
        return

    gray = to_gray(img)
    hist = hitung_histogram(gray)

    # Transformasi intensitas
    negatif = apply_lut(gray, lut_negatif())
    logaritma = apply_lut(gray, lut_log())
    gamma_05 = apply_lut(gray, lut_gamma(0.5))
    gamma_20 = apply_lut(gray, lut_gamma(2.0))
    stretching = apply_lut(gray, lut_contrast_stretching(hist))
    biner = apply_lut(gray, lut_threshold(128))

    # Ekualisasi histogram
    equalized, _, _ = ekualisasi_histogram(gray)

    tampil("Asli (grayscale)", gray)
    tampil("Negatif", negatif)
    tampil("Log", logaritma)
    tampil("Gamma 0.5", gamma_05)
    tampil("Gamma 2.0", gamma_20)
    tampil("Contrast Stretching", stretching)
    tampil("Threshold 128", biner)
    tampil("Ekualisasi Histogram", equalized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    quit = input("ketik 'q' untuk keluar: ")




if __name__ == "__main__":
    main()