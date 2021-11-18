;;Functions from library std
dump:
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

_strlen2:                   ; totally not copy pasted

  push  rbx                 ; save any registers that 
  push  rcx                 ; we will trash in here

  mov   rbx, rdi            ; rbx = rdi

  xor   al, al              ; the byte that the scan will
                            ; compare to is zero

  mov   rcx, 0xffffffff     ; the maximum number of bytes
                            ; i'm assuming any string will
                            ; have is 4gb

  repne scasb               ; while [rdi] != al, keep scanning

  sub   rdi, rbx            ; length = dist2 - dist1
  mov   rax, rdi            ; rax now holds our length

  pop   rcx                 ; restore the saved registers
  pop   rbx

  ret                       ; all done!

print:
    pop r10
    pop rsi
    mov [toPrint], rsi
    mov rsi, toPrint

    mov rdi, rsi
    call _strlen2
    mov rdx, rax

    mov rax, 1
    mov rdi, 1
    syscall

    push r10

    ret

;;End of functions from library std