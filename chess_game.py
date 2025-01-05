import pygame
import sys
import copy

# Initialize Pygame
pygame.init()

# --- Constants ---
# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Board dimensions
ROWS = 8
COLS = 8
SQUARE_SIZE = 60
BOARD_POS = (0, 0)  # Top-left corner of the board
board_x, board_y = BOARD_POS

# Window dimensions
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

# --- Pygame Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# --- Functions ---

def load_pieces():
    """Loads piece images and resizes them."""
    pieces = {}
    for color in ["w", "b"]:
        for piece in ["p", "r", "n", "b", "q", "k"]:
            img = pygame.image.load(f"assets/{color}{piece}.png")
            pieces[color + piece] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
    return pieces

def draw_board():
    """Draws the chessboard."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board, pieces):
    """Draws the pieces on the board."""
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_under_mouse(board, pos):
    """Returns the row and column of the square under the mouse position"""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return (row, col)
    else:
        return None

def get_notation_under_mouse(pos):
    """Returns the algebraic notation of the square under the mouse position"""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        col_notation = chr(ord('a') + col)
        row_notation = str(8 - row)
        return col_notation + row_notation
    else:
        return None

def draw_selector(board, pieces, selected_piece_pos):
    """Draws a highlight around a selected piece"""
    if selected_piece_pos:
        row, col = selected_piece_pos
        pygame.draw.rect(screen, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

def draw_valid_moves(board, pieces, valid_moves):
    """Draws valid moves for the selected piece."""
    for move in valid_moves:
        end_row, end_col = move
        pygame.draw.circle(screen, BLUE, (end_col * SQUARE_SIZE + SQUARE_SIZE // 2, end_row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)

def is_valid_move(board, start_row, start_col, end_row, end_col, turn, en_passant_target = None):
    """Checks if a move is valid."""
    piece = board[start_row][start_col]

    # Basic checks
    if piece == "--":
        return False  # No piece at the starting position
    if (turn == "white" and piece[0] == "b") or (turn == "black" and piece[0] == "w"):
        return False  # Wrong color to move.

    if start_row == end_row and start_col == end_col:
        return False  # Cannot move to the same square

    if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
        return False  # Move is out of bounds

    destination_piece = board[end_row][end_col]
    if destination_piece != "--" and (piece[0] == destination_piece[0]):
        return False  # Cannot capture your own piece

    # Specific piece movement logic
    if piece[1] == "p":
        return is_valid_pawn_move(board, start_row, start_col, end_row, end_col, turn) or is_valid_en_passant(board, start_row, start_col, end_row, end_col, turn, en_passant_target)
    elif piece[1] == "r":
        return is_valid_rook_move(board, start_row, start_col, end_row, end_col)
    elif piece[1] == "n":
        return is_valid_knight_move(board, start_row, start_col, end_row, end_col)
    elif piece[1] == "b":
        return is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
    elif piece[1] == "q":
        return is_valid_queen_move(board, start_row, start_col, end_row, end_col)
    elif piece[1] == "k":
        return is_valid_king_move(board, start_row, start_col, end_row, end_col)
    else:
        return False

def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, turn):
    """Checks if a pawn move is valid."""
    piece = board[start_row][start_col]
    direction = -1 if piece[0] == "w" else 1  # White moves up (-1), black moves down (+1)

    # One square forward
    if start_col == end_col and end_row == start_row + direction and board[end_row][end_col] == "--":
        return True

    # Two squares forward (only on the initial move)
    if start_col == end_col and end_row == start_row + 2 * direction and board[end_row][end_col] == "--" and board[start_row + direction][end_col] == "--":
        if (piece[0] == "w" and start_row == 6) or (piece[0] == "b" and start_row == 1):
            return True

    # Capture diagonally
    if abs(end_col - start_col) == 1 and end_row == start_row + direction:
        if (piece[0] == "w" and board[end_row][end_col][0] == "b") or (piece[0] == "b" and board[end_row][end_col][0] == "w"):
            return True

    return False

def is_path_clear(board, start_row, start_col, end_row, end_col):
    """Checks if the path between two squares is clear (except for knight moves)."""
    row_step = 0 if start_row == end_row else 1 if start_row < end_row else -1
    col_step = 0 if start_col == end_col else 1 if start_col < end_col else -1

    current_row = start_row + row_step
    current_col = start_col + col_step

    while current_row != end_row or current_col != end_col:
        if board[current_row][current_col] != "--":
            return False
        current_row += row_step
        current_col += col_step

    return True

def is_valid_rook_move(board, start_row, start_col, end_row, end_col):
    """Checks if a rook move is valid."""
    if start_row == end_row or start_col == end_col:  # Must move in a straight line
        return is_path_clear(board, start_row, start_col, end_row, end_col)
    return False

def is_valid_knight_move(board, start_row, start_col, end_row, end_col):
    """Checks if a knight move is valid."""
    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
    """Checks if a bishop move is valid."""
    if abs(start_row - end_row) == abs(start_col - end_col):  # Must move diagonally
        return is_path_clear(board, start_row, start_col, end_row, end_col)
    return False

def is_valid_queen_move(board, start_row, start_col, end_row, end_col):
    """Checks if a queen move is valid."""
    return is_valid_rook_move(board, start_row, start_col, end_row, end_col) or is_valid_bishop_move(board, start_row, start_col, end_row, end_col)

def is_valid_king_move(board, start_row, start_col, end_row, end_col):
    """Checks if a king move is valid."""
    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)
    return row_diff <= 1 and col_diff <= 1

def get_valid_moves(board, selected_piece_pos, turn, en_passant_target, castling_rights):
    """Returns a list of valid moves for the selected piece, including en passant and castling."""
    valid_moves = []
    if selected_piece_pos:
        start_row, start_col = selected_piece_pos
        piece = board[start_row][start_col]

        # Normal moves
        for end_row in range(ROWS):
            for end_col in range(COLS):
                if is_valid_move(board, start_row, start_col, end_row, end_col, turn, en_passant_target):
                    valid_moves.append((end_row, end_col))

        # Castling moves
        if piece[1] == "k":
            if castling_rights[turn]['king_side'] and is_valid_castling(board, start_row, start_col, 7, turn, castling_rights):
                valid_moves.append((start_row, start_col + 2))  # King moves 2 squares to the right
            if castling_rights[turn]['queen_side'] and is_valid_castling(board, start_row, start_col, 0, turn, castling_rights):
                valid_moves.append((start_row, start_col - 2))  # King moves 2 squares to the left

    return valid_moves

def is_check(board, turn):
    """Checks if the given side's king is in check."""
    # Find the king's position
    king_row, king_col = None, None
    for row in range(8):
        for col in range(8):
            if board[row][col] == ("wk" if turn == "white" else "bk"):
                king_row, king_col = row, col
                break

    # Check for attacks from the opponent's pieces
    opponent_turn = "black" if turn == "white" else "white"
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, king_row, king_col, opponent_turn):
                return True
    return False

