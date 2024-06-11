import customtkinter
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox
import os, cv2, numpy
from PIL import Image, ImageTk
from img import image_resize, encode_img, decode_img
from video import video_encryption,video_decryption,image_to_binary,binary_to_image
from audio_steganography import encode_wav, decode_wav
import vlc, threading
import wave, pydub, pygame
from pygame import mixer

# Allow for TkDnD to utilise CTK
class App(customtkinter.CTk, TkinterDnD.DnDWrapper):

    def image_encode_and_display(self):
        if not self.listbox_data:
            messagebox.showerror("Error", "No image file added.")
            return
        if not self.tbox.get(1.0, "end-1c"):  # Check if textbox_data is empty or contains only whitespace
            messagebox.showerror("Error", " No text file added.")
            return
        try:
            # Call the encode function with the appropriate arguments
            encoded_image = encode_img(self.listbox_data, self.tbox.get(1.0, "end-1c"), self.bit_data)

            # Convert the encoded image to a format Tkinter can display
            resized_encoded_image = image_resize(encoded_image, height=400)
            resized_encoded_image_pil = Image.fromarray(cv2.cvtColor(resized_encoded_image, cv2.COLOR_BGR2RGB))
            resized_encoded_image_tk = ImageTk.PhotoImage(resized_encoded_image_pil)

            # save the output image (encoded image)
            cv2.imwrite("output.png", encoded_image)

            # Update the output image label
            self.output_image_label_text.configure(text='Encoded Image')
            self.output_image_label.configure(image=resized_encoded_image_tk)
            self.output_image_label.image = resized_encoded_image_tk  # Keep a reference to avoid garbage collection
            print("Encoding successful")

        except Exception as e:
            print(f"An error occurred: {e}")

    def encode_video(self):  
        video_file = self.video_file_listb.get(tk.ACTIVE)
        if not video_file:  
            messagebox.showerror("Error", "Please select a video file.")
            return

        text = self.payload_textbox.get("1.0", "end").strip()
        if not text:
            messagebox.showerror("Error", "Please insert a text payload.")
            return 

        bit_length = int(self.bit_slider.get())  # Ensure bit_length is an integer 
        try:  
            video_encryption(video_file, text, bit_length)  
            messagebox.showinfo("Success", "Text encoded successfully into video.")  
        except Exception as e:  
            messagebox.showerror("Error", f"Failed to encode text: {e}")  
            
    def play_video(self):  
        file_path = self.video_file_listb.get(tk.ACTIVE)
        if not file_path:
            messagebox.showerror("Error", "Please select a video file to play.") 
            return

        file_path = os.path.abspath(file_path)
        print(f"Attempting to play video: {file_path}")  

        def play_thread(): 
            try:  
                media = self.vlc_instance.media_new(file_path) 
                self.player.set_media(media) 
                self.player.set_hwnd(self.video_frame.winfo_id()) 
                self.player.play()  
            except Exception as e:  
                print(f"Error playing video: {e}")  
                messagebox.showerror("Error", f"Failed to play video: {e}")  

        threading.Thread(target=play_thread).start()  

    def stop_video(self):  
        self.player.stop() 

    def play_encoded_video(self):  
        file_path = "output_video.avi"
        if not file_path:  
            messagebox.showerror("Error", "Please encode a video file to play.") 
            return  

        file_path = os.path.abspath(file_path)
        print(f"Attempting to play video: {file_path}")  

        def play_thread(): 
            try:  
                media = self.vlc_instance.media_new(file_path) 
                self.encoded_player.set_media(media) 
                self.encoded_player.set_hwnd(self.encoded_video_frame.winfo_id()) 
                self.encoded_player.play()  
            except Exception as e:  
                print(f"Error playing video: {e}")  
                messagebox.showerror("Error", f"Failed to play video: {e}")  

        threading.Thread(target=play_thread).start()  

    def stop_encoded_video(self):  
        self.encoded_player.stop() 

    def play_audio(self):
        file_path = self.audio_file_listb.get(tk.ACTIVE)
        if not file_path:
            messagebox.showerror("Error", "Please select an audio file to play.")
            return

        def play_thread():
            try:
                mixer.init()
                mixer.music.load(file_path)
                mixer.music.play()

                while mixer.music.get_busy():
                    continue

                mixer.quit()
            except pygame.error as e:
                messagebox.showerror("Error", f"Failed to play audio file: {e}")

        threading.Thread(target=play_thread).start()

    def stop_audio(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    
    def play_encoded_audio(self):
        file_path = 'encoded.wav'
        if not file_path:
            messagebox.showerror("Error", "Please select an audio file to play.")
            return

        def play_thread():
            try:
                mixer.init()
                mixer.music.load(file_path)
                mixer.music.play()

                while mixer.music.get_busy():
                    continue

                mixer.quit()
            except pygame.error as e:
                messagebox.showerror("Error", f"Failed to play audio file: {e}")

        threading.Thread(target=play_thread).start()


    def encode_audio(self):
        cover_file = self.audio_file_listb.get(tk.ACTIVE)

        if not cover_file or not os.path.exists(cover_file):
            messagebox.showerror("Error", "Invalid file path or file does not exist.")
            return
        cover_file = os.path.abspath(cover_file)
        if not self.payload_audio_textbox.get(1.0, "end-1c"):  # Check if textbox_data is empty or contains only whitespace
            messagebox.showerror("Error", " No text file added.")
            return
        
        num_lsb = self.audio_bit_data  # Ensure bit_length is an integer 
        try:  
            encode_wav(cover_file, self.payload_audio_textbox.get(1.0, "end-1c"), num_lsb)  
            messagebox.showinfo("Success", "Text encoded successfully into audio.")  
        except Exception as e:  
            messagebox.showerror("Error", f"Failed to encode text: {e}")  

    def decode_file(self):
        stego_file = self.decode_listb.get(tk.ACTIVE)

        if not stego_file:
            messagebox.showerror("Error", "Please select the encoded .wav file")
            return
        num_lsb = self.audio_bit_data
            
        try:
            text = decode_wav(stego_file, num_lsb)
            messagebox.showinfo("Decoded Text", text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode text: {e}")


    def usedecodefunction(self):
        # Retrieve the selected bit value
        bit_value = self.decode_bit_data

        # Retrieve the value from the combobox
        selected_payload = self.decode_combobox.get()
        # Retrieve the filepath within the listbox
        decode_filepath = self.decode_listb.get(tk.ACTIVE)
        if decode_filepath.endswith(('jpg', 'png')):
            if selected_payload == "Text":
                decode_data = decode_img(decode_filepath, bit_value)
                self.decode_output_label.configure(text=decode_data)
            else:
                messagebox.showwarning("Not Supported", "Image decoding does not support " + selected_payload + " payloads")
        elif decode_filepath.endswith('avi'):
            decode_data = video_decryption(decode_filepath, bit_value)
            if selected_payload == "Text":
                self.decode_output_label.configure(text=decode_data)
            elif selected_payload == "Image":
                decode_image  = binary_to_image(decode_data)
                resized_decoded_image = image_resize(decode_image, height=400)
                resized_decoded_image_pil = Image.fromarray(cv2.cvtColor(resized_decoded_image, cv2.COLOR_BGR2RGB))
                resized_decoded_image_tk = ImageTk.PhotoImage(resized_decoded_image_pil)
                self.decode_output_label.configure(image=resized_decoded_image_tk)
                cv2.imwrite("video_output.png", decode_image)
            else:
                messagebox.showwarning("Not Supported", "Video decoding does not support " + selected_payload + " payloads")
        elif decode_filepath.endswith('wav'):
            if selected_payload == "Text":
                try:
                    text = decode_wav(decode_filepath, bit_value)
                    self.decode_output_label.configure(text=text)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to decode text: {e}")
            else:
                messagebox.showwarning("Not Supported", "Audio decoding does not support " + selected_payload + " payloads")
        else:
            messagebox.showwarning("Invalid Type", "Accepted cover : .png, .wav, .avi")
    

    def __init__(self):
        super().__init__()

        # Define TkDnD ver.
        self.TkdndVersion = TkinterDnD._require(self)
        self.bit_data = 1
        self.audio_bit_data = 1
        self.video_bit_data = 1
        self.decode_bit_data = 1
        self.current_screen = "image_screen"
        
        # Drag and Drop Method - Listbox: Get filepath to listbox (IMPT: Omit spaces in file path)
        def drop_inside_listbox(event, element):
            element.delete("0", "end") # Clear previous data
            file_path = event.data.strip("{}")
            element.insert("end", file_path)
            display_input_image(file_path)

        # Drag and Drop Method - Textbox: Strip text from file (IMPT: Omit spaces in file path)
        def drop_inside_textbox(event, element):
            element.delete("1.0", "end") # Clear previous data
            event.data = event.data.strip("}{")
            if event.data.endswith(".txt"):
                with open(event.data, "r") as file:
                    for line in file:
                        line = line.strip()
                        element.insert("end", f"{line}\n")

        # Image encode slider
        def image_slider_event(value):
            self.slider_label.configure(text="Selected number of bits: "+str(int(value)))
            self.bit_data = int(value)

        def video_slider_event(value):
            self.video_slider_label.configure(text="Selected number of bits: "+str(int(value)))
            self.video_bit_data = int(value)

        def audio_slider_event(value):
            self.audio_slider_label.configure(text="Selected number of bits: "+str(int(value)))
            self.audio_bit_data = int(value)

        # Decode slider
        def decode_slider_event(value):
            self.decode_slider_label.configure(text="Selected number of bits for decoding: "+str(int(value)))
            self.decode_bit_data = int(value)

        # Function to display image in label
        def display_input_image(file_path):
            img = cv2.imread(file_path)
            if not isinstance(img, numpy.ndarray):
                return
            img = image_resize(img, height=400)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            if self.current_screen == "image_screen":
                self.input_image_label_text.configure(text='Normal Image')
                self.input_image_label.configure(image=img)
                self.input_image_label.image = img
            
        # Define Title, Window size and Grid layout
        self.title("CSF Steganography Group 42")
        self.geometry("1280x800")
        # Configure Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load example images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                       size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))

        # Navigation icons
        self.chat_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.video_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "video_icon.png")), size=(20, 20))
        self.volume_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "volume_icon.png")), size=(20, 20))

        # Side Navigation (ALL SCREENS)
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Steganography",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.image_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                           border_spacing=10, text="Image",
                                                           fg_color="transparent", text_color=("gray10", "gray90"),
                                                           hover_color=("gray70", "gray30"),
                                                           image=self.chat_image, anchor="w",
                                                           command=self.image_screen_button_event)
        self.image_screen_button.grid(row=2, column=0, sticky="ew")
        self.video_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                           border_spacing=10, text="Video",
                                                           fg_color="transparent", text_color=("gray10", "gray90"),
                                                           hover_color=("gray70", "gray30"),
                                                           image=self.video_image, anchor="w",
                                                           command=self.video_screen_button_event)
        self.video_screen_button.grid(row=3, column=0, sticky="ew")
        self.audio_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                           border_spacing=10, text="Audio",
                                                           fg_color="transparent", text_color=("gray10", "gray90"),
                                                           hover_color=("gray70", "gray30"),
                                                           image=self.volume_image, anchor="w",
                                                           command=self.audio_screen_button_event)
        self.audio_screen_button.grid(row=4, column=0, sticky="ew")
        self.decode_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                           border_spacing=10, text="Decode",
                                                           fg_color="transparent", text_color=("gray10", "gray90"),
                                                           hover_color=("gray70", "gray30"),
                                                           image=self.image_icon_image,anchor="w",
                                                           command=self.decode_screen_button_event)
        self.decode_screen_button.grid(row=5, column=0, sticky="ew")

        # IMAGE SCREEN (ERNEST & JY)
        self.image_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.image_screen.grid_columnconfigure(0, weight=1)
        self.image_screen.grid_columnconfigure(1, weight=1)

        # Textbox
        self.text_label = customtkinter.CTkLabel(self.image_screen, text="Insert text file payload:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.text_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.tbox = tk.Text(self.image_screen, width=70, height=25)
        self.tbox.grid(row=1, column=0, columnspan=3, padx=15, pady=10, sticky="nsew")
        self.tbox.drop_target_register(DND_FILES)
        self.tbox.dnd_bind("<<Drop>>", lambda event: drop_inside_textbox(event, element=self.tbox))

        # Listbox to drag and drop file path
        self.file_label = customtkinter.CTkLabel(self.image_screen, text="Insert cover image:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.file_label.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.listb = tk.Listbox(self.image_screen, selectmode=tk.SINGLE, background="#ffe0d6", width=50, height=2, font=20)
        self.listb.grid(row=3, column=0, columnspan=3, padx=15, pady=10, sticky='ew')
        self.listb.drop_target_register(DND_FILES)
        self.listb.dnd_bind("<<Drop>>", lambda event: drop_inside_listbox(event, element=self.listb))

        # Bit Selection Slider
        bit_value = tk.IntVar()
        self.slider_label = customtkinter.CTkLabel(self.image_screen, text="Selected number of bits: 1", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.slider_label.grid(row=4, column=0, padx=15, pady=(10, 0), sticky="ew")
        self.bit_slider = customtkinter.CTkSlider(self.image_screen, from_=1, to=8, number_of_steps=7, command=image_slider_event, variable=bit_value)
        self.bit_slider.grid(row=5, column=0, columnspan=1, padx=15, pady=5, sticky="ew")

        # Encode button
        self.encode_button = customtkinter.CTkButton(self.image_screen, text="Encode", command=self.image_encode_and_display)
        self.encode_button.grid(row=5, column=1, columnspan=1, padx=15, pady=5, sticky="ew")

        # Label for displaying the input image
        self.input_image_label_text = customtkinter.CTkLabel(self.image_screen, text="", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.input_image_label_text.grid(row=6, column=0, padx=15, pady=(30, 5), sticky="ew")
        self.input_image_label = customtkinter.CTkLabel(self.image_screen, text="", image=None)
        self.input_image_label.grid(row=7, column=0, padx=15, pady=5, sticky="ew")

        # Label for displaying the output image
        self.output_image_label_text = customtkinter.CTkLabel(self.image_screen, text="", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.output_image_label_text.grid(row=6, column=1, padx=15, pady=(30, 5), sticky="ew")
        self.output_image_label = customtkinter.CTkLabel(self.image_screen, text="", image=None)
        self.output_image_label.grid(row=7, column=1, padx=15, pady=5, sticky="ew")

        # VIDEO SCREEN
        self.video_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.video_screen.grid_columnconfigure(0, weight=1)
        self.video_screen.grid_columnconfigure(1, weight=1)

        # Payload textbox
        self.payload_label = customtkinter.CTkLabel(self.video_screen, text="Insert text file payload:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.payload_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.payload_textbox = tk.Text(self.video_screen, width=70, height=25) 
        self.payload_textbox.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="ew") 
        self.payload_textbox.drop_target_register(DND_FILES)
        self.payload_textbox.dnd_bind("<<Drop>>", lambda event: drop_inside_textbox(event, element=self.payload_textbox))
        
        # Video listbox
        self.video_file_label = customtkinter.CTkLabel(self.video_screen, text="Drop video file here:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.video_file_label.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.video_file_listb = tk.Listbox(self.video_screen, font=20, background="#ffe0d6", width=50, height=2)
        self.video_file_listb.grid(row=3, column=0, columnspan=2, padx=15, pady=10, sticky="ew")  
        self.video_file_listb.drop_target_register(DND_FILES)
        self.video_file_listb.dnd_bind("<<Drop>>", lambda event: drop_inside_listbox(event, element=self.video_file_listb))

        # Bit Selection Slider
        bit_value = tk.IntVar()
        self.video_slider_label = customtkinter.CTkLabel(self.video_screen, text="Selected number of bits: 1", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.video_slider_label.grid(row=4, column=0, padx=15, pady=(10, 0), sticky="ew")
        self.video_bit_slider = customtkinter.CTkSlider(self.video_screen, from_=1, to=8, number_of_steps=7, command=video_slider_event, variable=bit_value)
        self.video_bit_slider.grid(row=5, column=0, columnspan=1, padx=15, pady=5, sticky="ew")

        # Video encode button
        self.encode_button = customtkinter.CTkButton(self.video_screen, text="Encode", command=self.encode_video)
        self.encode_button.grid(row=5, column=1, columnspan=1, padx=15, pady=10, sticky="ew")

        # Vlc player for video
        self.video_frame = tk.Frame(self.video_screen, bg='black', width=40, height=560)  
        self.video_frame.grid(row=6, column=0, columnspan=1, padx=15, pady=10, sticky="ew")  
        self.video_frame.grid_propagate(False)

        self.encoded_video_frame = tk.Frame(self.video_screen, bg='black', width=40, height=560)  
        self.encoded_video_frame.grid(row=6, column=1, columnspan=1, padx=15, pady=10, sticky="ew")  
        self.encoded_video_frame.grid_propagate(False)
        
        # Play / Stop button
        self.play_button = customtkinter.CTkButton(self.video_screen, text="Play Cover Video", command=self.play_video)
        self.play_button.grid(row=7, column=0, columnspan=1, padx=15, pady=10)  
        self.stop_button = customtkinter.CTkButton(self.video_screen, text="Stop Cover Video", command=self.stop_video)  
        self.stop_button.grid(row=8, column=0, columnspan=1, padx=15, pady=10)
        
        self.play_encoded_button = customtkinter.CTkButton(self.video_screen, text="Play Encoded Video", command=self.play_encoded_video)
        self.play_encoded_button.grid(row=7, column=1, padx=15, pady=10)
        self.stop_encoded_button = customtkinter.CTkButton(self.video_screen, text="Stop Encoded Video", command=self.stop_encoded_video)  
        self.stop_encoded_button.grid(row=8, column=1, padx=15, pady=10)

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.encoded_vlc_instance = vlc.Instance()
        self.encoded_player = self.encoded_vlc_instance.media_player_new()

        # AUDIO SCREEN (INSERT YOUR UI ELEMENTS HERE) [SHIFA & JING YI]
        self.audio_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.audio_screen.grid_columnconfigure(0, weight=1)
        self.audio_screen.grid_columnconfigure(1, weight=1)

        # Payload textbox
        self.audio_text_label = customtkinter.CTkLabel(self.audio_screen, text="Insert text file payload:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.audio_text_label.grid(row=0, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        self.payload_audio_textbox = tk.Text(self.audio_screen, width=70, height=25)
        self.payload_audio_textbox.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="nesw")
        self.payload_audio_textbox.drop_target_register(DND_FILES)
        self.payload_audio_textbox.dnd_bind("<<Drop>>", lambda event: drop_inside_textbox(event, element=self.payload_audio_textbox))

        # Audio label dropbox
        self.audio_file_label = customtkinter.CTkLabel(self.audio_screen, text="Drop audio file here:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.audio_file_label.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        self.audio_file_listb = tk.Listbox(self.audio_screen, background="#ffe0d6", width=50, height=2, font=20)
        self.audio_file_listb.grid(row=3, column=0, columnspan=2, padx=15, pady=10, sticky="nesw")  
        self.audio_file_listb.drop_target_register(DND_FILES)
        self.audio_file_listb.dnd_bind("<<Drop>>", lambda event: drop_inside_listbox(event, element=self.audio_file_listb))

        # Bit Selection Slider
        bit_value = tk.IntVar()
        self.audio_slider_label = customtkinter.CTkLabel(self.audio_screen, text="Selected number of bits: 1", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.audio_slider_label.grid(row=4, column=0, padx=15, pady=(10, 0), sticky="ew")
        self.audio_bit_slider = customtkinter.CTkSlider(self.audio_screen, from_=1, to=8, number_of_steps=7, command=audio_slider_event, variable=bit_value)
        self.audio_bit_slider.grid(row=5, column=0, columnspan=1, padx=15, pady=5, sticky="ew")

        # Audio Encode Button
        self.audio_encode_button = customtkinter.CTkButton(self.audio_screen, text="Encode", command=self.encode_audio)
        self.audio_encode_button.grid(row=5, column=1, columnspan=1, padx=15, pady=5, sticky="ew")

        # Play/stop Audio Button
        self.play_button = customtkinter.CTkButton(self.audio_screen, text="Play Cover Audio", command=self.play_audio)
        self.play_button.grid(row=6, column=0, padx=15, pady=10) 
        self.stop_button = customtkinter.CTkButton(self.audio_screen, text="Stop Cover Audio", command=self.stop_audio)
        self.stop_button.grid(row=7, column=0, padx=15, pady=10)

        # Play/stop Encoded Audio Button
        self.play_button = customtkinter.CTkButton(self.audio_screen, text="Play Encoded Audio", command=self.play_encoded_audio)
        self.play_button.grid(row=6, column=1, padx=15, pady=10) 
        self.stop_button = customtkinter.CTkButton(self.audio_screen, text="Stop Encoded Cover Audio", command=self.stop_audio)
        self.stop_button.grid(row=7, column=1, padx=15, pady=10)

        # DECODE SCREEN (USED FOR ALL FORMATS OF DECODING)
        self.decode_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.decode_screen.grid_columnconfigure(0, weight=1)
        self.decode_screen.grid_columnconfigure(1, weight=1)

        # Listbox to drag and drop file path
        self.decode_file_label = customtkinter.CTkLabel(self.decode_screen, text="Drop cover file here:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.decode_file_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.decode_listb = tk.Listbox(self.decode_screen, selectmode=tk.SINGLE, background="#ffe0d6", width=50, height=2, font=20)
        self.decode_listb.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky='ew')
        self.decode_listb.drop_target_register(DND_FILES)
        self.decode_listb.dnd_bind("<<Drop>>", lambda event: drop_inside_listbox(event, element=self.decode_listb))

        # Dropdown box
        self.decode_text_label = customtkinter.CTkLabel(self.decode_screen, text="Select file payload used in encoding process:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.decode_text_label.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.decode_combobox = customtkinter.CTkComboBox(self.decode_screen,state="readonly", values=['Text', 'Image', 'Audio'], width=300, height=25)
        self.decode_combobox.set('Text')
        self.decode_combobox.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self.selected_payload = self.decode_combobox.get()

        # Bit Selection Slider
        decode_bit_data = tk.IntVar()
        self.decode_slider_label = customtkinter.CTkLabel(self.decode_screen, font=customtkinter.CTkFont(size=13, weight="bold"), text="Selected number of bits for decoding: 1")
        self.decode_slider_label.grid(row=2, column=1, padx=15, pady=(10, 0), sticky="w")
        self.decode_bit_slider = customtkinter.CTkSlider(self.decode_screen, from_=1, to=8, number_of_steps=7, command=decode_slider_event, variable=decode_bit_data)
        self.decode_bit_slider.grid(row=3, column=1, padx=15, pady=5, sticky="ew")

        # Decode Button
        self.decode_button = customtkinter.CTkButton(self.decode_screen, font=customtkinter.CTkFont(size=13, weight="bold"), text="Decode", command=self.usedecodefunction)
        self.decode_button.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

        # Output screen
        self.decode_output_label = customtkinter.CTkLabel(self.decode_screen, text="", image=None, wraplength=500)
        self.decode_output_label.grid(row=6, column=0, columnspan=3, padx=10, pady=(50, 5), sticky="ew")

        # Select default frame - IMAGES
        self.select_frame_by_name("image_screen")

    def select_frame_by_name(self, name):
        # Change side nav button color on select
        self.current_screen = name
        print(self.current_screen)
        self.image_screen_button.configure(fg_color=("gray75", "gray25") if name == "image_screen" else "transparent")
        self.video_screen_button.configure(fg_color=("gray75", "gray25") if name == "video_screen" else "transparent")
        self.audio_screen_button.configure(fg_color=("gray75", "gray25") if name == "audio_screen" else "transparent")
        self.decode_screen_button.configure(fg_color=("gray75", "gray25") if name == "decode_screen" else "transparent")

        # Add and destroy frame
        if name == "image_screen":
            self.image_screen.grid(row=0, column=1, sticky="nsew")
        else:
            self.image_screen.grid_forget()
        if name == "video_screen":
            self.video_screen.grid(row=0, column=1, sticky="nsew")
        else:
            self.video_screen.grid_forget()
        if name == "audio_screen":
            self.audio_screen.grid(row=0, column=1, sticky="nsew")
        else:
            self.audio_screen.grid_forget()
        if name == "decode_screen":
            self.decode_screen.grid(row=0, column=1, sticky="nsew")
        else:
            self.decode_screen.grid_forget()

    
    def image_screen_button_event(self):
        self.select_frame_by_name("image_screen")

    def video_screen_button_event(self):
        self.select_frame_by_name("video_screen")

    def audio_screen_button_event(self):
        self.select_frame_by_name("audio_screen")

    def decode_screen_button_event(self):
        self.select_frame_by_name("decode_screen")

# Run Application
if __name__ == "__main__":
    app = App()
    app.mainloop()
