# Crap Nativelang Compiler
## Details
only compiles to linux x86_64 lol
## How to compile

```bash
python3 main.py -c
./out
```
## How to write the language's bytecode
### Printing from variable
Heres a really dumb example "bytecode" program that sets and prints "Hi!" from a variable
```python
program = [
    6, "testString", 100, # declare variable
    0, "libs/std.asm",    # include standard lib

    7, "testString", 72,  # cool stuff with strings
    7, "testString + 1", 105,
    7, "testString + 2", 33,
    7, "testString + 3", 10,
    4, "qword [testString]",
    3, "print",
]
```
### files stuff
this program deletes the file test.txt it exists and then creates the file again and writes "test file lol"
```python
program = [
    14, "toWrite", "test file lol",
    14, "filename", "test.txt",
    0, "libs/std.asm",
    0, "libs/file.asm",
    4, "filename",
    3, "files_delete",
    4, 13,
    4, "toWrite",
    4, "filename",
    3, "files_write"
]
```