def get_all_valid_moves(board, turn, en_passant_target, castling_rights):
    """Returns a list of all valid moves for a given side."""
    all_valid_moves = []
    for start_row in range(8):
        for start_col in range(8):
            if (turn == "white" and board[start_row][start_col][0] == "w") or \
               (turn == "black" and board[start_row][start_col][0] == "b"):
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(board, start_row, start_col, end_row, end_col, turn, en_passant_target):
                            # Check for check after the move to avoid illegal moves
                            temp_board = [row[:] for row in board]
                            castling_rights_copy = copy.deepcopy(castling_rights) # Create a deep copy of castling_rights
                            make_move(temp_board, start_row, start_col, end_row, end_col, en_passant_target, castling_rights_copy)
                            if not is_check(temp_board, turn):
                                all_valid_moves.append((start_row, start_col, end_row, end_col))
    return all_valid_moves

def is_checkmate(board, turn):
    """Checks if the given side is in checkmate."""
    return is_check(board, turn) and not get_all_valid_moves(board, turn, en_passant_target, castling_rights)

def is_stalemate(board, turn):
    """Checks if the given side is in stalemate."""
    return not is_check(board, turn) and not get_all_valid_moves(board, turn, en_passant_target, castling_rights)

def make_move(board, start_row, start_col, end_row, end_col):
    """Makes a move on the board."""
    piece = board[start_row][start_col]
    board[end_row][end_col] = piece
    board[start_row][start_col] = "--"
