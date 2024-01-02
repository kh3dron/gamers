- Estimating the size of game trees:
  - Chess: about 30 options per move, and games last aorund 80 moves: 30^80 ~= 10^118 states. 
  - Go: 250 options * 150 moves, more like 10^359 states!
- Small prunes to the breadth or depth of the game tree can radically shrink the size of the tree
  - Pruning Heuristics: 
    - Handcrafted - are you playing offensively or defensively? Keep the tree leaning in that direction
      - Flaws here are obvious - can miss when it's best to change strategy


# Performance of ML Models
- Minmax at depth 2 on a 9x9 board takes about half a second per turn - evaluating about 81^2 ~= 6500 options. 
  - 1 more level takes that to half a million