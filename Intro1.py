import cv2


IMAGE_PATH = "gambar.jpg"

img = cv2.imread(r"C:\Users\hi\OneDrive\Pictures\1643681004972.jpg")

if img is None:
    raise FileNotFoundError(
        f"Gambar tidak ditemukan: {IMAGE_PATH}. "
        "Pastikan path/nama filenya benar."
    )

print("Ukuran gambar (tinggi, lebar, channel):", img.shape)


hasil = img.copy()
hasil[:, :, 0] = 0   
hasil[:, :, 1] = 0   


cv2.imshow("Output", hasil)

cv2.waitKey(0)
cv2.destroyAllWindows()