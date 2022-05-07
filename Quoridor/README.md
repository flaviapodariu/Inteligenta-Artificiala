# Quoridor

## Players
 There are 2 players:
* Player 1 (the red pawn) - starts the game
* Player 2 (the blue pawn)

 Inside the algorithms, the players will be represented as PMIN and PMAX
  
 The user can choose between the two colors, but he will always play as PMIN,
  leaving PMAX for the computer.
## Representation of walls
 A cell has 4 edges where walls can be placed:
    
     UP    = 2⁰
     RIGHT = 2¹
     DOWN  = 2²
     LEFT  = 2³
 The cell's code will be the values of its' walls summed up.

 So if a cell only has a wall on its left, its code will be 8.

 The up-left corner will initially have a code of 9 since it has nothing
 upwards or on its left (1 + 8 = 9).



