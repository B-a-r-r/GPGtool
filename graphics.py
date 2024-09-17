from tkinter import Tk, StringVar
import customtkinter as ctk

class Graphics:
    
    MODES = ["Encryption", "Decryption"]
    ERRORS = [0,1]
    
    _window: Tk
    selected_mode: str = None
    appearence_mode: StringVar
    color_theme: StringVar
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
        
    def mainloop(self)->None:
        self._window.mainloop()

    def init_window(self)->None:
        self._window = Tk()
        self._window.minsize(600, 600)
        self._window.maxsize(600, self._window.winfo_screenheight())
        self._window.title("GPG tool")
        self._window.iconbitmap("encrypt.ico")
        self._window.configure(bg="#2B2B2B")
        
        self.appearence_mode = StringVar(value="dark")
        self.color_theme = StringVar(value="blue")
        
        ctk.set_appearance_mode(self.appearence_mode.get())
        ctk.set_default_color_theme(self.color_theme.get())
        
        self.main_frame = ctk.CTkScrollableFrame(master=self._window)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure((0, 2), weight=1)
        self.main_frame.grid_rowconfigure((0, 10), weight=1)
        
        self.title_label = ctk.CTkLabel(master=self.main_frame, 
                                        text="Simple GPG Encryption/Decryption App", 
                                        font=("Inter", 22)
        )
        self.title_label.grid(columnspan=self.main_frame.grid_size()[0], row=0, pady=35)
        
        self.mode_menu = ctk.CTkOptionMenu(master=self.main_frame,
                                           variable=StringVar(value="Select mode"), 
                                           values=self.MODES,
                                           dynamic_resizing=True,
                                           command=self.refresh_layout
        )
        self.mode_menu.grid(columnspan=self.main_frame.grid_size()[0], row=1, pady=10)

        self.text_label = ctk.CTkLabel(master=self.main_frame, text="Text:")
        
        self.text_entry = ctk.CTkTextbox(master=self.main_frame, width=400, height=300)

        self.email_label = ctk.CTkLabel(master=self.main_frame, text="Email:")
        self.email_entry = ctk.CTkEntry(master=self.main_frame, width=300)

        self.key_label = ctk.CTkLabel(master=self.main_frame, text="Key:")
        
        self.key_entry = ctk.CTkEntry(master=self.main_frame, width=300)
        
        self.submit_button = ctk.CTkButton(master=self.main_frame, text="Submit", command=self.handle_submit)

        self.result_label = ctk.CTkTextbox(master=self.main_frame, width=400, height=300, state="disabled")
        
        self.mainloop()
        self.handle_error(0)
    
    def refresh_layout(self, event=None)->None:
        if (self.mode_menu.get() not in [self.selected_mode, self.mode_menu._variable]):
            self.switch_mode(self.mode_menu.get())
        
        if (self.text_entry. != "" and self.key_entry.get(0) != ""):
            self.submit_button.configure(state="normal")
            
        assert StringVar(value=self.selected_mode).get() in self.MODES, self.handle_error(1)

        match self.selected_mode:
            case "Encryption":
                self.text_label.configure(text="The text to encrypt :")
                self.text_label.grid(column=0, row=1, sticky="e", pady=0)
                self.text_entry.grid(column=1, row=2, pady=5)
                
                self.key_label.configure(text="The public key :")
                self.key_label.grid(column=0, row=3, sticky="e", pady=5)
                self.key_entry.grid(column=1, row=3, pady=5)
                
                self.submit_button.configure(state="normal")

            case "Decryption":
                self.text_label.configure(text="The text to decrypt :")
                self.text_label.grid(column=0, row=2, sticky="e", pady=5)
                self.text_entry.grid(column=1, row=2, pady=5)
                
                self.key_label.configure(text="The private key :")
                self.key_label.grid(column=0, row=4, sticky="e", pady=5)
                self.key_entry.grid(column=1, row=4, pady=5)
                
                self.submit_button.configure(state="normal")
            
            case "":
                self.email_label.grid_forget()
                self.email_entry.grid_forget()
                self.text_entry.grid_forget()
                self.key_entry.grid_forget()
                self.text_label.grid_forget()
                self.key_label.grid_forget()
                self.submit_button.configure(state="disabled")
        
    def switch_mode(self, new_mode:str)->None:
        self.selected_mode = new_mode
        self.result_label.grid_forget()

    def handle_submit(self, event=None)->None:
        self.result_label.grid(column=0, row=5, columnspan=2, pady=10)
    
    def handle_error(self, error:int)->None:
        assert error in self.ERRORS, SystemError("[GPGtool] Crash report : unknown error '"+str(error)+"' reported.")
        match error:
            case  1:
                SystemError("[GPGtool] Crash report : unknown mode '"+self.selected_mode+"' selected.")
            case  0:
                SystemError("[GPGtool] The application has been shotdown.")
        self._window.destroy()
        self._window.quit()

if __name__ == "__main__":
    test = Graphics()
    test.init_window()
            