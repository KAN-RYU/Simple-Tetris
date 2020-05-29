import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def numStrip(n):
    striped = []
    if n == 0:
        return [0]
    while n > 0:
        striped.append(n % 10)
        n //= 10
    
    return striped
