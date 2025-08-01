import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import chess.pgn
import io
from Board import PGNWindow
from Notation_Viewer import NotationViewer
from Key_Bindings import bind_navigation_keys

root = tk.Tk()
root.title("Chess PGN Viewer")
style = Style(theme="cyborg")

ttk.Label(root, text="Enter PGN:", bootstyle="success").pack(padx=10, pady=5)
pgn_text_box = tk.Text(root, height=20, width=60)
pgn_text_box.pack(padx=10, pady=10)

validation_label = ttk.Label(root, text="", bootstyle="success")
validation_label.pack(padx=10, pady=5)
error_label = ttk.Label(root, text="", bootstyle="primary")
error_label.pack(padx=10, pady=5)

def validate_pgn(pgn):
    try:
        game = chess.pgn.read_game(io.StringIO(pgn))
        if game is None or not game.headers or not list(game.mainline_moves()):
            error_label.config(text="Invalid or empty PGN.")
            return False
        error_label.config(text="")
        return True
    except Exception as e:
        error_label.config(text=f"Error validating PGN: {e}")
        return False

def view_pgn():
    pgn = pgn_text_box.get("1.0", tk.END).strip()
    if validate_pgn(pgn):
        validation_label.config(text="PGN is valid", bootstyle="success")
        pgn_window = PGNWindow(pgn)
        NotationViewer(pgn, pgn_window)
        bind_navigation_keys(root, pgn_window)

    else:
        validation_label.config(text="PGN is invalid", bootstyle="danger")

ttk.Button(root, text="View PGN", bootstyle="primary",
           command=view_pgn).pack(padx=10, pady=10)

root.mainloop()
