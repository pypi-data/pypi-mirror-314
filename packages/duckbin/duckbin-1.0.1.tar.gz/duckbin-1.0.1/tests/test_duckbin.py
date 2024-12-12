# tests/test_duckbin.py

import duckbin

link = duckbin.post("This is a test text!")
print(f"Text saved! Access it at: {link}")