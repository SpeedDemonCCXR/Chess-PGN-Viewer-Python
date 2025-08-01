import io
import chess
import chess.pgn
import tkinter as tk
from tkinter import ttk

class NotationViewer:
    def __init__(self, pgn_text, pgn_window):
        self.pgn_window = pgn_window
        self.moves = list(chess.pgn.read_game(io.StringIO(pgn_text)).mainline_moves())
        board = chess.Board()

        master = pgn_window.window
        frame = ttk.Frame(master, padding=10)
        frame.grid(row=0, column=9, sticky="nsew")
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        self.tree = ttk.Treeview(
            frame,
            columns=("Move", "White", "Black"),
            show="headings",
            height=20
        )
        for col, w in [("Move", 50), ("White", 150), ("Black", 150)]:
            anchor = "center" if col == "Move" else "w"
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=anchor)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        num = 1
        for i in range(0, len(self.moves), 2):
            san_w = board.san(self.moves[i])
            board.push(self.moves[i])

            san_b = ""
            if i + 1 < len(self.moves):
                san_b = board.san(self.moves[i+1])
                board.push(self.moves[i+1])

            self.tree.insert("", "end", values=(num, san_w, san_b))
            num += 1

        self.tree.bind("<ButtonRelease-1>", self._on_click)

    def _on_click(self, event):
        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)
        if not row_id or col_id not in ("#2", "#3"):
            return

        move_num = int(self.tree.set(row_id, "Move"))
        half_move = (move_num - 1) * 2 + (1 if col_id == "#2" else 2)
        self.pgn_window.go_to(half_move)