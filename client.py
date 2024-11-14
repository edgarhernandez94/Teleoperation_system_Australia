import cv2
import base64
import socketio
import time

# Crear una instancia del cliente SocketIO
sio = socketio.Client()

SERVER_URL = 'http://127.0.0.1:5000'

@sio.event
def connect():
    print("Conectado al servidor")

@sio.event
def disconnect():
    print("Desconectado del servidor")

def capturar_y_enviar_imagen():
    # Iniciar la cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara.")
        return

    while True:
        # Leer un frame de la cámara
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede leer el frame de la cámara.")
            break

        # Codificar la imagen en formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        imagen_base64 = base64.b64encode(buffer).decode('utf-8')

        # Enviar la imagen al servidor
        sio.emit('video_frame', {'imagen': 'data:image/jpeg;base64,' + imagen_base64})

        # Esperar un poco antes de enviar el siguiente frame
        time.sleep(0.1)

    # Liberar la cámara
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sio.connect(SERVER_URL)
    capturar_y_enviar_imagen()
