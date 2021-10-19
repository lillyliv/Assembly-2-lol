;;Functions from library std
dump:
    ;;dump
    pop r10
    pop rsi
    mov [toDump], rsi
    mov rsi, toDump
    mov rax, 1
    mov rdi, 1
    mov rdx, 8
    syscall
    push r10
    ret
;;End of functions from library std
