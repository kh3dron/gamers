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

- [ ] More GUIs everywhere
- [ ] Re-integrate frontend, backend with dlgo state representations
- [ ] Export game / log games to GTP
- [ ] Benchmark model v. model tournaments on 4060Ti, or public GPUs
  - [ ] "Bracket" program to run all model v. model comps, output to readme
- [ ] Pickle models to run inference in browser would be great