import customtkinter as ctk

class Side_pannel(ctk.CTkFrame):
    
    master: ctk.CTkFrame
    main_frame: ctk.CTkFrame
    title_label: ctk.CTkLabel
    mode_menu: ctk.CTkOptionMenu
    color_theme_menu: ctk.CTkOptionMenu
    scale_menu: ctk.CTkOptionMenu
    copyright_label: ctk.CTkLabel
    
    def __init__(self, **kwargs)->None:
        """
        Initialize and store all the graphics components for the side menu, and the bind events.
        """
        super().__init__(**kwargs)
        
        self.master = kwargs["master"]
        
        self.main_frame = ctk.CTkFrame(master=self.master)
        
        self.title_label = ctk.CTkLabel(master=self.main_frame, 
                                        text="Welcome\naboard !", 
                                        font=("Inter", 22, "bold")
        )
        self.mode_menu = ctk.CTkOptionMenu(master=self.main_frame,
                                           variable=ctk.StringVar(value="Select mode"),
                                           values=["Encryption/Decryption", 
                                                   "Key generation", 
                                                   "Key management"],
                                           dynamic_resizing=True
        )
        self.color_theme_menu = ctk.CTkOptionMenu(master=self.main_frame,
                                                 values=["System", 
                                                        "Light", 
                                                        "Dark"],
                                                 dynamic_resizing=True
        )
        self.scale_menu = ctk.CTkOptionMenu(master=self.main_frame,
                                           values=["100%", 
                                                   "200%", 
                                                   "80%",
                                                   "50%"],
                                           dynamic_resizing=False
        )
        self.copyright_label = ctk.CTkLabel(master=self.main_frame,
                                           text="© 2024, GPGtool",
                                           font=("Inter", 10)
        )
    
    def display_configuration(self)->None:
        """
        Display the configuration of the side menu.
        """
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(5, weight=0)
        
        self.main_frame.grid(column=0, 
                             row=0, 
                             columnspan=1,
                             rowspan=self.master.grid_size()[1], 
                             padx=5,
                             pady=5,
                             sticky="nsew"
        )
        self.title_label.grid(column=0, row=0, pady=50, padx=5)
        self.mode_menu.grid(column=0, row=3, pady=20)
        self.color_theme_menu.grid(column=0, row=6, pady=20)
        self.scale_menu.grid(column=0, row=7, pady=20)
        self.copyright_label.grid(column=0, row=8, pady=20)
        
        self.refreshing_triggers = {self.mode_menu : [self.mode_menu.bind("<Button>", self.mode_menu_clicked)],
                                    self.color_theme_menu : [self.color_theme_menu.bind("<Button>", self.color_theme_menu_clicked)],
                                    self.scale_menu : [self.scale_menu.bind("<Button>", self.scale_menu_clicked)]
        }

    def mode_menu_clicked(self, event)->None:
        """
        Event handler for the mode menu.
        """
        print("Mode menu clicked")
    
    def color_theme_menu_clicked(self, event)->None:
        """
        Event handler for the color theme menu.
        """
        print("Color theme menu clicked")
    
    def scale_menu_clicked(self, event)->None:
        """
        Event handler for the scale menu.
        """
        print("Scale menu clicked")
    
    def refresh_layout(self, event=None)->None:
        """
        Refresh the layout of the side menu.
        """
        pass
        

if __name__ == "__main__":
    pass