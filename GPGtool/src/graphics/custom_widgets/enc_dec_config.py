import customtkinter as ctk

class Enc_dec_configuration(ctk.CTkFrame):
    
    (MODES) = ("Encryption", "Decryption")
    
    master: ctk.CTkFrame
    selected_mode: str = None
    title_label: ctk.CTkLabel
    mode_menu: ctk.CTkOptionMenu
    text_label: ctk.CTkLabel
    text_entry: ctk.CTkTextbox
    email_label: ctk.CTkLabel
    email_entry: ctk.CTkEntry
    key_label: ctk.CTkLabel
    key_entry: ctk.CTkEntry
    submit_button: ctk.CTkButton
    result_label: ctk.CTkTextbox
    
    def __init__(self, **kwargs)->None:
        """
        Initialize and store all the graphics components for the simple encryption/decryption
        tool, and the bind events.
        """
        super().__init__(**kwargs)
        
        self.master = kwargs["master"]
        
        self.main_frame = ctk.CTkScrollableFrame(master=self.master)
        
        self.title_label = ctk.CTkLabel(master=self.main_frame, 
                                        text="Simple GPG Encryption/Decryption App", 
                                        font=("Inter", 22)
        )
        
        self.mode_menu = ctk.CTkOptionMenu(master=self.main_frame,
                                           variable=ctk.StringVar(value="Select mode"), 
                                           values=self.MODES,
                                           dynamic_resizing=True,
                                           command=self.mode_menu_clicked
        )
        
        self.text_entry = ctk.CTkTextbox(master=self.main_frame, 
                                         width=400, 
                                         height=300, 
                                         cursor="xterm", 
                                         text_color="grey")
        
        self.passphrase_entry = ctk.CTkEntry(master=self.main_frame, 
                                             width=350, 
                                             placeholder_text="Passphrase...")
        
        self.key_entry = ctk.CTkEntry(master=self.main_frame, width=350, placeholder_text="Key...")
        
        self.submit_button = ctk.CTkButton(master=self.main_frame, 
                                           text="Submit", 
                                           state="disabled",
                                           fg_color="grey"
        )

        self.result_label = ctk.CTkTextbox(master=self.main_frame, 
                                           width=400, 
                                           height=300, 
                                           state="disabled"
        )
        
        self.refreshing_triggers = {self.text_entry : [self.text_entry.bind("<Button>", self.text_entry_clicked),
                                                         self.text_entry.bind("<Key>", self.text_entry_clicked)],
                                      self.key_entry : [self.key_entry.bind("<Key>", self.key_entry_modified())]
        }
        
        (self.PERSISTENT_WIDGETS) = (self.main_frame, self.title_label, self.mode_menu)
    
        
    def display_configuration(self)->None:
        """
        Configures the window, color theme, and set the grid configuration on the main frame. Then displays the non variable components.
        """
        self.main_frame.grid(column=1,
                             row=0,
                             columnspan=self.master.grid_size()[0]-1, 
                             rowspan=self.master.grid_size()[1], 
                             padx=5, 
                             pady=5, 
                             sticky="nsew"
        )
        self.main_frame.grid_columnconfigure((0, 2), weight=1)
        self.main_frame.grid_rowconfigure((0, 10), weight=1)
        
        self.title_label.grid(columnspan=self.main_frame.grid_size()[0], row=0, pady=20)
        
        self.mode_menu.grid(columnspan=self.main_frame.grid_size()[0], row=1, pady=20)
        
        self.text_entry.insert("1.0", "Your text...")
    
    def refresh_layout(self, event=None)->None:
        """
        According to the selected mode, configure and displays the relative components.
        Args:
            event: A string given in special circumstances to adjust the display. Defaults to None.
        """
            
        assert self.selected_mode in [*self.MODES, None] , self.handle_error(1)
        
        match self.selected_mode:
            
            case "Encryption":
                if (not event == "text_entry_clicked"):
                    self.text_entry_placeholder(mode="encrypt")
                self.text_entry.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=2, pady=5, ipady=20)
                
                self.key_entry.configure(placeholder_text="Public key...")
                self.key_entry.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=3, pady=5)
                
                self.submit_button.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=4, pady=20)
                
                self.result_label.grid(columnspan=self.main_frame.grid_size()[0], row=5, pady=10)

            case "Decryption":                
                if (not event == "text_entry_clicked"):
                    self.text_entry_placeholder(mode="decrypt")
                self.text_entry.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=2, pady=5, ipady=20)
                
                self.key_entry.configure(placeholder_text="Prvate key...")
                self.key_entry.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=3, pady=5)
                
                self.passphrase_entry.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=4, pady=5)
                
                self.submit_button.grid(column=0, columnspan=self.main_frame.grid_size()[0], row=5, pady=20)
                
                self.result_label.grid(columnspan=self.main_frame.grid_size()[0], row=6, pady=10)
            
            case _:
                self.handle_error(1)
    
    def dispose_all(self)->None:
        """
        Clears the main frame of all the displayed components, exept the non variable ones.
        """
        
        for widget in self.main_frame.winfo_children():
            if widget not in self.PERSISTENT_WIDGETS:
                widget.grid_forget()
        
    def switch_mode(self, new_mode:str)->None:
        """
        Changes the selected mode, disposing all the components, then refreshs the display.
        """
        
        self.selected_mode = new_mode
        self.dispose_all()
        self.refresh_layout()
        
    def text_entry_clicked(self, event=None)->None:
        """
        Switchs the text entry from placeholder status to writting status.
        """
        
        if (self.text_entry.get("1.0", "end") in ["Your text...\n", 
                                                  "\n", 
                                                  "Text to encrypt...\n", 
                                                  "Text to decrypt...\n"]):
            self.text_entry.delete("1.0", "end")
            self.text_entry._text_color = "white"
            self.refresh_layout(event="text_entry_clicked")
    
    def key_entry_modified(self, event=None):
        """
        If the key entry is modified by the user, enables the submit button.
        """
        
        if (len(self.key_entry.get()) == 1):
            self.submit_button.configure(state="disabled", fg_color="grey")  
        else:
            self.submit_button.configure(state="normal", fg_color="#1F6AA5")
        
    def mode_menu_clicked(self, event=None)->None:
        """
        If the user select a action mode in the mode menu, switch to this mode.
        """
        
        if (self.mode_menu.get() not in [self.selected_mode, 'Select mode']):
            self.switch_mode(self.mode_menu.get())
    
    def text_entry_placeholder(self, mode:str)->None:
        """
        If the text entry isn't filled with user's data, displays its placeholder.
        Args:
            mode (str): 'encrypt' or 'decrypt', according to the selected mode.
        """
        
        if (self.text_entry.get("1.0", "end") in ["Your text...\n", "\n", "Text to encrypt...\n", "Text to decrypt...\n"]):
            self.text_entry.delete("1.0", "end")
            self.text_entry.insert("1.0", "Text to " + mode + "...")
            self.text_entry._text_color = "grey"
    
    def handle_error(self, error:int)->None:
        """
        Create an error according to a error number reported, then crash the app.
        Args:
            error (int): the number of the reported error.
        """
        
        match error:
            case  1:
                SystemExit("[GPGtool] Crash repport : unknown mode '"+self.selected_mode+"' selected.")
            case  0:
                SystemExit("[GPGtool] The application has been shotdown; from graphics.py.")
            case _:
                SystemExit("[GPGtool] Crash report : unknown error reported; in graphics.py.")
        self.master.quit()