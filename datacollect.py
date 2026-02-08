import cv2
import os

# Membuka kamera
video = cv2.VideoCapture(0)

# Menggunakan file video jika diperlukan
# video = cv2.VideoCapture("test.mp4")

# Menggunakan haarcascade untuk deteksi wajah
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Input ID dan Nama dari pengguna
id = input("Enter Your ID: ")
name = input("Enter Your Name: ")

# Membuat folder dataset jika belum ada
dataset_folder = 'datasets'
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

user_folder = os.path.join(dataset_folder, f'User.{str(id)}.{name}')
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

count = 0

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to capture video.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        # Simpan gambar wajah yang terdeteksi ke dalam folder dataset
        cv2.imwrite(os.path.join(user_folder, f'{name}.{str(count)}.jpg'), gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

    # Tampilkan jumlah gambar yang telah disimpan
    cv2.putText(frame, f'Images Saved: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Frame", frame)

    # Jika sudah menyimpan 500 gambar, hentikan atau tekan 'q' untuk keluar
    k = cv2.waitKey(1)
    if count >= 500 or k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
print("Dataset Collection Done.")