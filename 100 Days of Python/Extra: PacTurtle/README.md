(Incomplete) 
Faced some difficulties with 
1. getting ghosts to chase pacman
2. collisions with walls
3. for some reason, hiding food after they've been eaten. 
  [SOLVED] - 
  

Take-away points:
To control multiple objects with diff states but same class,
1. Inherit Turtle, use SELF, create multiple objects in main.py (paddle in Day 22: ponGArt)
   (Exception: food in Extra: PacTurtle as self.clear() can clear .write() & .dot())
2. Don't inherit turtle, use LIST to control (snake in Day 21: Snake Game)

To control single object,
1. Inherit Turtle, use SELF

