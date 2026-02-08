import cv2
from controller import doorAutomate
import time

# Menggunakan haarcascade untuk mendeteksi wajah
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Inisialisasi pengenalan wajah
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")  # Pastikan file ini ada di direktori yang benar

# Daftar nama yang dikenali (sesuaikan dengan ID)
name_list = ["Ayah","Ayah","Ayah"]

# Membaca dan resize background
imgBackground = cv2.imread("background.png")
imgBackground = cv2.resize(imgBackground, (1430, 870))

# Membuka kamera
video = cv2.VideoCapture(0)

while True:
    # Membaca frame dari video
    ret, frame = video.read()
    if not ret:
        print("Failed to capture video.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.1, 5)

    # Variabel untuk menyimpan confidence terakhir
    last_conf = 0

    for (x, y, w, h) in faces:
        serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
        
        last_conf = conf  # Simpan nilai confidence terakhir
        accuracy = max(0, min(100, 100 - conf))  # Hitung persen akurasi
        
        if serial >= len(name_list):  # Memastikan indeks berada dalam range yang valid
            serial = 0  # Jika diluar range, gunakan "Tidak dikenali"
        
        if conf < 50:  # Jika confidence kurang dari 50, berarti wajah dikenali
            # Wajah dikenali, kotak hijau, nama, dan akurasi
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y-60), (x+w, y), (0, 255, 0), -1)
            cv2.putText(frame, f"{name_list[serial]} ({accuracy:.2f}% Akurasi)", (x, y-30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        else:
            # Wajah tidak dikenali, kotak merah, dan akurasi
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y-60), (x+w, y), (0, 0, 255), -1)
            cv2.putText(frame, f"Tidak dikenali ({accuracy:.2f}%)", (x, y-30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Resize frame menjadi 800x600
    frame = cv2.resize(frame, (800, 600))
    
    # Menempatkan frame video di sebelah kiri, sedikit bergeser ke kanan (20px dari kiri)
    x_offset = 20
    y_offset = ((870 - 600) // 2) + 60  # posisi vertikal di tengah background
    
    # Menyisipkan frame video ke background
    imgBackground[y_offset:y_offset + 600, x_offset:x_offset + 800] = frame
    
    # Menampilkan frame video di background
    cv2.imshow("Frame", imgBackground)
    
    # Mengontrol pintu dan keluar program
    k = cv2.waitKey(1)
    
    # Jika wajah dikenali dan tombol 'o' ditekan, buka pintu
    if k == ord('o') and last_conf < 50:  # Ubah nilai confidence ke 50
        doorAutomate(0)  # Buka pintu
        time.sleep(10)  # Tunggu 10 detik
        doorAutomate(1)  # Tutup pintu
        
    # Jika tombol 'q' ditekan, keluar dari loop
    if k == ord("q"):
        break

# Melepaskan kamera dan menutup semua jendela
video.release()
cv2.destroyAllWindows()
