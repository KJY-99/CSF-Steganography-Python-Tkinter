import customtkinter
import os
from PIL import Image
import cv2, numpy as np
from tkinter import filedialog

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Define Title, Window size and Grid layout
        self.title("CSF Steganography Group --")
        self.geometry("1280x800")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))

        # Navigation icons
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Steganography", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.image_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Image",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.image_screen_button_event)
        self.image_screen_button.grid(row=2, column=0, sticky="ew")

        self.video_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Video",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.video_screen_button_event)
        self.video_screen_button.grid(row=3, column=0, sticky="ew")

        self.audio_screen_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Audio",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.audio_screen_button_event)
        self.audio_screen_button.grid(row=4, column=0, sticky="ew")

        # create dashboard screen
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame (image)
        self.image_screen = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Create a label to show the dropped file path
        self.dnd_label = customtkinter.CTkLabel(self.image_screen, text="Click below to select an image file",
                                                height=200, width=600, corner_radius=10, fg_color="gray80")
        self.dnd_label.grid(row=0, column=0, padx=20, pady=20)

        # Text field for secret message
        self.secret_message_label = customtkinter.CTkLabel(self.image_screen, text="Enter Secret Message:")
        self.secret_message_label.grid(row=1, column=0, padx=20, pady=10)
        self.secret_message_entry = customtkinter.CTkEntry(self.image_screen, width=400)
        self.secret_message_entry.grid(row=2, column=0, padx=20, pady=10)

        # Button to encode message
        self.encode_button = customtkinter.CTkButton(self.image_screen, text="Encode Message",
                                                     command=self.encode_message)
        self.encode_button.grid(row=3, column=0, padx=20, pady=10)

        # Labels to show images
        self.original_image_label = customtkinter.CTkLabel(self.image_screen, text="Original Image")
        self.original_image_label.grid(row=4, column=0, padx=20, pady=10)
        self.encoded_image_label = customtkinter.CTkLabel(self.image_screen, text="Encoded Image")
        self.encoded_image_label.grid(row=5, column=0, padx=20, pady=10)

        # create third frame (video)
        self.video_screen = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create fourth frame (audio)
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame (dashboard)
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.image_screen_button.configure(fg_color=("gray75", "gray25") if name == "image_screen" else "transparent")
        self.video_screen_button.configure(fg_color=("gray75", "gray25") if name == "video_screen" else "transparent")
        self.audio_screen_button.configure(fg_color=("gray75", "gray25") if name == "audio_screen" else "transparent")

        # show selected frame
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

    def encode_message(self):
        # Get the secret message from the entry field
        secret_message = self.secret_message_entry.get()

        # Check if the secret message is empty
        if not secret_message:
            print("Error: Secret message is empty.")
            return

        # Ask user to select an image file
        image_path = filedialog.askopenfilename()

        # Check if the user canceled the file dialog
        if not image_path:
            print("Error: No image selected.")
            return

        # Define the output directory and ask user for file name
        output_directory = filedialog.askdirectory()
        output_file_name = filedialog.asksaveasfilename(defaultextension=".png")

        # Check if the user canceled the save dialog
        if not output_file_name:
            print("Error: Save operation canceled.")
            return

        # Encode the secret message into the image
        try:
            encoded_image = self.encode(image_path, secret_message)
        except Exception as e:
            print("Error:", e)
            return

        # Save the encoded image to the specified location
        output_file_path = os.path.join(output_directory, output_file_name)
        cv2.imwrite(output_file_path, encoded_image)

        print("Encoded image saved successfully.")

    def to_bin(self, data):
        """Convert `data` to binary format as string"""
        if isinstance(data, str):
            return ''.join([format(ord(i), "08b") for i in data])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [format(i, "08b") for i in data]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")

    def encode(self, image_name, secret_data):
        # Read the image
        image = cv2.imread(image_name)

        # Make a copy of the image to preserve the original
        encoded_image = np.copy(image)

        # Calculate the maximum bytes to encode
        n_bytes = encoded_image.shape[0] * encoded_image.shape[1] * 3 // 8
        print("[*] Maximum bytes to encode:", n_bytes)

        # Add stopping criteria to the secret data
        secret_data += "====="

        # Check if the secret data fits within the image
        if len(secret_data) > n_bytes:
            raise ValueError("[!] Insufficient bytes, need a bigger image or less data.")

        print("[*] Encoding data...")

        # Convert secret data to binary
        binary_secret_data = self.to_bin(secret_data)

        # Get the size of data to hide
        data_len = len(binary_secret_data)

        # Index to keep track of the current data position
        data_index = 0

        # Iterate through each pixel in the image
        for row in range(encoded_image.shape[0]):
            for col in range(encoded_image.shape[1]):
                # Get the pixel value (RGB)
                r, g, b = encoded_image[row, col]

                # Convert RGB values to binary format
                r_bin, g_bin, b_bin = self.to_bin((r, g, b))

                # Modify the least significant bit only if there is still data to store
                if data_index < data_len:
                    r_bin = r_bin[:-1] + binary_secret_data[data_index]
                    data_index += 1
                if data_index < data_len:
                    g_bin = g_bin[:-1] + binary_secret_data[data_index]
                    data_index += 1
                if data_index < data_len:
                    b_bin = b_bin[:-1] + binary_secret_data[data_index]
                    data_index += 1

                # Convert modified binary values back to decimal
                r = int(r_bin, 2)
                g = int(g_bin, 2)
                b = int(b_bin, 2)

                # Update the pixel value in the encoded image
                encoded_image[row, col] = [r, g, b]

                # Break out of the loop if data is encoded
                if data_index >= data_len:
                    break

        return encoded_image

    def home_button_event(self):
        self.select_frame_by_name("dashboard")

    def image_screen_button_event(self):
        self.select_frame_by_name("image_screen")

    def video_screen_button_event(self):
        self.select_frame_by_name("video_screen")

    def audio_screen_button_event(self):
        self.select_frame_by_name("audio_screen")

    if __name__ == "__main__":
        app = App()
        app.mainloop()
