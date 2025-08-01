def bind_navigation_keys(root, pgn_window):

    root.bind_all("<Right>",  lambda e: pgn_window.next_move(),  add="+")

    root.bind_all("<Left>",   lambda e: pgn_window.prev_move(), add="+")