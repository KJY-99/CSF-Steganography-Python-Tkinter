# AUDIO SCREEN (INSERT YOUR UI ELEMENTS HERE) [SHIFA & JING YI]
        # self.audio_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        # # DECODE SCREEN (USED FOR ALL FORMATS OF DECODING)
        # self.decode_screen = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        # self.decode_screen.grid_columnconfigure(0, weight=1)
        # self.decode_screen.grid_columnconfigure(1, weight=1)

        # # Listbox to drag and drop file path
        # self.decode_file_label = customtkinter.CTkLabel(self.decode_screen, text="Drop cover file here:", font=customtkinter.CTkFont(size=13, weight="bold"))
        # self.decode_file_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        # self.decode_listb = tk.Listbox(self.decode_screen, selectmode=tk.SINGLE, background="#ffe0d6", width=50, height=2, font=20)
        # self.decode_listb.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky='ew')
        # self.decode_listb.drop_target_register(DND_FILES)
        # self.decode_listb.dnd_bind("<<Drop>>", lambda event: drop_inside_decode_listbox(event, element=self.decode_listb))

        # # Dropdown box
        # self.decode_text_label = customtkinter.CTkLabel(self.decode_screen, text="Select file payload used in encoding process:", font=customtkinter.CTkFont(size=13, weight="bold"))
        # self.decode_text_label.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        # self.decode_combobox = customtkinter.CTkComboBox(self.decode_screen,state="readonly", values=['Text', 'Image', 'Audio'], width=300, height=25)
        # self.decode_combobox.set('Text')
        # self.decode_combobox.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        # self.selected_payload = self.decode_combobox.get()

        # # Bit Selection Slider
        # decode_bit_value = tk.IntVar()
        # self.decode_slider_label = customtkinter.CTkLabel(self.decode_screen, font=customtkinter.CTkFont(size=13, weight="bold"), text="Selected number of bits for decoding: 1")
        # self.decode_slider_label.grid(row=2, column=1, padx=15, pady=(10, 0), sticky="w")
        # self.decode_bit_slider = customtkinter.CTkSlider(self.decode_screen, from_=1, to=8, number_of_steps=7, command=decode_slider_event, variable=decode_bit_value)
        # self.decode_bit_slider.grid(row=3, column=1, padx=15, pady=5, sticky="ew")

        # # Decode Button
        # self.decode_button = customtkinter.CTkButton(self.decode_screen, font=customtkinter.CTkFont(size=13, weight="bold"), text="Decode", command=self.usedecodefunction)
        # self.decode_button.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

        # # Output screen
        # self.decode_output_label = customtkinter.CTkLabel(self.decode_screen, text="", image=None, wraplength=500)
        # self.decode_output_label.grid(row=6, column=0, columnspan=3, padx=10, pady=(50, 5), sticky="ew")
