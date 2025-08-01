import tkinter as tk
import chess
import chess.pgn
import io

class PGNWindow:
    def __init__(self, pgn):
        self.pgn = pgn
        pgn_file = io.StringIO(pgn)
        self.game = chess.pgn.read_game(pgn_file)
        self.moves = list(self.game.mainline_moves())

        # initial board and FEN
        self.board = self.game.board()
        self.initial_fen = self.board.fen()
        self.current_index = 0

        # create window
        self.window = tk.Toplevel()
        self.window.title("Chess PGN Viewer")
        self._build_ui()

    def _build_ui(self):
        S, M = 50, 25
        size = S * 8 + M * 2
        self.canvas = tk.Canvas(self.window, width=size, height=size)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        white = self.game.headers.get("White", "White")
        black = self.game.headers.get("Black", "Black")
        tk.Label(self.window, text=f"White: {white}").grid(
            row=1, column=0, sticky="w", padx=10
        )
        tk.Label(self.window, text=f"Black: {black}").grid(
            row=2, column=0, sticky="w", padx=10
        )

        self.move_label = tk.Label(self.window, text="Move: 0")
        self.move_label.grid(row=1, column=1, sticky="e", padx=10)

        nav = tk.Frame(self.window)
        nav.grid(row=2, column=1, sticky="e", padx=10)
        tk.Button(nav, text="Previous", command=self.prev_move).pack(
            side="left", padx=10, pady=10
        )
        tk.Button(nav, text="Next", command=self.next_move).pack(
            side="left", padx=5
        )

        self.draw_board()

    def draw_board(self):
        S, M = 50, 25
        C = self.canvas
        C.delete("all")

        light, dark = "#F0D9B5", "#B58863"
        for r in range(8):
            for f in range(8):
                x1, y1 = f * S + M, (7 - r) * S + M
                x2, y2 = x1 + S, y1 + S
                color = light if (r + f) % 2 else dark
                C.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                f, r = chess.square_file(sq), chess.square_rank(sq)
                x = f * S + M + S / 2
                y = (7 - r) * S + M + S / 2
                C.create_text(x, y, text=piece.unicode_symbol(),
                              font=("Arial", int(S*0.7)))

        for f in range(8):
            letter = chr(ord("a") + f)
            x = f * S + M + S / 2
            C.create_text(x, M + 8 * S + 8, text=letter, font=("Arial", 10))

        for r in range(8):
            num = str(r + 1)
            y = (7 - r) * S + M + S / 2
            C.create_text(M - 8, y, text=num, font=("Arial", 10))

        if self.current_index == 0:
            self.move_label.config(text="Move: 0")
        else:
            self.move_label.config(text=f"Move: {self.board.fullmove_number}")

    def next_move(self):
        if self.current_index < len(self.moves):
            self.board.push(self.moves[self.current_index])
            self.current_index += 1
            self.draw_board()

    def prev_move(self):
        if self.current_index > 0:
            self.board.pop()
            self.current_index -= 1
            self.draw_board()

    def go_to(self, half_move_index):
        # reset to initial position
        self.board = chess.Board(self.initial_fen)
        self.current_index = 0

        # replay moves up to half_move_index
        for i in range(min(half_move_index, len(self.moves))):
            self.board.push(self.moves[i])
            self.current_index += 1

        self.draw_board()
