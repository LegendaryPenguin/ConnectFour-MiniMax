This project was part of the Hack Midwest 2024 competition. I participated in the brAInrot challange for which I had to create a connect 4 AI bot that would face off against other players bots and compete for the win.
The bots were placed in a round robin tournament after submitting.

I tested two main strategies for my Connect $ bot.
MiniMax - This strategy uses a resursive algorithm that checks all possible moves and gives it a score based on how close the opponent will be to winning, how close the bot will be to winning, and future placements.
After recursively testing all spots and giving each possible move a score, the highest scoring move will be placed. 
These moves are testing by creating a decision tree from the game state and creating nodes for each possible move sequence and then testing the scores.
Due to imperfections in the recursive formula, not all moves played will actually be the very best move.

AlphaBeta - This is a strategy that utilizes a minimax style algorithm but attempts to search deeper down the decision tree. 
The algorithm therefore ends up prioritizing future possible moves instead of considering moves that can be played sooner. 
I found that this strategy was particularly effective against my minimax algorithm when the minimax algorithm would start but would would lose every other time it would go second.

As a result, my final player class for the competition used the based minimax algorithm since it won approximately 90% of games when it went first and approximately 50% of games against the other bots going second.

Future Recommendations:
The player class could be greatly improved in the future by creating an algorithm that uses the minimax algorithm every time when going first and the alpha beta algorithm each time it goes second if a minimax is detected.

