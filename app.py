import customtkinter
import tkinter as tk
import os, cv2

from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from img import image_resize
from img import encode, decode

# Allow for TkDnD to utilise CTK
class App(customtkinter.CTk, TkinterDnD.DnDWrapper):

    def image_encode_and_display(self):
        if not self.listbox_data:
            print("Error: No image file added.")
            return
        if not self.tbox.get(1.0, "end-1c"):  # Check if textbox_data is empty or contains only whitespace
            print("Error: No text file added.")
            return
        try:
            # Call the encode function with the appropriate arguments
            encoded_image = encode(self.listbox_data, self.tbox.get(1.0, "end-1c"), self.bit_data)

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

    def __init__(self):
        super().__init__()

        # Define TkDnD ver.
        self.TkdndVersion = TkinterDnD._require(self)
        self.listbox_data = ""
        self.bit_data = 1

        # Drag and Drop Method - Listbox: Get filepath to listbox (IMPT: Omit spaces in file path)
        def drop_inside_listbox(event, element):
            file_path = event.data.strip("}{")
            element.insert("end", file_path)
            self.listbox_data = file_path
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

        # Decode slider
        def decode_slider_event(value):
            self.decode_slider_label.configure(text="Selected number of bits: "+str(int(value)))
            self.decode_bit_value = int(value)

        # Function to display image in label
        def display_input_image(file_path):
            img = cv2.imread(file_path)
            img = image_resize(img, height=400)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.input_image_label_text.configure(text='Normal Image')
            self.input_image_label.configure(image=img)
            self.input_image_label.image = img

        # Define Title, Window size and Grid layout
        self.title("CSF Steganography Group --")
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
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.video_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "video_icon.png")), size=(20, 20))
        self.volume_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "volume_icon.png")), size=(20, 20))

        # Side Navigation (ALL SCREENS)
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Steganography",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
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

        # DASHBOARD SCREEN
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Image Example
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # Buttons 1 - 4 Example
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # IMAGE SCREEN (ERNEST & JY)
        self.image_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.image_screen.grid_columnconfigure(0, weight=1)
        self.image_screen.grid_columnconfigure(1, weight=1)

        # Textbox
        self.text_label = customtkinter.CTkLabel(self.image_screen, text="Insert text file payload:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.text_label.grid(row=0, column=0, columnspan=1)
        self.tbox = tk.Text(self.image_screen, width=70, height=25)
        self.tbox.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        self.tbox.drop_target_register(DND_FILES)
        self.tbox.dnd_bind("<<Drop>>", lambda event: drop_inside_textbox(event, element=self.tbox))

        # Listbox to drag and drop file path
        self.file_label = customtkinter.CTkLabel(self.image_screen, text="Insert cover image:",font=customtkinter.CTkFont(size=13, weight="bold"))
        self.file_label.grid(row=0, column=1)
        self.listb = tk.Listbox(self.image_screen, selectmode=tk.SINGLE, background="#ffe0d6", width=90, height=25)
        self.listb.grid(row=1, column=1, padx=15, pady=10, sticky="nsew")
        self.listb.drop_target_register(DND_FILES)
        self.listb.dnd_bind("<<Drop>>", lambda event: drop_inside_listbox(event, element=self.listb))

        # Bit Selection Slider
        bit_value = tk.IntVar()
        self.slider_label = customtkinter.CTkLabel(self.image_screen, text="Selected number of bits: 1")
        self.slider_label.grid(row=2, column=0, padx=15, pady=(10, 0), sticky="nsew")
        self.bit_slider = customtkinter.CTkSlider(self.image_screen, from_=1, to=8, number_of_steps=7,
                                                  command=image_slider_event, variable=bit_value)
        self.bit_slider.grid(row=3, column=0, padx=15, pady=0, sticky="ew")

        # Encode button
        self.encode_button = customtkinter.CTkButton(self.image_screen, text="Encode", command=self.image_encode_and_display)
        self.encode_button.grid(row=2, column=1, padx=(10, 15), pady=(10, 0), sticky="ew")

        # Label for displaying the input image
        self.input_image_label_text = customtkinter.CTkLabel(self.image_screen, text="")
        self.input_image_label_text.grid(row=4, column=0, padx=10, pady=(50, 0))

        self.input_image_label = customtkinter.CTkLabel(self.image_screen, text="", image=None)
        self.input_image_label.grid(row=5, column=0, padx=10, pady=10)

        # Label for displaying the output image
        self.output_image_label_text = customtkinter.CTkLabel(self.image_screen, text="")
        self.output_image_label_text.grid(row=4, column=1, padx=10, pady=(50, 0))
        self.output_image_label = customtkinter.CTkLabel(self.image_screen, text="", image=None)
        self.output_image_label.grid(row=5, column=1, padx=10, pady=10)

        # VIDEO SCREEN (INSERT YOUR UI ELEMENTS HERE) [ALVIS & DANIEL]
        self.video_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        # AUDIO SCREEN (INSERT YOUR UI ELEMENTS HERE) [SHIFA & JING YI]
        self.audio_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        # DECODE SCREEN (USED FOR ALL FORMATS OF DECODING)
        self.decode_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.decode_screen.grid_columnconfigure(1, weight=1)

        # Textbox
        self.decode_text_label = customtkinter.CTkLabel(self.decode_screen, text="Insert text file payload:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.decode_text_label.grid(row=0, column=0, columnspan=1)
        self.decode_tbox = tk.Text(self.decode_screen, width=70, height=25)
        self.decode_tbox.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        self.decode_tbox.drop_target_register(DND_FILES)
        self.decode_tbox.dnd_bind("<<Drop>>", lambda event: drop_inside_textbox(event, element=self.decode_tbox))

        # Listbox to drag and drop file path
        self.decode_file_label = customtkinter.CTkLabel(self.decode_screen, text="Insert cover image:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.decode_file_label.grid(row=0, column=1)
        self.decode_listb = tk.Listbox(self.decode_screen, selectmode=tk.SINGLE, background="#ffe0d6", width=90, height=25)
        self.decode_listb.grid(row=1, column=1, padx=15, pady=10, sticky="nsew")
        self.decode_listb.drop_target_register(DND_FILES)
        self.decode_listb.dnd_bind("<<Drop>>", lambda event: drop_inside_listbox(event, element=self.decode_listb))

        # Bit Selection Slider
        decode_bit_value = tk.IntVar()
        self.decode_slider_label = customtkinter.CTkLabel(self.decode_screen, text="Selected number of bits: 1")
        self.decode_slider_label.grid(row=2, column=0, padx=15, pady=(10, 0), sticky="nsew")
        self.decode_bit_slider = customtkinter.CTkSlider(self.decode_screen, from_=1, to=8, number_of_steps=7, command=decode_slider_event, variable=decode_bit_value)
        self.decode_bit_slider.grid(row=3, column=0, padx=15, pady=0, sticky="ew")

        # Decode Button
        self.decode_button = customtkinter.CTkButton(self.decode_screen, text="Decode")
        self.decode_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Select default frame - DASHBOARD
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # Change side nav button color on select
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.image_screen_button.configure(fg_color=("gray75", "gray25") if name == "image_screen" else "transparent")
        self.video_screen_button.configure(fg_color=("gray75", "gray25") if name == "video_screen" else "transparent")
        self.audio_screen_button.configure(fg_color=("gray75", "gray25") if name == "audio_screen" else "transparent")
        self.decode_screen_button.configure(fg_color=("gray75", "gray25") if name == "decode_screen" else "transparent")

        # Add and destroy frame
        if name == "dashboard":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
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


    def home_button_event(self):
        self.select_frame_by_name("dashboard")

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
