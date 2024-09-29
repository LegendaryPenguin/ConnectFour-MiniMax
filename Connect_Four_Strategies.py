# Define the Connect4 game class first to ensure it is recognized
class Connect4:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.turn = 1  # player 1 goes first

    def detect_win(self):
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        rows, cols = 6, 7

        for x in range(rows):
            for y in range(cols):
                if self.board[x][y] != 0:
                    for dx, dy in dirs:
                        if all(0 <= x + i * dx < rows and 0 <= y + i * dy < cols and
                               self.board[x + i * dx][y + i * dy] == self.board[x][y] for i in range(4)):
                            return self.board[x][y]
        return 0

    def make_move(self, col):
        if col < 0 or col > 6:
            return False
        for row in range(6):
            if self.board[row][col] == 0:
                self.board[row][col] = self.turn
                self.turn = 3 - self.turn
                return True
        return False

    def undo_move(self, col):
        for row in reversed(range(6)):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                return

    def is_full(self):
        return all(self.board[5][c] != 0 for c in range(7))

    def available_moves(self):
        return [c for c in range(7) if self.board[5][c] == 0]


# Define Player1Minimax class that uses minimax strategy
class Player1Minimax:
    def __init__(self, playerOne):
        self.is_player_one = playerOne
        self.player_number = 1 if playerOne else 2

    def makeMove(self, game: Connect4) -> int:
        _, move = self.minimax(game, 4, True)
        return move if move is not None else game.available_moves()[0]

    def minimax(self, game, depth, maximizing):
        winner = game.detect_win()
        if winner == self.player_number:
            return 100000, None
        elif winner == (3 - self.player_number):
            return -100000, None
        elif game.is_full() or depth == 0:
            return self.evaluate_board(game), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in game.available_moves():
                game.make_move(move)
                eval, _ = self.minimax(game, depth - 1, False)
                game.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in game.available_moves():
                game.make_move(move)
                eval, _ = self.minimax(game, depth - 1, True)
                game.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def evaluate_board(self, game):
        # Evaluation heuristic for the board state
        player_score = self.count_patterns(game, self.player_number)
        opponent_score = self.count_patterns(game, 3 - self.player_number)
        return player_score - opponent_score

    def count_patterns(self, game, player):
        score = 0
        rows, cols = 6, 7
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for x in range(rows):
            for y in range(cols):
                if game.board[x][y] == player:
                    for dx, dy in directions:
                        score += self.evaluate_direction(game, x, y, dx, dy, player)
        return score

    def evaluate_direction(self, game, x, y, dx, dy, player):
        count, empty_spaces = 0, 0
        rows, cols = 6, 7

        for i in range(4):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if game.board[nx][ny] == player:
                    count += 1
                elif game.board[nx][ny] == 0:
                    empty_spaces += 1

        if count == 4:
            return 100  # Winning pattern
        elif count == 3 and empty_spaces == 1:
            return 10   # 3-in-a-row with an open space
        elif count == 2 and empty_spaces == 2:
            return 5    # 2-in-a-row with two open spaces
        return 0


# Define Player2AlphaBeta class that uses alpha-beta pruning strategy
class Player2AlphaBeta:
    def __init__(self, playerOne):
        self.is_player_one = playerOne
        self.player_number = 1 if playerOne else 2

    def makeMove(self, game: Connect4) -> int:
        _, move = self.alphabeta(game, 4, float('-inf'), float('inf'), True)
        return move if move is not None else game.available_moves()[0]

    def alphabeta(self, game, depth, alpha, beta, maximizing):
        winner = game.detect_win()
        if winner == self.player_number:
            return 100000, None
        elif winner == (3 - self.player_number):
            return -100000, None
        elif game.is_full() or depth == 0:
            return self.evaluate_board(game), None

        if maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in game.available_moves():
                game.make_move(move)
                eval, _ = self.alphabeta(game, depth - 1, alpha, beta, False)
                game.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in game.available_moves():
                game.make_move(move)
                eval, _ = self.alphabeta(game, depth - 1, alpha, beta, True)
                game.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval, best_move

    def evaluate_board(self, game):
        # Evaluation heuristic for the board state
        player_score = self.count_patterns(game, self.player_number)
        opponent_score = self.count_patterns(game, 3 - self.player_number)
        return player_score - opponent_score

    def count_patterns(self, game, player):
        score = 0
        rows, cols = 6, 7
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for x in range(rows):
            for y in range(cols):
                if game.board[x][y] == player:
                    for dx, dy in directions:
                        score += self.evaluate_direction(game, x, y, dx, dy, player)
        return score

    def evaluate_direction(self, game, x, y, dx, dy, player):
        count, empty_spaces = 0, 0
        rows, cols = 6, 7

        for i in range(4):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if game.board[nx][ny] == player:
                    count += 1
                elif game.board[nx][ny] == 0:
                    empty_spaces += 1

        if count == 4:
            return 100  # Winning pattern
        elif count == 3 and empty_spaces == 1:
            return 10   # 3-in-a-row with an open space
        elif count == 2 and empty_spaces == 2:
            return 5    # 2-in-a-row with two open spaces
        return 0


# Function to print the game board
def print_board(game):
    for row in reversed(game.board):
        print(' '.join(str(cell) for cell in row))
    print()


# Function to simulate a game between Player1Minimax and Player2AlphaBeta
def test_connect4():
    game = Connect4()
    player1 = Player1Minimax(playerOne=True)
    player2 = Player2AlphaBeta(playerOne=False)

    while True:
        print("Player 1's move:")
        col1 = player1.makeMove(game)
        game.make_move(col1)
        print_board(game)

        if game.detect_win() == 1:
            print("Player 1 wins!")
            break
        elif game.is_full():
            print("It's a tie!")
            break

        print("Player 2's move:")
        col2 = player2.makeMove(game)
        game.make_move(col2)
        print_board(game)

        if game.detect_win() == 2:
            print("Player 2 wins!")
            break
        elif game.is_full():
            print("It's a tie!")
            break


# Run the test function to simulate the game
test_connect4()
