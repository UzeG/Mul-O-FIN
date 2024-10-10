# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:42:52 2024

@author: xiaol
"""

import subprocess
import tkinter as tk
from threading import Thread

# Define the path to the .exe file
exe_path = r'manage/manage.exe'

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Django Server Configuration")
        self.geometry("800x600")
        
        # Create a text widget to display output
        self.output_text = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.output_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)
        
        # Create labels and entry fields
        self.address_label = tk.Label(self, text="Server Address (IP:Port): ")
        self.address_label.pack()
        
        # Initialize the entry field with a default value
        default_address = "127.0.0.1:8000"
        self.address_entry = tk.Entry(self)
        self.address_entry.insert(0, default_address)  # Set default value
        self.address_entry.pack()
        
        # Create a button
        self.start_button = tk.Button(self, text="Start Server", command=self.start_server)
        self.start_button.pack()
        
        # Store the user input address
        self.server_address = ""
        self.process = None
    
    def start_server(self):
        # Clear the text widget content
        self.clear_output()
        
        # Get the user input address
        self.server_address = self.address_entry.get()
        
        # Build the command
        address_parts = self.server_address.split(':')
        if len(address_parts) == 2:
            ip = address_parts[0]
            port = address_parts[1]
            command = [exe_path, 'runserver', f'{ip}:{port}', '--noreload']
            
            # Display information about starting the server
            self.append_output(f"Starting server at {self.server_address}.\n")
            
            # Start the subprocess and read its output in a new thread
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.output_thread = Thread(target=self.read_process_output)
            self.output_thread.start()
        else:
            self.append_output("Invalid server address format. Please use IP:Port.\n")
    
    def append_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)  # Auto-scroll to the bottom
        self.output_text.config(state=tk.DISABLED)
        self.update_idletasks()  # Update the GUI
    
    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def read_process_output(self):
        try:
            for line in iter(self.process.stdout.readline, ''):
                self.append_output(line)
        finally:
            if self.process is not None:
                self.process.terminate()
                self.process.wait()
                self.append_output("Server has been terminated.\n")
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()
