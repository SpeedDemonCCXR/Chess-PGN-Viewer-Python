import tkinter as tk
import chess.pgn
import io
import chess

class PGNWindow:
    def __init__(self, pgn):
        self.pgn = pgn
        self.window = tk.Toplevel()
        self.window.title("Chess PGN Viewer")

        # Parse PGN
        pgn_file = io.StringIO(self.pgn)
        self.game = chess.pgn.read_game(pgn_file)
        self.moves = list(self.game.mainline_moves())
        self.board = self.game.board()
        self.current_index = 0

        # board drawing parameters
        self.tile_size = 50
        self.margin = 25
        canvas_size = self.tile_size * 8 + self.margin * 2
        self.board_canvas = tk.Canvas(
            self.window, width=canvas_size, height=canvas_size
        )
        self.board_canvas.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10
        )

        white_player = self.game.headers.get("White", "White")
        black_player = self.game.headers.get("Black", "Black")
        tk.Label(
            self.window, text=f"White: {white_player}", font=("Arial", 12)
        ).grid(row=1, column=0, sticky="w", padx=10)
        tk.Label(
            self.window, text=f"Black: {black_player}", font=("Arial", 12)
        ).grid(row=2, column=0, sticky="w", padx=10)

        self.move_label = tk.Label(
            self.window, text="Move: 0", font=("Arial", 12)
        )
        self.move_label.grid(row=1, column=1, sticky="e", padx=10)

        nav_frame = tk.Frame(self.window)
        nav_frame.grid(row=2, column=1, sticky="e", padx=10)
        tk.Button(nav_frame, text="Previous", command=self.prev_move).pack(
            side="left", padx=5
        )
        tk.Button(nav_frame, text="Next", command=self.next_move).pack(
            side="left", padx=5
        )

        self.draw_board()

    def draw_board(self):
        S, M = self.tile_size, self.margin
        C = self.board_canvas
        C.delete("all")

        # draw squares
        light, dark = "#F0D9B5", "#B58863"
        for rank in range(8):
            for file in range(8):
                x1 = file * S + M
                y1 = (7 - rank) * S + M
                x2, y2 = x1 + S, y1 + S
                # (0,0) is a1; h1=(7,0) should be light => swap parity
                color = light if (rank + file) % 2 != 0 else dark
                C.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                f = chess.square_file(square)
                r = chess.square_rank(square)
                x = f * S + M + S/2
                y = (7 - r) * S + M + S/2
                C.create_text(x, y, text=piece.unicode_symbol(),
                              font=("Arial", int(S*0.7)))

        # draw file coords (a–h) along bottom
        for f in range(8):
            letter = chr(ord('a') + f)
            x = f * S + M + S/2
            C.create_text(x, M + 8*S + 8, text=letter, font=("Arial", 10))

        # draw rank coords (1–8) along left
        for r in range(8):
            num = str(r + 1)
            y = (7 - r) * S + M + S/2
            C.create_text(M - 8, y, text=num, font=("Arial", 10))

        # update move label to fullmove number
        if self.current_index == 0:
            self.move_label.config(text="Move: 0")
        else:
            # board.fullmove_number increments after Black’s move
            self.move_label.config(
                text=f"Move: {self.board.fullmove_number}"
            )

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

    def show(self):
        self.window.mainloop()
