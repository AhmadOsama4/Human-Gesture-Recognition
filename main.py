from mode_controller import ModeController
import os

def main():
    controller = ModeController(os.path.join(os.getcwd()), 'config.py')

if __name__ == '__main__':
    main()