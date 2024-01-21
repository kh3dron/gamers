TODOs: 

- Agents
  - [ ] Manual policy network / heuristics to evaluate board values
    - [ ] count stones on board
    - [ ] simple DFS to monopoly proximity to guess at controlled territory?
  - [x] Agents to play against
    - [x] Random
    - [x] Greedy (minmax depth 1-5?)
    - [ ] Minmax with alpha/beta pruning with heuristics 
    - [ ] NNs with X parameters & Y compute-hours

- [ ] Export game / log games to GTP

KNOWN BUGS 
- [ ] Web UI: 
  - [ ] Game doesn't end after double passing
  - [ ] Illegal placements allowed by black 