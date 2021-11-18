;;functions from file.asm
files_write:
    pop r10
    ;how to use

    ;push len
    ;push msg
    ;push filename

    ;call write
    
    pop rdi ;filename
    ;mov rdi, filename
    mov rsi, 0102o     ;O_CREAT, man open
    mov rdx, 0666o     ;umode_t
    mov rax, 2
    syscall

    pop rsi ;msg
    pop rdx ;msg len

    ;mov [fd], rax
    ;mov rdx, len       ;message length
    ;mov rsi, msg       ;message to write
    push rax
    mov rdi, rax      ;file descriptor
    mov rax, 1         ;system call number (sys_write)
    syscall            ;call kernel
    pop rdi
    mov rax, 3         ;sys_close
    syscall

    push r10

    ret
files_delete:
    pop r10

    pop rbx ;file path
    mov eax, 10 ; unlink syscall 
    int  0x80 ;syscall

    push r10
    ret
;;end of fuction from file.asm
