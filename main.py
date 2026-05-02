import sys

from app import App

def main():
    app = App()
    app.run(sys.argv[1:])

if __name__ == "__main__":
    main()