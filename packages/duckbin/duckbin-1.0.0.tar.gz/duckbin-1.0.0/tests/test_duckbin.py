# tests/test_duckbin.py

from duckbin import *

link = save_text("This is a test text!")
print(f"Text saved! Access it at: {link}")