"""
Face detection in a video using OpenCV (Python 3.13)
- Detects faces frame by frame
- Optionally saves the output video with detected faces
"""

import cv2

# Ruta del video
VIDEO_PATH = "video.mp4"  # cambia esto al nombre de tu video
OUTPUT_PATH = "output_detected_faces.mp4"  # video resultante

# Cargar clasificador Haar
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if face_cascade.empty():
    raise Exception("Error loading Haar cascade")

# Abrir video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise Exception("Cannot open video")

# Obtener propiedades del video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Crear VideoWriter para guardar salida
out = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (frame_width, frame_height)
)

while True:
    ret, frame = cap.read()
    if not ret:
        break  # fin del video

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Mostrar en pantalla
    cv2.imshow("Face Detection - Video", frame)

    # Guardar en video de salida
    out.write(frame)

    # Salir si se presiona ESC o 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
