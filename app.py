import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Archivo modificado: {event.src_path}, reiniciando el servidor...")
            self.process.terminate()
            self.process.wait()
            self.process = subprocess.Popen(['python3', 'index.py'])

if __name__ == "__main__":
    process = subprocess.Popen(['python3', 'index.py'])
    event_handler = ChangeHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)  # Observa la carpeta actual y todas las subcarpetas
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    process.terminate()
