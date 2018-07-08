from mode_controller import ModeController
import os

def main():
    path = os.path.join(os.getcwd(), 'config.py')
    controller = ModeController()

if __name__ == '__main__':
    main()