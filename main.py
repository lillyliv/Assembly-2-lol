import sys
import os

from std import std
# opcodes list
# 0: include
# 1: add
# 2: sub
# 3: dump : prints last thing on the stack and removes item
# 4: push

program = [
    0, 1,       # include standard lib
    1, 98, 1,   # add second to third and push to stack
    3,          # dump
    4, 10,      # push 10 (newline) to stack
    3           # dump
]
def compile():
    with open('out.asm', 'w') as file:
        print('compiling...')
        file.write('global _start\n')
        file.write('section .bss\n')
        file.write('toDump resb 8\n')
        file.write('section .text\n')
        i = 0
        while(i < len(program)):
            if program[i] == 0:
                print('import')
                if program[i+1] == 1:
                    std(file)
            else:
                break
            i+=2

        file.write('_start:\n')
        while i < len(program):
            if program[i] == 1:
                print('add opcode')
                file.write('    ;;add\n')
                file.write('    mov rax, %s + %s\n' % (program[i+1], program[i+2]))
                file.write('    push rax\n')
                i+=2
            elif program[i] == 3:
                print('dump')
                file.write('    ;;dump\n')
                file.write('    call dump\n')
            elif program[i] == 4:
                print('push')
                file.write('    ;;push to stack\n')
                file.write('    push %s\n' % program[i+1])
                i+=1
            else:
                print('ERROR, unknown opcode: %s' % (program[i]))
                exit(1)
            i+=1

        file.write('    mov rax, 60\n')
        file.write('    mov rdi, 0\n')
        file.write('    syscall\n')

        file.close()

        os.system('nasm -f elf64 -o out.o out.asm')
        os.system('ld -o out out.o')

if len(sys.argv) < 2:
    print('Error expected an argument')
    print('   USAGE')
    print('   -c <filename>    Compiles program')
    exit(1)
if sys.argv[1] == "-c":
    compile()
    print('Done! executable in ./out')
    exit(1)