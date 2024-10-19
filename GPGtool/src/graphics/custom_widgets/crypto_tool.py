import customtkinter as ctk

class Crypto_tool(ctk.CTkFrame):
    
    (_MODES): tuple
    (_FORMAT): tuple
    (_PERSISTENT_WIDGETS): tuple
    
    _master: ctk.CTkFrame
    _selected_mode: str = None
    _main_frame: ctk.CTkScrollableFrame
    _mode_menu: ctk.CTkOptionMenu
    _refreshing_triggers: dict
    
    _input_frame: ctk.CTkFrame
    _entry_menu: ctk.CTkSegmentedButton
    _selected_entry_format: str = None
    _text_entry: ctk.CTkTextbox
    _key_entry: ctk.CTkEntry
    _submit_button: ctk.CTkButton
    
    _result_frame: ctk.CTkFrame
    _result_menu: ctk.CTkSegmentedButton
    _selected_result_format: str = None
    _text_result: ctk.CTkTextbox
    _warning_label: ctk.CTkLabel
    
    def __init__(self, **kwargs)->None:
        """
        Initialize and store all the graphics components for the simple encryption/decryption
        tool, and the bind events.
        """
        super().__init__(**kwargs)
        
        self._master = kwargs["master"]
        
        (self._MODES) = ("Encryption", "Decryption")
        (self._FORMAT) = ("Text", "File")
        
        self._selected_mode = self._MODES[0]
        
        self._main_frame = ctk.CTkFrame(master=self._master,
                                        width=self._master.cget("width")
                                                -self._master
                                                    .children["!ctkframe2"]
                                                    .cget("width")
        )
        print("main_frame width : ", self._main_frame.cget("width"), '\n')
        print("master width : ", self._master.cget("width"), '\n')    
        print("side_pannel_frame width : ", self._master.children["!ctkframe2"].cget("width"), '\n')
        print(self._master.children.__repr__())

        self._input_frame = ctk.CTkFrame(master=self._main_frame)
        
        self._result_frame = ctk.CTkFrame(master=self._main_frame)
        
        self._mode_menu = ctk.CTkOptionMenu(master=self._main_frame,
                                            variable=ctk.StringVar(value=self._MODES[0]),
                                            values=self._MODES,
                                            dynamic_resizing=True,
                                            command=self.mode_menu_changed
        )
        
        self._entry_menu = ctk.CTkSegmentedButton(master=self._main_frame,
                                                variable=ctk.StringVar(value=self._FORMAT[0]),
                                                values=self._FORMAT,
                                                command=self.entry_menu_changed
        )
        self._text_entry = ctk.CTkTextbox(master=self._main_frame, 
                                        width=400, 
                                        height=300, 
                                        cursor="xterm", 
                                        text_color="grey"
        )
        
        self.passphrase_entry = ctk.CTkEntry(master=self._main_frame, 
                                            width=350, 
                                            placeholder_text="Passphrase..."
        )
        
        self._key_entry = ctk.CTkEntry(master=self._main_frame, width=350, placeholder_text="Key...")
        
        self._submit_button = ctk.CTkButton(master=self._main_frame, 
                                            text="Submit", 
                                            state="disabled",
                                            fg_color="grey"
        )

        self._result_menu = ctk.CTkSegmentedButton(master=self._result_frame,
                                                    variable=ctk.StringVar(value=self._FORMAT[0]),
                                                    values=self._FORMAT,
                                                    command=self.result_menu_changed
        )                   
        self._text_result = ctk.CTkTextbox(master=self._result_frame, 
                                            width=400, 
                                            height=300, 
                                            state="disabled"
        )
        
        self._refreshing_triggers = {
            self._text_entry : [self._text_entry.bind("<Button>", self.text_entry_clicked),
                                self._text_entry.bind("<Key>", self.text_entry_clicked)],
            self._key_entry : [self._key_entry.bind("<Key>", self.key_entry_modified())]
        }
        
        (self._PERSISTENT_WIDGETS) = (self._main_frame, 
                                        self._mode_menu, 
                                        self._submit_button
        )
        
    def display_configuration(self)->None:
        """
        Configures the window, color theme, and set the grid configuration on the main frame. 
        Then displays the non variable components.
        """
        self._main_frame.grid_columnconfigure((0,2), weight=1)
        self._main_frame.grid_rowconfigure((0, 5), weight=1)
        self._main_frame.grid(column=1,
                             row=0,
                             columnspan=self._master.grid_size()[0], 
                             rowspan=self._master.grid_size()[1], 
                             padx=5, 
                             pady=5
        )
        
        # self._input_frame.grid_columnconfigure((0, 3), weight=1)
        # self._input_frame.grid_rowconfigure((0, 3), weight=1)
        # self._input_frame.grid(column=0, row=1, rowspan=3, padx=5, pady=5, sticky="nswe")
        
        # self._result_frame.grid_columnconfigure((0, 3), weight=1)
        # self._result_frame.grid_rowconfigure((0, 3), weight=1)
        # self._result_frame.grid(column=1, row=1, rowspan=3, padx=5, pady=5, sticky="nswe")
        
        self._mode_menu.grid(column=0, 
                            columnspan=self._main_frame.grid_size()[0], 
                            row=0, 
                            rowspan=1, 
                            pady=20
        )
        self._submit_button.grid(column=0, 
                                columnspan=self._main_frame.grid_size()[0], 
                                row=self._main_frame.grid_size()[1], 
                                rowspan=1, 
                                pady=20
        )
        
        self._text_entry.insert("1.0", "Your text...")
        
        self.refresh_layout()
    
    def refresh_layout(self, event=None)->None:
        """
        According to the selected mode, configure and displays the relative components.
        Args:
            event: A string given in special circumstances to adjust the display. Defaults to None.
        """
        assert self._selected_mode in [*self._MODES, None], self.handle_error(1)
        
        match self._selected_mode:
            
            case "Encryption":
                self._entry_menu.grid(column=0, row=1, padx=(20, 10), sticky="wn")
                
                if (not event == "text_entry_clicked"):
                    self.text_entry_placeholder(mode="encrypt")
                self._text_entry.grid(column=0,
                                        columnspan=self._main_frame.grid_size()[0],
                                        row=2, 
                                        rowspan=2, 
                                        ipady=20, 
                                        sticky="nsew"
                )
                
                self._key_entry.configure(placeholder_text="Public key..."
                )
                self._key_entry.grid(column=1, row=5, pady=5, sticky="w")
                
                # self._result_menu.grid(column=0, row=0, padx=(20, 10), sticky="wn")
                # self._text_result.grid(column=1, row=0, rowspan=2, sticky="e")

            case "Decryption":                
                if (not event == "text_entry_clicked"):
                    self.text_entry_placeholder(mode="decrypt")
                self._text_entry.grid(column=0, columnspan=self._main_frame.grid_size()[0], row=2, pady=5, ipady=20)
                
                self._key_entry.configure(placeholder_text="Prvate key...")
                self._key_entry.grid(column=0, columnspan=self._main_frame.grid_size()[0], row=3, pady=5)
                
                self.passphrase_entry.grid(column=0, columnspan=self._main_frame.grid_size()[0], row=4, pady=5)
                
                self._submit_button.grid(column=0, columnspan=self._main_frame.grid_size()[0], row=5, pady=20)
                
                self._text_result.grid(columnspan=self._main_frame.grid_size()[0], row=6, pady=10)
            
            case _:
                self.handle_error(1)
    
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
        self.refresh_layout()
        
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
            self.refresh_layout(event="text_entry_clicked")
    
    def key_entry_modified(self, event=None):
        """
        If the key entry is modified by the user, enables the submit button.
        """
        
        if (len(self._key_entry.get()) == 1):
            self._submit_button.configure(state="disabled", fg_color="grey")  
        else:
            self._submit_button.configure(state="normal", fg_color="#1F6AA5")
        
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
        if (self._entry_menu.get() not in [self._selected_entry_format, 'Select source']):
            self.switch_format(target=self._selected_entry_format, new_format=self._entry_menu.get())
            
    def result_menu_changed(self, event=None)->None:
        """
        If the user select a result mode in the result menu, switch to this mode.
        """
        if (self._result_menu.get() not in [self._selected_result_format, 'Select outcome']):
            self.switch_format(target=self._selected_result_format, new_format=self._result_menu.get())
    
    def switch_format(self, target:str, new_format:str)->None:
        """
        Changes the selected entry _FORMAT, disposing all the components, then refreshs the display.
        """
        target = new_format
        self.dispose_all(inner_command=True)
        self.refresh_layout()
    
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
    
    def handle_error(self, error:int)->None:
        """
        Create an error according to a error number reported, then crash the app.
        Args:
            error (int): the number of the reported error.
        """
        match error:
            case  1:
                SystemExit("[GPGtool] Crash repport : unknown mode '"+self._selected_mode+"' selected.")
            case  0:
                SystemExit("[GPGtool] The application has been shotdown; from graphics.py.")
            case _:
                SystemExit("[GPGtool] Crash report : unknown error reported; in graphics.py.")
        self._master.quit()
        