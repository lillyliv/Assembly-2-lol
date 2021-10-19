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
# 8: declare function
# 9: start of function
# 10: end of function
# 11: if                 Not implemented
#   1: equ
#   2: not equ
# 12 start if            Not implemented
# 13 end if              Not implemented

program = [
    6, "testString", 100, #declare variable
    0, "libs/std.asm",    # include standard lib
    8, "hi", 9,
    4, 107,
    3, "dump",
    4, 10,
    3, "dump",
    10,
    1, 98, 1,   # add second to third and push to stack
    3, "dump",  # dump
    4, 10,      # push 10 (newline) to stack
    3, "dump",  # dump
    3, "hi"
]

def writeTok(i, file):
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
    return i
def compile():
    with open('out.asm', 'w') as file:
        print('compiling...')
        
        i = 0

        file.write('global _start\n')
        file.write('section .bss\n')
        file.write('toDump resb 8\n')
        file.write('toPrint resb 1000\n')
        file.write('memory resb 10000000\n')

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
                std(file, program[i+1])
            else:
                break
            i+=2

        inFunc = False

        while(i < len(program)):
            if program[i] == 8:
                print('declare function')
                inFunc = True
                file.write('%s:\n' % program[i+1])
                i+=3
            elif program[i] != 8 and inFunc == False:
                break
            elif inFunc == True and program[i] != 10:
                i=writeTok(i, file)
            elif inFunc == True and program[i] == 10:
                print('end of func')
                file.write('    ret\n')
                inFunc = False
                i+=1


        file.write('_start:\n')
        while i < len(program):
            i = writeTok(i, file)

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