def draw_check(board, turn):
    """Draws a red background for the king if it's in check."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ("wk" if turn == "white" else "bk"):
                if is_check(board, turn):
                    pygame.draw.rect(screen, RED, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def is_valid_castling(board, king_row, king_col, rook_col, turn, castling_rights):
    """Checks if castling is a valid move."""
    # Check if king and rook have moved
    if not castling_rights[turn]['king_side'] and not castling_rights[turn]['queen_side']:
        return False

    # Check if path is clear
    if rook_col > king_col:  # King-side
        for col in range(king_col + 1, rook_col):
            if board[king_row][col] != "--":
                return False
    else:  # Queen-side
        for col in range(rook_col + 1, king_col):
            if board[king_row][col] != "--":
                return False

    # Check if king is in check or would pass through check
    opponent_turn = "black" if turn == "white" else "white"
    for col in range(min(king_col, rook_col), max(king_col, rook_col) + 1):
        # Create a temporary board to simulate the move
        temp_board = [row[:] for row in board]
        temp_board[king_row][king_col] = "--"
        temp_board[king_row][col] = "wk" if turn == "white" else "bk"
        if is_check(temp_board, turn):
            return False
    return True
def is_valid_en_passant(board, start_row, start_col, end_row, end_col, turn, en_passant_target):
    """Checks if an en passant capture is valid."""
    piece = board[start_row][start_col]
    direction = -1 if piece[0] == "w" else 1

    # Check if it's a pawn's diagonal move
    if abs(end_col - start_col) == 1 and end_row == start_row + direction:
        # Check if the target square is the en passant target square
        if (end_row, end_col) == en_passant_target:
            return True

    return False
def promote_pawn(board, row, col, turn):
    """Promotes a pawn to another piece (Queen, Rook, Bishop, or Knight)."""
    while True:
        # Create a small window for promotion choice
        promotion_window = pygame.Surface((SQUARE_SIZE * 4, SQUARE_SIZE))
        promotion_window.fill(GRAY)

        # Load and display the promotion options
        promotion_options = ["q", "r", "b", "n"]
        option_images = [pieces[f"{turn[0]}" + piece] for piece in promotion_options]

        for i, img in enumerate(option_images):
            promotion_window.blit(img, (i * SQUARE_SIZE, 0))

        # Display the promotion window
        screen.blit(promotion_window, (board_x + col * SQUARE_SIZE - (2 * SQUARE_SIZE), \
                                        board_y + row * SQUARE_SIZE if turn == 'black' else board_y + (row - 1) * SQUARE_SIZE ))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                option_index = (x - (board_x + col * SQUARE_SIZE - (2 * SQUARE_SIZE))) // SQUARE_SIZE

                if 0 <= option_index < 4:
                    selected_piece = promotion_options[option_index]
                    board[row][col] = turn[0] + selected_piece
                    return
def make_move(board, start_row, start_col, end_row, end_col, en_passant_target=None, castling_rights=None):
    """Makes a move on the board. Handles en passant, castling, and pawn promotion."""
    global turn
    piece = board[start_row][start_col]

    # Handle en passant capture
    if is_valid_en_passant(board, start_row, start_col, end_row, end_col, turn, en_passant_target):
        board[end_row][end_col] = piece
        board[start_row][start_col] = "--"
        captured_pawn_row = end_row - (-1 if piece[0] == "w" else 1)  # Row of the captured pawn
        board[captured_pawn_row][end_col] = "--"  # Remove the captured pawn

    # Handle castling
    elif piece[1] == "k" and abs(end_col - start_col) == 2:
        board[end_row][end_col] = piece
        board[start_row][start_col] = "--"
        if end_col > start_col:  # King-side
            rook_start_col = 7
            rook_end_col = 5
        else:  # Queen-side
            rook_start_col = 0
            rook_end_col = 3
        board[end_row][rook_end_col] = board[end_row][rook_start_col]
        board[end_row][rook_start_col] = "--"
        # Update castling rights after castling (only if not a simulation)
        if castling_rights:
            castling_rights[turn]['king_side'] = False
            castling_rights[turn]['queen_side'] = False

    else:  # Regular move
        board[end_row][end_col] = piece
        board[start_row][start_col] = "--"

    # Handle pawn promotion
    if piece[1] == "p" and (end_row == 0 or end_row == 7):
        promote_pawn(board, end_row, end_col, turn)
        
    # Update castling rights if king or rook moves (only if not a simulation)
    if castling_rights:
        if piece[1] == "k":
            castling_rights[turn]['king_side'] = False
            castling_rights[turn]['queen_side'] = False
        elif piece[1] == "r":
            if start_col == 0:
                castling_rights[turn]['queen_side'] = False
            elif start_col == 7:
                castling_rights[turn]['king_side'] = False
# --- Game Variables ---
board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]
pieces = load_pieces()
selected_piece_pos = None  # (row, col) of the selected piece
valid_moves = []
turn = "white"
game_over = False
en_passant_target = None  # (row, col) of the en passant target square
castling_rights = {
    "white": {"king_side": True, "queen_side": True},
    "black": {"king_side": True, "queen_side": True}
}

# --- Main Game Loop ---
# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                pos = pygame.mouse.get_pos()
                clicked_square = get_square_under_mouse(board, pos)

                if clicked_square:
                    clicked_row, clicked_col = clicked_square

                    # If a piece is already selected, try to move it
                    if selected_piece_pos:
                        if clicked_square in valid_moves:
                            start_row, start_col = selected_piece_pos
                            # Make the move (no need to check for check here because valid_moves are already filtered)
                            make_move(board, start_row, start_col, clicked_row, clicked_col, en_passant_target, castling_rights)
                            
                            turn = "black" if turn == "white" else "white"

                            # Update en passant target
                            piece = board[clicked_row][clicked_col]
                            if piece[1] == "p" and abs(start_row - clicked_row) == 2:
                                en_passant_target = (start_row + (1 if piece[0] == "b" else -1), clicked_col)
                            else:
                                en_passant_target = None

                            selected_piece_pos = None
                            valid_moves = []

                            # Check for checkmate or stalemate
                            if is_checkmate(board, turn):
                                print(f"Checkmate! {('Black' if turn == 'white' else 'White')} wins!")
                                game_over = True
                            if is_stalemate(board, turn):
                                print("Stalemate! It's a draw.")
                                game_over = True

                        else:
                            selected_piece_pos = None
                            valid_moves = []
                    # If no piece selected or clicked_square doesn't belong to the player, try to select a piece
                    # Inside the main game loop, in the MOUSEBUTTONDOWN event:
                    elif (turn == "white" and board[clicked_row][clicked_col][0] == "w") or \
                         (turn == "black" and board[clicked_row][clicked_col][0] == "b"):
                        selected_piece_pos = clicked_square
                        valid_moves = get_valid_moves(board, selected_piece_pos, turn, en_passant_target, castling_rights)

                        # If the king is in check, filter valid moves to only those that get it out of check
                        if is_check(board, turn):
                            valid_moves_to_remove_check = []
                            for move in valid_moves:
                                start_row, start_col = selected_piece_pos
                                end_row, end_col = move
                                temp_board = [row[:] for row in board]
                                castling_rights_copy = copy.deepcopy(castling_rights) # Create a deep copy of castling_rights
                                make_move(temp_board, start_row, start_col, end_row, end_col, en_passant_target, castling_rights_copy)
                                if not is_check(temp_board, turn):  # Only keep moves that resolve the check
                                    valid_moves_to_remove_check.append(move)
                            valid_moves = valid_moves_to_remove_check  # Update valid_moves

            else: # Game is over, reset the game if user clicks
                board = [
                    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
                    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
                ]
                pieces = load_pieces()
                selected_piece_pos = None
                valid_moves = []
                turn = "white"
                game_over = False
                en_passant_target = None
                castling_rights = {
                    "white": {"king_side": True, "queen_side": True},
                    "black": {"king_side": True, "queen_side": True}
                }

    # --- Drawing ---
    draw_board()
    draw_check(board, turn)  # Draw red background for king in check
    draw_pieces(board, pieces)
    draw_selector(board, pieces, selected_piece_pos)
    draw_valid_moves(board, pieces, valid_moves)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()