from src.logging_setup import log_setup
log_setup()

from src.app import App

if __name__ == "__main__": 
    App().run() # точка входа