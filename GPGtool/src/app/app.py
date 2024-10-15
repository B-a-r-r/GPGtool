from GPGtool.src.graphics.graphics import Graphics
from GPGtool.src.crypto_engine.gpg import GPG_engine, Key_inputs

class App:
    
    (UI_MODES) = ("GUI", "CLI", "API")
    
    ui_mode: str
    engine: GPG_engine
    user_inputs: Key_inputs
    
    def __init__(self, ui_mode:str="GUI")->None:
        self.ui_mode = ui_mode.upper()
        assert ui_mode in self.UI_MODES, self.handle_error(1)
        
        if (ui_mode.upper() == "GUI"):
            self.graphics = Graphics()
            self.graphics.submit_button.configure(command=self.handle_submit)
            self.graphics.init_window()
            
        self.engine = GPG_engine()

    def handle_submit(event=None)->None:
        print("Submit button clicked.")
    
    def genrate_key_paire(self,**kwargs)->None:
        """
        Gather user inputs, then generate a key pair. If ui_mode is set to "GUI", 
        the user inputs are gathered from the GUI. Otherwise, the user is asked 
        to submit its inputs in the CLI. However, the inputs can also be provided
        in parameters, in case the user wants to use the API mode.
        """
        match self.ui_mode:
            case "CLI":
                self.user_inputs = Key_inputs(mode="CLI")
                
            case "API":
                self.user_inputs = Key_inputs(mode="API", **kwargs)
            
            case "GUI":
                pass
            
            case _:
                self.handle_error(1)

    def handle_error(self, error_code:int)->str:
        """
        Create an error according to a error number reported, then crash the app.
        Args:
            error (int): the number of the reported error.
        """
        match error_code:
            case 1:
                raise SystemExit("[GPGtool] Crash repport : unknown UI mode '" + self.ui_mode + "' selected.")
            case 0:
                raise SystemExit("[GPGtool] The application has been shot down; from app.py.")
            case _:
                raise SystemExit("[GPGtool] Crash report : unknown error reported; in app.py.")


if __name__ == "__main__":
    app = App(ui_mode="GUI")
