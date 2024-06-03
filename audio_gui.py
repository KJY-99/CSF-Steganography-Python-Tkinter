import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
from audio_steganography import encode_wav, decode_wav
import wave
import pyaudio
import threading

def play_audio(file_path):
    if not file_path:
        messagebox.showerror("Error", "Please select a file to play.")
        return

    def play_thread():
        chunk = 1024
        try:
            wf = wave.open(file_path, 'rb')
        except Exception as e:
            messagebox.showerror("Error", "Failed to open audio file: File selected is not a .wav file.")
            return

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

    threading.Thread(target=play_thread).start()

def encode_file():
    cover_file = cover_file_entry.get()
    payload_file = payload_file_entry.get()

    if not cover_file or not payload_file:
        messagebox.showerror("Error", "Please select both cover and payload files.")
        return

    try:
        with open(payload_file, 'r') as f:
            text = f.read()
            payload_text_box.delete(1.0, tk.END)
            payload_text_box.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read payload file: {e}")
        return

    try:
        num_lsb = int(lsb_entry.get())
        if num_lsb < 1 or num_lsb > 8:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Number of LSBs must be between 1 and 8.")
        return

    try:
        encode_wav(cover_file, text, num_lsb)
        messagebox.showinfo("Success", "Text encoded successfully into 'encoded.wav'.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encode text: {e}")

def decode_file():
    stego_file = stego_file_entry.get()

    if not stego_file:
        messagebox.showerror("Error", "Please select the encoded .wav file")
        return

    try:
        num_lsb = int(lsb_entry.get())
        if num_lsb < 1 or num_lsb > 8:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Number of LSBs must be between 1 and 8.")
        return

    try:
        text = decode_wav(stego_file, num_lsb)
        messagebox.showinfo("Decoded Text", text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode text: {e}")

def on_drag_files(event, entry):
    file_path = event.data.strip('{}')
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def browse_cover_file():
    filename = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
    if filename:
        cover_file_entry.delete(0, tk.END)
        cover_file_entry.insert(0, filename)

def browse_payload_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        payload_file_entry.delete(0, tk.END)
        payload_file_entry.insert(0, filename)

def browse_stego_file():
    filename = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    if filename:
        stego_file_entry.delete(0, tk.END)
        stego_file_entry.insert(0, filename)

root = TkinterDnD.Tk()
root.title("Audio Steganography")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Cover file entry and buttons
tk.Label(frame, text="Cover File:").grid(row=0, column=0, padx=5, pady=5)
cover_file_entry = tk.Entry(frame, width=50)
cover_file_entry.grid(row=0, column=1, padx=5, pady=5)
cover_file_entry.drop_target_register(DND_FILES)
cover_file_entry.dnd_bind('<<Drop>>', lambda e: on_drag_files(e, cover_file_entry))
tk.Button(frame, text="Browse", command=browse_cover_file).grid(row=0, column=2, padx=5, pady=5)

# Payload file entry and buttons
tk.Label(frame, text="Payload File:").grid(row=1, column=0, padx=5, pady=5)
payload_file_entry = tk.Entry(frame, width=50)
payload_file_entry.grid(row=1, column=1, padx=5, pady=5)
payload_file_entry.drop_target_register(DND_FILES)
payload_file_entry.dnd_bind('<<Drop>>', lambda e: on_drag_files(e, payload_file_entry))
tk.Button(frame, text="Browse", command=browse_payload_file).grid(row=1, column=2, padx=5, pady=5)

# Payload text box
tk.Label(frame, text="Payload Text:").grid(row=2, column=0, padx=5, pady=5)
payload_text_box = scrolledtext.ScrolledText(frame, width=50, height=10)
payload_text_box.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

# Stego file entry and buttons
tk.Label(frame, text="Encoded File:").grid(row=3, column=0, padx=5, pady=5)
stego_file_entry = tk.Entry(frame, width=50)
stego_file_entry.grid(row=3, column=1, padx=5, pady=5)
stego_file_entry.drop_target_register(DND_FILES)
stego_file_entry.dnd_bind('<<Drop>>', lambda e: on_drag_files(e, stego_file_entry))
tk.Button(frame, text="Browse", command=browse_stego_file).grid(row=3, column=2, padx=5, pady=5)

# LSB entry
tk.Label(frame, text="Number of LSBs:").grid(row=4, column=0, padx=5, pady=5)
lsb_entry = tk.Entry(frame, width=5)
lsb_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
lsb_entry.insert(0, "1")

# Encode and Decode buttons
tk.Button(frame, text="Encode Text in Audio", command=encode_file).grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
tk.Button(frame, text="Decode Text from Audio", command=decode_file).grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

# Audio play buttons
tk.Button(frame, text="Play Cover Audio", command=lambda: play_audio(cover_file_entry.get())).grid(row=7, column=0, columnspan=1, padx=5, pady=5, sticky='ew')
tk.Button(frame, text="Play Encoded Audio", command=lambda: play_audio(stego_file_entry.get())).grid(row=7, column=1, columnspan=1, padx=5, pady=5, sticky='ew')

root.mainloop()
