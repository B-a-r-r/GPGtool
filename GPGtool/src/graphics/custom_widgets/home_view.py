import customtkinter as ctk

class Home_view(ctk.CTkFrame):
    
    master: ctk.CTkFrame
    main_frame: ctk.CTkFrame
    title_label: ctk.CTkLabel
    text_label: ctk.CTkLabel
    
    def __init__(self, **kwargs)->None:
        self.master = kwargs["master"]
        
        super().__init__(**kwargs)
        
        self.main_frame = ctk.CTkFrame(master=self.master
        )
        self.title_label = ctk.CTkLabel(master=self.main_frame, 
                                        text="GPG tool", 
                                        font=("Inter", 32, "bold")
        )
        self.text_label = ctk.CTkLabel(master=self.main_frame, 
                                       text="Welcome to GPG tool !", 
                                       font=("Inter", 16)
        )
    
    def display_configuration(self)->None:
        
        self.main_frame.grid(column=1,
                             row=0,
                             columnspan=self.master.grid_size()[0]-1, 
                             rowspan=self.master.grid_size()[1], 
                             padx=5, 
                             pady=5, 
                             sticky="nsew"
        )
        
        self.title_label.pack(anchor="center")
        self.text_label.pack(anchor="center")