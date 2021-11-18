import sys
import os

from lib import lib

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
# 14 declare constant string

#how to print string
# [
#   4, "qword [string-name-here]" # needs to be a qword for 64 bit!
#   3, "print"
# ]


# program = [
#     14, "testStringTwo", "hewo",
#     6, "testString", 100, # declare variable
#     0, "libs/std.asm",    # include standard lib
#     8, "hi", 9, # declare and start function hi
#     4, 107,     # push ascii to stack
#     3, "print", # print
#     4, 10,      # push newline to stack
#     3, "print", # print

#     7, "testString", 77,     # cool stuff with uninitalized strings
#     7, "testString + 1", 10,
#     4, "qword [testString]",
#     3, "print",

#     4, "qword [testStringTwo]", # print string constant
#     5, "testString",            # pop to variable
#     4, "qword [testString]",    # put variable back in stack
#     3, "print",

#     10,         # end func "hi"
#     2, 98, 1,   # add second and third and push to stack
#     3, "print", # print
#     4, 10,      # push 10 (newline) to stack
#     3, "print", # print
#     3, "hi"     # call func "hi"
# ]

#test files stuff

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

def writeTok(i, file):
    if program[i] == 1:
        print('add opcode')
        file.write('    push %s + %s\n' % (program[i+1], program[i+2]))
        i+=2
    elif program[i] == 2:
        print('sub opcode')
        file.write('    push %s - %s\n' % (program[i+1], program[i+2]))
        i+=2
    elif program[i] == 3:
        print('call: %s' % program[i+1])
        file.write('    call %s\n' % program[i+1])
        i+=1
    elif program[i] == 4:
        print('push')
        file.write('    push %s\n' % program[i+1])
        i+=1
    elif program[i] == 5:
        print('pop to variable')
        file.write('    ;;pop to variable\n')
        file.write('    pop qword [%s]\n' % program[i+1])
        i+=1
    elif program[i] == 7:
        print('setting value into var')
        file.write('    ;;set value in variable\n')
        file.write('    mov dword [%s], %s\n' % (program[i+1], program[i+2]))
        i+=2
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
        file.write('section .data\n')

        while(i < len(program)):
            if program[i] == 14:
                print('declare string constant')
                file.write('%s DB "%s", 0\n' % (program[i+1], program[i+2]))
                i+=3
            else:
                break

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
                lib(file, program[i+1])
                i+=1
            else:
                break
            i+=1

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