import cv2
 
 
def tint_merah(frame):
    
    hasil = frame.copy()
    hasil[:, :, 0] = 0  
    hasil[:, :, 1] = 0  
    return hasil
 
 
def main():
    cap = cv2.VideoCapture(0)
 
    if not cap.isOpened():
        print("Tidak bisa membuka webcam")
        return
 
    print("Tekan 'q' untuk keluar.")
 
    while True:
        success, frame = cap.read()
        if not success:
            print("Gagal membaca frame dari webcam")
            break
 
        frame = cv2.flip(frame, 1)  
        frame_merah = tint_merah(frame)
 
        cv2.imshow("Output", frame_merah)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    cap.release()
    cv2.destroyAllWindows()
 
 
if __name__ == "__main__":
    main()