import customtkinter as ctk

from custom_widgets.crypto_tool import Crypto_tool
from custom_widgets.home_view import Home_view
from custom_widgets.key_manager import Key_manager

class Index:
    
    (MODES) = ("Encryption/Decryption", "Key manager")
    
    _window: ctk.CTk
    _appearence_mode: ctk.StringVar
    _color_theme: ctk.StringVar
    
    main_frame: ctk.CTkFrame
    _active_config: ctk.CTkFrame
    
    _side_pannel_frame: ctk.CTkFrame
    _side_pannel_title_label: ctk.CTkLabel
    _side_pannel_mode_menu: ctk.CTkOptionMenu
    _side_pannel_bottom_frame: ctk.CTkFrame
    _side_pannel_appearance_menu: ctk.CTkOptionMenu
    _side_pannel_scale_menu: ctk.CTkOptionMenu
    _side_pannel_copyright_label: ctk.CTkLabel
    _side_pannel_triggers: dict
    
    def __init__(self)->None:
        """
        Initialize the main window of the app.
        """
        self._window = ctk.CTk()
        
        self._appearence_mode = ctk.StringVar(value="dark")
        self._color_theme = ctk.StringVar(value="blue")
        
        self.main_frame = ctk.CTkFrame(master=self._window)
        
        self._active_config = Home_view(master=self.main_frame)
        
        self._side_pannel_frame = ctk.CTkFrame(master=self.main_frame)
        
        self._side_pannel_title_label = ctk.CTkLabel(master=self._side_pannel_frame, 
                                            text="Welcome aboard !", 
                                            font=("Inter", 22, "bold")
        )
        self.side_pannel_mode_menu = ctk.CTkOptionMenu(master=self._side_pannel_frame,
                                        variable=ctk.StringVar(value="Select mode"),
                                        values=self.MODES,
                                        dynamic_resizing=True,
                                        command=self.switch_mode
        )
        
        self._side_pannel_bottom_frame = ctk.CTkFrame(master=self._side_pannel_frame,
                                            bg_color=self.main_frame.cget("bg_color")
        )
        self._side_pannel_appearance_menu = ctk.CTkComboBox(
                                                master=self._side_pannel_bottom_frame,
                                                values=["System", 
                                                        "Light", 
                                                        "Dark"],
                                                state="readonly",
                                                variable=ctk.StringVar(value="System"),
                                                command=self.switch_appearance
        )
        self._side_pannel_scale_menu = ctk.CTkComboBox(
                                        master=self._side_pannel_bottom_frame,
                                        values=["100%", 
                                                "200%", 
                                                "80%",
                                                "50%"],
                                        state="readonly",
                                        variable=ctk.StringVar(value="100%"),
                                        command=self.update_scaling
        )
        self._side_pannel_copyright_label = ctk.CTkLabel(
                                                master=self._side_pannel_bottom_frame,
                                                text="© 2024, GPGtool",
                                                font=("Inter", 10)
        )
    
    def init_window(self)->None:
        """
        Configures the window, color theme, and set the grid configuration on the main frame. Then displays the non variable components.
        """
        self._window.minsize(1000,600)
        self._window.maxsize(self._window.winfo_screenwidth(), self._window.winfo_screenheight())
        self._window.geometry("1000x600")
        self._window.title("GPG tool")
        self._window.configure(bg="#2B2B2B")
        
        self.set_appereance_mode()
        
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.pack(fill="both", expand=True)
    
        self.display_side_pannel()
        self._active_config.display_configuration()
        
        self._window.mainloop()
    
    def display_side_pannel(self)->None:
        """
        Display the configuration of the side menu.
        """
        self._side_pannel_frame.grid_columnconfigure(0, weight=0)
        self._side_pannel_frame.grid_rowconfigure(3, weight=0)
        
        self._side_pannel_frame.grid(column=0,
                                    row=0,
                                    columnspan=1,
                                    rowspan=self.main_frame.grid_size()[1],
                                    padx=5,
                                    pady=5,
                                    sticky="nsew"
        )
        self._side_pannel_title_label.grid(column=0,
                                          row=0, 
                                          pady=25, 
                                          padx=25,
        )
        self.side_pannel_mode_menu.grid(column=0, 
                                        row=1,
                                        pady=20         
        )
        
        self._side_pannel_bottom_frame.grid_columnconfigure(0, weight=1)
        self._side_pannel_bottom_frame.grid_rowconfigure(2, weight=1)
        self._side_pannel_bottom_frame.grid(column=0, 
                                           row=self._side_pannel_frame.grid_size()[1], 
                                           columnspan=1,
                                           rowspan=self._side_pannel_frame.grid_size()[1],
                                           pady=20,
                                           sticky="nsew"
        )
        self._side_pannel_appearance_menu.grid(column=0, 
                                                row=0, 
                                                pady=20
        )
        self._side_pannel_scale_menu.grid(column=0, 
                                            row=1, 
                                            pady=20
        )
        self._side_pannel_copyright_label.grid(column=0, 
                                                row=2,  
                                                pady=20
        )
        
        self._side_pannel_triggers = {
            
        }
        
    def set_appereance_mode(self)->None:
        """
        Set the color theme and the appereance mode of the app,
        according to the corresponding attributes.
        """
        ctk.set_appearance_mode(self._appearence_mode.get())
        ctk.set_default_color_theme(self._color_theme.get())
    
    def switch_mode(self, event)->None:
        """
        Switch the active configuration of the app, according to the selected
        value in the mode menu.
        """
        match self.side_pannel_mode_menu.get():
            case "Select mode":
                if self._active_config is not Home_view:
                    self._active_config.dispose_all()
                    self._active_config.destroy()
                    self._active_config = Home_view(master=self.main_frame)
                    self._active_config.display_configuration()
            case "Encryption/Decryption":
                if self._active_config is not Crypto_tool:
                    self._active_config.dispose_all()
                    self._active_config.destroy()
                    self._active_config = Crypto_tool(master=self.main_frame)
                    self._active_config.display_configuration()
            case "Key manager":
                if self._active_config is not Key_manager:
                    self._active_config.dispose_all()
            case _:
                self.handle_error(error=1, info=self._side_pannel_mode_menu.get())
    
    def switch_appearance(self, event)->None:
        """
        Update the appearance mode of the app, according to the selected 
        value in the appearance menu.
        """
        self._appearence_mode.set(self._side_pannel_appearance_menu.get().lower())
        self.set_appereance_mode()
    
    def update_scaling(self, event)->None:
        """
        Update the scaling of the app, according to the selected 
        value in the scale menu.
        """
        new_scaling_float = int(self._side_pannel_scale_menu.get().replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def handle_error(self, error:int, info:str="")->None:
        """
        Create an error according to a error number reported, then crash the app.
        Args:
            error (int): the number of the reported error.
            info (str): complementary information about the error.
        """
        match error:
            case  1:
                SystemExit("[GPGtool] Crash repport : unknown mode '"+info+"' selected.")
            case  0:
                SystemExit("[GPGtool] The application has been shotdown; from graphics.py.")
            case _:
                SystemExit("[GPGtool] Crash report : unknown error reported; in graphics.py.")
        self._window.quit()
    
if __name__ == "__main__":
    test = Index()
    test.init_window()
            