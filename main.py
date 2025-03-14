import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("Hello i am from the main root file.")

BOT_SCRIPT = "src/main.py"  # The name of your bot script
process = None


def restart_bot():
    global process
    if process:
        print("Restarting bot...")
        process.kill()  # Kill the existing process
        time.sleep(1)
    process = subprocess.Popen(["python", BOT_SCRIPT])  # Restart the bot


class RestartOnChange(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Only restart on Python file changes
            print(f"File changed: {event.src_path}")
            restart_bot()


if __name__ == "__main__":
    path = "."  # Watch the current directory
    event_handler = RestartOnChange()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print("Starting bot and watching for changes...")
    restart_bot()  # Start bot initially
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        process.kill()

    observer.join()
