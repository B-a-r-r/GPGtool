from graphics import Graphics
from gpg import GPG_engine, Key_inputs

class App:
    
    (UI_MODES) = ("GUI", "CLI", "API")
    
    ui_mode: str
    engine: GPG_engine
    user_inputs: Key_inputs
    
    def __init__(self, ui_mode:str="GUI")->None:
        self.ui_mode = ui_mode.title()
        assert ui_mode in self.UI_MODES, self.handle_error(1)
        
        if (ui_mode.title() == "GUI"):
            self.graphics = Graphics()
            self.graphics.submit_button.configure(command=self.handle_submit)
            self.graphics.init_window()
            
        self.engine = GPG_engine()
        self.user_inputs = Key_inputs()

    def handle_submit(event=None)->None:
        print("Submit button clicked.")
    
    def genrate_key_paire(self, 
                          key_email:str=None, 
                          key_passphrase:str=None,
                          key_type:str=None,
                          key_length:int=None,
                          key_name:str=None
                          )->None:
        """
        Gather user inputs, then generate a key pair. If ui_mode is set to "GUI", 
        the user inputs are gathered from the GUI. Otherwise, the user is asked 
        to submit its inputs in the CLI. However, the inputs can also be provided
        in parameters, in case the user wants to use the API mode.
        Args:
            key_email (str, optional): Defaults to None.
            key_passphrase (str, optional): Defaults to None.
            key_type (str, optional): Defaults to None.
            key_length (int, optional): Defaults to None.
            key_name (str, optional): Defaults to None.
        """
        
        match self.ui_mode:
            case "CLI":
                self.user_inputs = Key_inputs()
                
            case "API":
                self.user_inputs = Key_inputs(
                    key_email, 
                    key_passphrase, 
                    key_name, 
                    key_type, 
                    key_length
                )
            
            case "GUI":
                pass
            
            case _:
                self.handle_error(0)

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
    app = App()
