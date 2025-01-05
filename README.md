# Graphical Chess Game

## Overview

This project is a graphical implementation of the classic game of Chess using Python and the Pygame library. It allows two players to play against each other on the same computer. The game includes features like:

-   Visual representation of the chessboard and pieces.
-   Mouse-based controls for selecting and moving pieces.
-   Highlighting of valid moves.
-   Check detection (with the king highlighted in red when in check).
-   Checkmate and stalemate detection.
-   **En Passant** capture.
-   **Castling** move.
-   **Pawn Promotion** (to Queen, Rook, Bishop, or Knight).

## Requirements

-   Python 3.x
-   Pygame library

## Installation

1.  **Install Python 3:** If you don't have Python 3 installed, download it from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Install Pygame:** Open a terminal or command prompt and run:

    ```bash
    pip install pygame
    ```

3.  **Download Assets:**
    *   Create a folder named `assets` in the same directory as the Python script.
    *   Download a set of chess piece images in PNG format. You can find free sets online (e.g., from Wikimedia Commons or Lichess.org).
    *   Rename the images according to the following naming convention:
        *   `w` or `b` for the color (white or black).
        *   `p`, `r`, `n`, `b`, `q`, or `k` for the piece type (pawn, rook, knight, bishop, queen, or king).
        *   Example: `wp.png` (white pawn), `br.png` (black rook).
    *   Place the images inside the `assets` folder.

## How to Run

1.  **Clone the Repository (Optional):** If the code is on GitHub, you can clone it:

    ```bash
    git clone <repository_url>
    ```

2.  **Navigate to the Directory:** Open a terminal and use the `cd` command to navigate to the directory where you saved the `chess_game.py` file and the `assets` folder.

3.  **Run the Game:** Execute the following command in the terminal:

    ```bash
    python chess_game.py
    ```

## How to Play

1.  **Select a Piece:** Click the left mouse button on a piece of your color that you want to move. The selected piece will be highlighted.
2.  **Move the Piece:** Click the left mouse button again on a valid destination square. Valid moves are indicated by blue circles.
3.  **Special Moves:**
    *   **En Passant:** If a pawn moves two squares forward from its starting position and lands beside an opponent's pawn, the opponent's pawn can capture it "in passing" on the next move as if it had moved only one square forward.
    *   **Castling:** If neither the king nor the chosen rook has moved, the path between them is clear, and the king is not in check or would not pass through check, the king can move two squares towards the rook, and the rook will jump to the other side of the king.
    *   **Pawn Promotion:** When a pawn reaches the opposite end of the board, it can be promoted to a Queen, Rook, Bishop, or Knight. A small window will appear allowing you to choose the desired piece.
4.  **Check:** If your king is under attack (in "check"), you must make a move to remove the threat. The king will be highlighted with a red background when in check. Also, when the king is in check only those moves will be shown which will remove the check.
5.  **Checkmate:** If your king is in check and there is no legal move to remove the threat, you are "checkmated," and the game ends.
6.  **Stalemate:** If it's your turn to move, you are not in check, but you have no legal moves, the game is a "stalemate" (a draw).

## Controls

-   **Left Mouse Button:** Select a piece, move a piece, choose promotion piece.

## Code Structure

-   `chess_game.py`: The main Python file containing the game code.
-   `assets/`: Folder containing the PNG images for the chess pieces.

## Key Functions

-   `load_pieces()`: Loads and resizes piece images.
-   `draw_board()`: Draws the chessboard.
-   `draw_pieces()`: Draws the pieces on the board.
-   `get_square_under_mouse()`: Gets the board coordinates of the clicked square.
-   `draw_selector()`: Highlights the selected piece.
-   `draw_valid_moves()`: Highlights valid moves for the selected piece.
-   `is_valid_move()`: Checks if a move is valid (general rules).
-   `is_valid_pawn_move()`, `is_valid_rook_move()`, etc.: Check the validity of moves for specific piece types.
-   `is_valid_en_passant()`: Checks if an en passant capture is valid.
-   `is_valid_castling()`: Checks if castling is valid.
-   `is_path_clear()`: Checks if the path between two squares is clear.
-   `get_valid_moves()`: Returns a list of valid moves for a selected piece.
-   `is_check()`: Checks if a king is in check.
-   `get_all_valid_moves()`: Returns all valid moves for a given side, taking checks into account.
-   `is_checkmate()`: Checks for checkmate.
-   `is_stalemate()`: Checks for stalemate.
-   `make_move()`: Makes a move on the board (handles en passant, castling, and pawn promotion).
-   `draw_check()`: Highlights the king in red if it's in check.
-   `promote_pawn()`: Handles pawn promotion.

## Contributing

Contributions are welcome! If you have suggestions, bug fixes, or want to add new features, feel free to fork the repository, make your changes, and submit a pull request.
