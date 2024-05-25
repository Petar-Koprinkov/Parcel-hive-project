from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from multiprocessing import Queue, Process, Event
import time
import cv2
from pynput import mouse
from database import insert_event

app = Flask(__name__)
socketio = SocketIO(app)

event_queue = Queue()
stop_event = Event()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    emit('status', {'data': 'Connected'})


def mouse_listener(queue, stop_event):
    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            print(f"Mouse clicked at ({x}, {y}) with the left button on the mouse")
            queue.put(('click', (x, y)))
            socketio.emit('mouse_click', {'x': x, 'y': y})

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    stop_event.wait()
    listener.stop()

def webcam_capture(queue, stop_event):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        if not queue.empty():
            event = queue.get_nowait()
            if event[0] == 'click':
                x, y = event[1]
                timestamp = int(time.time())
                image_path = f'static/capture_{timestamp}.png'
                cv2.imwrite(image_path, frame)
                print(f'Image captured and saved as {image_path} at coordinates ({x}, {y})')
                insert_event(x, y, image_path)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    p1 = Process(target=mouse_listener, args=(event_queue, stop_event))
    p2 = Process(target=webcam_capture, args=(event_queue, stop_event))

    p1.start()
    p2.start()

    try:
        socketio.run(app, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        stop_event.set()
        p1.join()
        p2.join()