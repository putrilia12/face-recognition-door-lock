import cv2
import os
import numpy as np

# Menggunakan haarcascade untuk deteksi wajah
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Inisialisasi pengenalan wajah
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Folder dataset
dataset_folder = 'datasets'

# Menyimpan ID dan nama
faces = []
ids = []

# Mengumpulkan data untuk pelatihan
for user_folder in os.listdir(dataset_folder):
    user_path = os.path.join(dataset_folder, user_folder)
    
    # Pastikan user_path adalah direktori
    if not os.path.isdir(user_path):
        print(f"Skipping non-directory: {user_path}")
        continue  # Lewati jika bukan folder

    for image_file in os.listdir(user_path):
        # Membaca gambar
        image_path = os.path.join(user_path, image_file)
        
        # Pastikan itu adalah file gambar
        if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Skipping non-image file: {image_path}")
            continue  # Lewati jika bukan file gambar

        image = cv2.imread(image_path)

        if image is None:
            print(f"Failed to read image: {image_path}")
            continue  # Lewati gambar yang tidak bisa dibaca

        # Mengubah gambar ke grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Deteksi wajah
        faces_detected = facedetect.detectMultiScale(gray, 1.3, 5)

        if len(faces_detected) == 0:
            print(f"No faces detected in image: {image_path}")
            continue  # Lewati jika tidak ada wajah yang terdeteksi

        for (x, y, w, h) in faces_detected:
            # Simpan wajah dan ID pengguna
            faces.append(gray[y:y+h, x:x+w])
            # Ambil ID dari nama folder (misalnya User.1.Name)
            try:
                id = int(user_folder.split('.')[1])  # Mengambil ID dari nama folder
                ids.append(id)
            except (IndexError, ValueError):
                print(f"Invalid ID in folder name: {user_folder}")
                continue

# Melatih model dengan data yang dikumpulkan
if len(faces) > 0 and len(ids) > 0:
    recognizer.train(faces, np.array(ids))
    # Simpan model ke file
    recognizer.save('trainer.yml')
    print("Training Complete. Model saved as 'trainer.yml'.")
else:
    print("No data to train. Please check your dataset.")