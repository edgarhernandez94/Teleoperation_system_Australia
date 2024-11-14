from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app)

# Ruta principal para servir la página web
@app.route('/')
def index():
    return render_template('index.html')

# Evento para recibir una imagen desde el cliente
@socketio.on('video_frame')
def handle_video_frame(data):
    # Recibir la imagen en base64 desde el cliente y retransmitirla a los navegadores conectados
    imagen_base64 = data.get('imagen')
    if imagen_base64:
        emit('video_frame', {'imagen': imagen_base64}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
