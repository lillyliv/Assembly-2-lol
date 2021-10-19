import sys
import os

from std import std

# opcodes list
# 0: include
# 1: add
# 2: sub
# 3: call
# 4: push
# 5: pop to variable
# 6: declare variable
# 7: set value to variable

program = [
    6, "testString", 100, #declare variable
    0, 1,       # include standard lib
    1, 98, 1,   # add second to third and push to stack
    3, "dump",  # dump
    4, 10,      # push 10 (newline) to stack
    3, "dump",  # dump
    4, 98,      # push and print char constant
    3, "print"  # print
]

def compile():
    with open('out.asm', 'w') as file:
        print('compiling...')

        i = 0

        file.write('global _start\n')
        file.write('section .bss\n')
        file.write('toDump resb 8\n')
        file.write('toPrint resb 1000\n')

        while(i < len(program)):
            if program[i] == 6:
                print('decalre variable')
                file.write('%s resb %s\n' % (program[i+1], program[i+2]))
                i+=2
            else:
                break
            i+=1

        file.write('section .text\n')

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
            elif program[i] == 2:
                print('sub opcode')
                file.write('    ;;subtract\n')
                file.write('    mov rax, %s - %s\n' % (program[i+1], program[i+2]))
                file.write('    push rax\n')
                i+=2
            elif program[i] == 3:
                print('call: %s' % program[i+1])
                file.write('    ;;call\n')
                file.write('    call %s\n' % program[i+1])
                i+=1
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
