import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import chess.pgn
import io 
from Board import PGNWindow

root = tk.Tk()
root.title("Chess PGN Viewer")

style = Style(theme="cyborg")

pgn_label = ttk.Label(root, text="Enter PGN:", bootstyle="success")
pgn_label.pack(padx=10, pady=5)

pgn_text_box = tk.Text(root, height=20, width=60)
pgn_text_box.pack(padx=10, pady=10)

validation_label = ttk.Label(root, text="", bootstyle="success")
validation_label.pack(padx=10, pady=5)

error_label = ttk.Label(root, text="", bootstyle="primary")
error_label.pack(padx=10, pady=5)

def validate_pgn(pgn):
    try:
        pgn_file = io.StringIO(pgn)
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            error_label.config(text="No game found in PGN.")
            return False
        if not game.headers or not list(game.mainline_moves()):
            error_label.config(text="PGN missing headers or moves.")
            return False
        error_label.config(text="")
        return True
    except Exception as e:
        error_label.config(text="Error validating PGN: " + str(e))
        return False

def view_pgn():
    pgn = pgn_text_box.get("1.0", tk.END).strip()
    if validate_pgn(pgn):
        validation_label.config(text="PGN is valid", bootstyle="success")
        pgn_window = PGNWindow(pgn)
        pgn_window.show()
    else:
        validation_label.config(text="PGN is invalid", bootstyle="danger")
        # Do NOT open PGNWindow if invalid

view_pgn_button = ttk.Button(root, text="View PGN", bootstyle="primary", command=view_pgn)
view_pgn_button.pack(padx=10, pady=10)

root.mainloop()