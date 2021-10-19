# Assembly-2-lol
assembly 2
## How to run
lets run an example program,
```python
program = [
    0, 1,       # include standard lib
    1, 98, 1,   # add second to third and push to stack
    3,          # dump
    4, 10,      # push 10 (newline) to stack
    3           # dump
]
```
This can be compiled by changing program in main.py, then running
```
python3 main.py -c
```
If there are no errors, run
```
./out
```
