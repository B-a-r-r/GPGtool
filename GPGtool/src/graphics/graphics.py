import customtkinter as ctk
from custom_widgets.side_pannel import Side_pannel
from custom_widgets.using_engine import Using_engine
from custom_widgets.home_view import Home_view

class Index:
    
    _window: ctk.CTk
    appearence_mode: ctk.StringVar
    color_theme: ctk.StringVar
    side_menu: Side_pannel    
    
    def __init__(self)->None:
        """
        Initialize the main window of the app.
        """
        self._window = ctk.CTk()
        
        self.appearence_mode = ctk.StringVar(value="dark")
        self.color_theme = ctk.StringVar(value="blue")
        
        self.main_frame = ctk.CTkFrame(master=self._window)
        
        self.side_menu = Side_pannel(master=self.main_frame)
        
        self.active_config = Home_view(master=self.main_frame)
    
    def init_window(self)->None:
        """
        Configures the window, color theme, and set the grid configuration on the main frame. Then displays the non variable components.
        """
        self._window.minsize(1000,600)
        self._window.maxsize(self._window.winfo_screenwidth(), self._window.winfo_screenheight())
        self._window.geometry("1000x600")
        self._window.title("GPG tool")
        self._window.configure(bg="#2B2B2B")
        
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.pack(fill="both", expand=True)
        
        ctk.set_appearance_mode(self.appearence_mode.get())
        ctk.set_default_color_theme(self.color_theme.get())
    
        self.side_menu.display_configuration()  
        self.active_config.display_configuration()
        
        self._window.mainloop()

    
if __name__ == "__main__":
    test = Index()
    test.init_window()
            