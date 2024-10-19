import customtkinter as ctk

class Crypto_tool(ctk.CTkFrame):
    
    (_ACTIVE_KEYS): tuple 
    (_MODES): tuple
    (_FORMAT): tuple
    (_PERSISTENT_WIDGETS): tuple
    
    _master: ctk.CTkFrame
    _selected_mode: str
    _main_frame: ctk.CTkScrollableFrame
    _mode_menu: ctk.CTkOptionMenu
    _refreshing_triggers: dict
    
    _format_buttons_frame: ctk.CTkFrame
    _entry_menu: ctk.CTkSegmentedButton
    _selected_entry_format: str
    _result_menu: ctk.CTkSegmentedButton
    _selected_result_format: str
    
    _io_frame: ctk.CTkFrame
    _text_entry: ctk.CTkTextbox
    _key_entry: ctk.CTkComboBox
    _passphrase_entry: ctk.CTkEntry
    _submit_button: ctk.CTkButton
    _text_result: ctk.CTkTextbox
    _path_entry: ctk.CTkComboBox
    _path_result: ctk.CTkComboBox
    _warning_entry_label: ctk.CTkLabel
    _warning_result_label: ctk.CTkLabel 
    
    def __init__(self, **kwargs)->None:
        """
        Initialize and store all the graphics components for the simple encryption/decryption
        tool, and the bind events.
        """
        super().__init__(**kwargs)
        
        self._master = kwargs["master"]
        (self._ACTIVE_KEYS) = None if "key_set" not in kwargs else kwargs["key_set"]
        (self._MODES) = ("Encryption", "Decryption")
        (self._FORMAT) = ("Text", "File")
        self._selected_mode = self._MODES[0]
        self._selected_entry_format = self._FORMAT[0]
        self._selected_result_format = self._FORMAT[0]
        
        self._main_frame = ctk.CTkFrame(master=self._master,
                                        bg_color='#2B2B2B', 
                                        fg_color='#2B2B2B'
        )

        self._io_frame = ctk.CTkFrame(master=self._main_frame)
        
        self._format_buttons_frame = ctk.CTkFrame(master=self._main_frame)
        
        self._mode_menu = ctk.CTkOptionMenu(master=self._main_frame,
                                            variable=ctk.StringVar(value=self._MODES[0]),
                                            values=self._MODES,
                                            command=self.mode_menu_changed,
                                            height=25,
                                            font=("Arial", 14),
        )
        
        self._entry_menu = ctk.CTkSegmentedButton(master=self._format_buttons_frame,
                                                    variable=ctk.StringVar(value=self._FORMAT[0]),
                                                    values=self._FORMAT,
                                                    command=self.entry_menu_changed,
                                                    corner_radius=10,
                                                    width=200,
                                                    height=30,
                                                    dynamic_resizing=True,
                                                    font=("Arial", 14)
        )
        
        self._text_entry = ctk.CTkTextbox(master=self._io_frame, 
                                            width=400, 
                                            height=300, 
                                            cursor="xterm", 
                                            text_color="grey"
        )
        
        self._passphrase_entry = ctk.CTkEntry(master=self._main_frame, 
                                                width=350, 
                                                placeholder_text="Enter relative passphrase...",
                                                placeholder_text_color="grey"
        )
        
        self._key_entry = ctk.CTkComboBox(master=self._main_frame, 
                                            width=350,
                                            variable=ctk.StringVar(value="Enter public key..."),
                                            values=self._ACTIVE_KEYS if self._ACTIVE_KEYS else ["No key available..."],
                                            border_width=1,
                                            command=self.key_entry_modified
        )

        self._submit_button = ctk.CTkButton(master=self._main_frame, 
                                            text="Submit", 
                                            state="disabled",
                                            fg_color="grey"
        )
        self._result_menu = ctk.CTkSegmentedButton(master=self._format_buttons_frame,
                                                    variable=ctk.StringVar(value=self._FORMAT[0]),
                                                    values=self._FORMAT,
                                                    command=self.result_menu_changed,
                                                    corner_radius=10,
                                                    width=200,
                                                    height=30,
                                                    dynamic_resizing=True,
                                                    font=("Arial", 14)
                                                    
        )      
                     
        self._text_result = ctk.CTkTextbox(master=self._io_frame, 
                                            width=400, 
                                            height=300,
                                            cursor="xterm",
                                            state="disabled"
        )
        
        self._arrow_label = ctk.CTkLabel(master=self._format_buttons_frame,
                                        text="→",
                                        font=("Inter", 32, "bold"),
        )
        
        self._path_entry = ctk.CTkComboBox(master=self._io_frame,
                                           variable=ctk.StringVar(value="Enter file path..."),
                                           values=["From computeur..."],
                                           command=self.path_entry_changed
        )
        
        self._path_result = ctk.CTkComboBox(master=self._io_frame,
                                            variable=ctk.StringVar(value="Enter file path..."),
                                            values=["From computeur..."],
                                            command=self.path_result_changed
        )
        
        self._warning_entry_label = ctk.CTkLabel(master=self._io_frame, 
                                                    text="\n⚠ Warning: \n  • if the file doesn't exists, the operation will fail" \
                                                         + "\n  • if the file already exists, the operation will fail.",
                                                    font=("Arial", 12),
                                                    text_color='grey',
                                                    justify="left"

        )
        
        self._warning_result_label = ctk.CTkLabel(master=self._io_frame,
                                                    text="\n⚠ Warning: \n  • if the file doesn't exists, it will be created" \
                                                         + "\n  • if the file already exists, the operation will fail.",
                                                    font=("Arial", 12),
                                                    text_color='grey',
                                                    justify="left"
                                                    
        )
        
        self._refreshing_triggers = {
            self._text_entry : [self._text_entry.bind("<Button>", self.text_entry_clicked),
                                self._text_entry.bind("<Key>", self.text_entry_clicked)],
            self._key_entry : [self._key_entry.bind("<FocusIn>", self.key_entry_clicked),
                                self._key_entry.bind("<Key>", self.key_entry_clicked)],
        }
        
        (self._PERSISTENT_WIDGETS) = (self._main_frame, 
                                        self._mode_menu, 
                                        self._submit_button
        )
        
    def display_configuration(self, event=None)->None:
        """
        Configures the window, color theme, and set the grid configuration on the main frame. 
        Then displays the non variable components.
        """
        assert self._selected_mode in [*self._MODES, None], self.handle_error(1)
        assert self._selected_entry_format in [*self._FORMAT, None], self.handle_error(2, info=self._selected_entry_format)
        assert self._selected_result_format in [*self._FORMAT, None], self.handle_error(2, info=self._selected_result_format)
        
        self._main_frame.grid_columnconfigure((0,2), weight=1)
        self._main_frame.grid_rowconfigure((0, 7), weight=1) if self._selected_mode == "Decryption" else self._main_frame.grid_rowconfigure((0, 6), weight=1)
        self._main_frame.grid(column=1,
                             row=0,
                             columnspan=self._master.grid_size()[0], 
                             rowspan=self._master.grid_size()[1], 
                             padx=5, 
                             pady=5,
                             sticky="nswe"
        )
        
        self._io_frame.grid_columnconfigure((0, 1), weight=1)
        self._io_frame.grid_rowconfigure((0, 1), weight=1)
        self._io_frame.grid(column=0,
                            columnspan=self._main_frame.grid_size()[0],
                            row=2, 
                            rowspan=2, 
                            padx=0, 
                            pady=0, 
                            sticky="nswe"
        )
        
        self._format_buttons_frame.grid_columnconfigure((0, 2), weight=1)
        self._format_buttons_frame.grid_rowconfigure(1, weight=1)
        self._format_buttons_frame.grid(column=0,
                                        row=1, 
                                        columnspan=self._main_frame.grid_size()[0], 
                                        pady=(5,15),
                                        padx=15,
                                        sticky="nswe"
        )
        
        self._mode_menu.grid(column=0,
                                columnspan=self._main_frame.grid_size()[0],
                                row=0, 
                                rowspan=1,
                                pady=(5,5) if self._selected_mode == "Decryption" else (10,15),
                                padx=(15,0),
                                sticky="w"
        )
        
        self._submit_button.grid(column=0,
                                    columnspan=self._main_frame.grid_size()[0],
                                    row=self._main_frame.grid_size()[1],
                                    pady=(8,16),
                                    sticky="n"
        )
        
        self._entry_menu.grid(column=0, row=0, padx=(0,15), pady=(5,0), sticky="en")
        self._arrow_label.grid(column=1, row=0, sticky="n", pady=0, padx=0, ipadx=0, ipady=0)
        self._result_menu.grid(column=2, row=0, padx=(15,0), pady=(5,0), sticky="wn")
        
        if (self._selected_entry_format == "File"):
            self._text_entry.grid_forget()
            self._path_entry.grid(column=0,
                                    row=0, 
                                    padx=(15, 15),
                                    pady=(10,20),
                                    sticky="nwe"
            )
            
            self._warning_entry_label.grid(column=0,
                                            row= 0 if self._selected_result_format == "Text" else 1, 
                                            padx=(27, 15),
                                            pady=(5,self._text_entry.cget('height')//2 - self._warning_entry_label.cget('height') + 5),
                                            sticky="w" if self._selected_result_format == "Text" else "nw"
            )
        else:
            self._path_entry.grid_forget()
            self._warning_entry_label.grid_forget()
            if (not event == "text_entry_clicked"):
                self.text_entry_placeholder(mode="encrypt")
            self._text_entry.grid(column=0,
                                    row=0, 
                                    rowspan=self._io_frame.grid_size()[1]-1, 
                                    ipady=20,
                                    padx=(15, 5),
                                    pady=(5,0),
                                    sticky="nswe"
            )
        
        if (self._selected_result_format == "File"):
            self._text_result.grid_forget()
            self._path_result.grid(column=1,
                                    row=0, 
                                    padx=(15, 15),
                                    pady=(10,20),
                                    sticky="nwe"
            )
            
            self._warning_result_label.grid(column=1,
                                            row=0 if self._selected_entry_format == "Text" else 1, 
                                            padx=(27, 15),
                                            pady=(5,self._text_result.cget('height')//2 - self._warning_result_label.cget('height')),
                                            sticky="w" if self._selected_entry_format == "Text" else "nw"
            )
        else:
            self._path_result.grid_forget()
            self._warning_result_label.grid_forget()
            self._text_result.grid(column=1,
                                    row=0, 
                                    rowspan=self._io_frame.grid_size()[1]-1, 
                                    ipady=20,
                                    padx=(5,15),
                                    pady=(5,0),
                                    sticky="nswe"
            )
        
        self._key_entry.set("Enter private key...") if self._selected_mode == "Decryption" else self._key_entry.set("Enter public key...")
        self._key_entry.configure(text_color="grey" if self._key_entry.get() in ["Enter public key...", "Enter private key..."] else "#DCE4EE")
        self._key_entry.grid(column=0,
                            columnspan=self._main_frame.grid_size()[0],
                            row=5, 
                            pady=(10,5),
                            sticky="s",
                            
        )
            
        self._passphrase_entry.grid(column=0,
                                    columnspan=self._main_frame.grid_size()[0],
                                    row=6, 
                                    pady=(5,10),
                                    sticky="n"
        ) if self._selected_mode == "Decryption" else self._passphrase_entry.grid_forget()
    
    def dispose_all(self, inner_command:bool=False)->None:
        """
        Clears the main frame of all the displayed components, exept the non variable ones.
        """
        if (inner_command):
            for widget in self._main_frame.winfo_children():
                if (widget not in self._PERSISTENT_WIDGETS):
                    widget.grid_forget()
        else:
            self._main_frame.destroy()
        
    def switch_mode(self, new_mode:str)->None:
        """
        Changes the selected mode, disposing all the components, then refreshs the display.
        """
        self._selected_mode = new_mode
        self.dispose_all(inner_command=True)
        self.display_configuration()
        
    def text_entry_clicked(self, event=None)->None:
        """
        Switchs the text entry from placeholder status to writting status.
        """
        
        if (self._text_entry.get("1.0", "end") in ["Your text...\n", 
                                                  "\n", 
                                                  "Text to encrypt...\n", 
                                                  "Text to decrypt...\n"]):
            self._text_entry.delete("1.0", "end")
            self._text_entry._text_color = "white"
            self.display_configuration(event="text_entry_clicked")
    
    def key_entry_modified(self, event=None):
        """
        If the key entry is modified by the user, enables the submit button.
        """
        if (self._key_entry.get() == "No key available..."):
            self._key_entry.configure(state="readonly")
            self._key_entry.set("Enter public key...") if self._selected_mode == "Encryption" \
            else self._key_entry.set("Enter private key...")

        if (self._key_entry.get() == "Enter public key..." or self._key_entry.get() == "Enter private key..."):
            self._key_entry.configure(text_color="grey")
            self._key_entry.configure(state="normal")
        else:
            self._key_entry.configure(text_color="#DCE4EE")
            self._key_entry.set(self._key_entry.get().removeprefix("Enter public key...").strip())
            
    def path_entry_changed(self, event=None):
        pass
    
    def path_result_changed(self, event=None):
        pass
            
    def key_entry_clicked(self, event=None):
        """
        If the key entry isn't filled with user's data, displays its placeholder.
        """
        if (self._key_entry.get() == "Enter public key..." or self._key_entry.get() == "Enter private key..."):
            self._key_entry.set("")
            self._key_entry.configure(text_color="#DCE4EE")
        
    def mode_menu_changed(self, event=None)->None:
        """
        If the user select a action mode in the mode menu, switch to this mode.
        """
        if (self._mode_menu.get() not in [self._selected_mode, 'Select mode']):
            self.switch_mode(self._mode_menu.get())
    
    def entry_menu_changed(self, event=None)->None:
        """
        If the user select a entry mode in the entry menu, switch to this mode.
        """
        if (self._entry_menu.get() != self._selected_entry_format):
            self._selected_entry_format = self._entry_menu.get()
            self.display_configuration()
            
    def result_menu_changed(self, event=None)->None:
        """
        If the user select a result mode in the result menu, switch to this mode.
        """
        if (self._result_menu.get() != self._selected_result_format):
            self._selected_result_format = self._result_menu.get()
            self.display_configuration()
    
    def text_entry_placeholder(self, mode:str)->None:
        """
        If the text entry isn't filled with user's data, displays its placeholder.
        Args:
            mode (str): 'encrypt' or 'decrypt', according to the selected mode.
        """
        if (self._text_entry.get("1.0", "end") in ["Your text...\n", "\n", "Text to encrypt...\n", "Text to decrypt...\n"]):
            self._text_entry.delete("1.0", "end")
            self._text_entry.insert("1.0", "Text to " + mode + "...")
            self._text_entry._text_color = "grey"
    
    def handle_error(self, error:int, info:str="")->None:
        """
        Create an error according to a error number reported, then crash the app.
        Args:
            error (int): the number of the reported error.
        """
        match error:
            case  2:
                SystemExit("[GPGtool] Crash repport : unknown format '"+info+"' selected.")
            case  1:
                SystemExit("[GPGtool] Crash repport : unknown mode '"+info+"' selected.")
            case  0:
                SystemExit("[GPGtool] The application has been shotdown; from graphics.py.")
            case _:
                SystemExit("[GPGtool] Crash report : unknown error reported; in graphics.py.")
        self._master.quit()
        