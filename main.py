from config import log_setup
log_setup()

from app import App

if __name__ == "__main__": 
    App().run() 
    