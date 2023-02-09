import webview
from app import app
from flask_cors import CORS
import threading
from os import path

path_to_dat = path.abspath(path.join(path.dirname(__file__), "gui/index.html"))

if __name__ == "__main__":

    print(path_to_dat)

    CORS(app)

    # recipe from https://thewebdev.info/2022/04/03/how-to-start-a-python-flask-application-in-separate-thread/
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    window = webview.create_window("Drama Llama!", "http://localhost:3000")
    webview.start()
