import customtkinter
import tkinter as tk
import os
from TkinterDnD2 import DND_FILES, TkinterDnD
from PIL import Image

# Allow for TkDnD to utilise CTK
class App(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()

        # Define TkDnD ver.
        self.TkdndVersion = TkinterDnD._require(self)

        # Drag and Drop Method - Listbox: Get filepath to listbox (IMPT: Omit spaces in filename)
        def drop_inside_listbox(event):
            self.listb.insert("end", event.data)
            
        # Drag and Drop Method - Textbox: Strip text from file (IMPT: Omit spaces in filename)
        def drop_inside_textbox(event):
            self.tbox.delete("1.0", "end")
            if event.data.endswith(".txt"):
                with open(event.data, "r") as file:
                    for line in file:
                        line = line.strip()
                        self.tbox.insert("end", f"{line}\n")

        # Define Title, Window size and Grid layout
        self.title("CSF Steganography Group --")
        self.geometry("1280x800")
        # Configure Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load example images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))

        # Navigation icons
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # Side Navigation (ALL SCREENS)
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
        self.image_screen = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.image_screen.grid_columnconfigure(0, weight=1)

        self.listb = tk.Listbox(self.image_screen, selectmode=tk.SINGLE, background="#ffe0d6")
        self.listb.grid(row=0, column=0, padx=20, pady=10)
        self.listb.drop_target_register(DND_FILES)
        self.listb.dnd_bind("<<Drop>>", drop_inside_listbox)

        self.tbox = tk.Text(self.image_screen)
        self.tbox.grid(row=1, column=0, padx=20, pady=10)
        self.tbox.drop_target_register(DND_FILES)
        self.tbox.dnd_bind("<<Drop>>", drop_inside_textbox)

        # VIDEO SCREEN (INSERT YOUR UI ELEMENTS HERE) [ALVIS & DANIEL]
        self.video_screen = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # AUDIO SCREEN (INSERT YOUR UI ELEMENTS HERE) [SHIFA & JING YI]
        self.audio_screen = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Select default frame - DASHBOARD
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # Change side nav button color on select
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.image_screen_button.configure(fg_color=("gray75", "gray25") if name == "image_screen" else "transparent")
        self.video_screen_button.configure(fg_color=("gray75", "gray25") if name == "video_screen" else "transparent")
        self.audio_screen_button.configure(fg_color=("gray75", "gray25") if name == "audio_screen" else "transparent")

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

    def home_button_event(self):
        self.select_frame_by_name("dashboard")

    def image_screen_button_event(self):
        self.select_frame_by_name("image_screen")

    def video_screen_button_event(self):
        self.select_frame_by_name("video_screen")

    def audio_screen_button_event(self):
        self.select_frame_by_name("audio_screen")

# Run Application
if __name__ == "__main__":
    app = App()
    app.mainloop()
