.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\n"
.globl main
.text
read:
  li $v0, 4
  la $a0, _prompt
  syscall
  li $v0, 5
  syscall
  jr $ra
write:
  li $v0, 1
  syscall
  li $v0, 4
  la $a0, _ret
  syscall
  move $v0, $0
  jr $ra
main:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  li $t0, 10
  sw $t0, -36($sp)
  li $t0, 20
  sw $t0, -40($sp)
  li $t0, 3
  sw $t0, -44($sp)
  lw $t3, -36($sp)
  lw $t5, -40($sp)
  lw $t6, -44($sp)
  mul $t4, $t5, $t6
  add $t1, $t3, $t4
  lw $t2, -40($sp)
  sub $t0, $t1, $t2
  sw $t0, -48($sp)
  lw $a0, -48($sp)
  addi $sp, $sp, -52
  sw $t0, 0($sp)
  addi $sp, $sp, -4
  sw $t1, 0($sp)
  addi $sp, $sp, -4
  sw $t2, 0($sp)
  addi $sp, $sp, -4
  sw $t3, 0($sp)
  addi $sp, $sp, -4
  sw $t4, 0($sp)
  addi $sp, $sp, -4
  sw $t5, 0($sp)
  addi $sp, $sp, -4
  sw $t6, 0($sp)
  addi $sp, $sp, -4
  sw $t7, 0($sp)
  addi $sp, $sp, -4
  sw $t8, 0($sp)
  addi $sp, $sp, -4
  sw $t9, 0($sp)
  addi $sp, $sp, -4
  sw $ra, 0($sp)
  jal write
  lw $ra, 0($sp)
  addi $sp, $sp, 4
  lw $t9, 0($sp)
  addi $sp, $sp, 4
  lw $t8, 0($sp)
  addi $sp, $sp, 4
  lw $t7, 0($sp)
  addi $sp, $sp, 4
  lw $t6, 0($sp)
  addi $sp, $sp, 4
  lw $t5, 0($sp)
  addi $sp, $sp, 4
  lw $t4, 0($sp)
  addi $sp, $sp, 4
  lw $t3, 0($sp)
  addi $sp, $sp, 4
  lw $t2, 0($sp)
  addi $sp, $sp, 4
  lw $t1, 0($sp)
  addi $sp, $sp, 4
  lw $t0, 0($sp)
  addi $sp, $sp, 52
  move $t0, $v0
  lw $t4, -36($sp)
  lw $t5, -40($sp)
  add $t2, $t4, $t5
  lw $t3, -44($sp)
  div $t2, $t3
  mflo $t1
  sw $t1, -48($sp)
  move $t0, $t1
  lw $a0, -48($sp)
  addi $sp, $sp, -52
  sw $t0, 0($sp)
  addi $sp, $sp, -4
  sw $t1, 0($sp)
  addi $sp, $sp, -4
  sw $t2, 0($sp)
  addi $sp, $sp, -4
  sw $t3, 0($sp)
  addi $sp, $sp, -4
  sw $t4, 0($sp)
  addi $sp, $sp, -4
  sw $t5, 0($sp)
  addi $sp, $sp, -4
  sw $t6, 0($sp)
  addi $sp, $sp, -4
  sw $t7, 0($sp)
  addi $sp, $sp, -4
  sw $t8, 0($sp)
  addi $sp, $sp, -4
  sw $t9, 0($sp)
  addi $sp, $sp, -4
  sw $ra, 0($sp)
  jal write
  lw $ra, 0($sp)
  addi $sp, $sp, 4
  lw $t9, 0($sp)
  addi $sp, $sp, 4
  lw $t8, 0($sp)
  addi $sp, $sp, 4
  lw $t7, 0($sp)
  addi $sp, $sp, 4
  lw $t6, 0($sp)
  addi $sp, $sp, 4
  lw $t5, 0($sp)
  addi $sp, $sp, 4
  lw $t4, 0($sp)
  addi $sp, $sp, 4
  lw $t3, 0($sp)
  addi $sp, $sp, 4
  lw $t2, 0($sp)
  addi $sp, $sp, 4
  lw $t1, 0($sp)
  addi $sp, $sp, 4
  lw $t0, 0($sp)
  addi $sp, $sp, 52
  move $t0, $v0
  lw $t2, -36($sp)
  lw $t3, -40($sp)
  add $t1, $t2, $t3
  sw $t1, -36($sp)
  move $t0, $t1
  lw $t2, -36($sp)
  lw $t3, -40($sp)
  sub $t1, $t2, $t3
  sw $t1, -40($sp)
  move $t0, $t1
  lw $t2, -36($sp)
  lw $t3, -40($sp)
  sub $t1, $t2, $t3
  sw $t1, -36($sp)
  move $t0, $t1
  lw $t6, -36($sp)
  lw $t7, -40($sp)
  sub $t4, $t6, $t7
  li $t5, 2
  div $t4, $t5
  mflo $t2
  lw $s0, -36($sp)
  lw $s1, -40($sp)
  div $s0, $s1
  mflo $t8
  li $t9, 2
  mul $t3, $t8, $t9
  add $t1, $t2, $t3
  sw $t1, -40($sp)
  move $t0, $t1
  lw $a0, -40($sp)
  addi $sp, $sp, -52
  sw $t0, 0($sp)
  addi $sp, $sp, -4
  sw $t1, 0($sp)
  addi $sp, $sp, -4
  sw $t2, 0($sp)
  addi $sp, $sp, -4
  sw $t3, 0($sp)
  addi $sp, $sp, -4
  sw $t4, 0($sp)
  addi $sp, $sp, -4
  sw $t5, 0($sp)
  addi $sp, $sp, -4
  sw $t6, 0($sp)
  addi $sp, $sp, -4
  sw $t7, 0($sp)
  addi $sp, $sp, -4
  sw $t8, 0($sp)
  addi $sp, $sp, -4
  sw $t9, 0($sp)
  addi $sp, $sp, -4
  sw $ra, 0($sp)
  jal write
  lw $ra, 0($sp)
  addi $sp, $sp, 4
  lw $t9, 0($sp)
  addi $sp, $sp, 4
  lw $t8, 0($sp)
  addi $sp, $sp, 4
  lw $t7, 0($sp)
  addi $sp, $sp, 4
  lw $t6, 0($sp)
  addi $sp, $sp, 4
  lw $t5, 0($sp)
  addi $sp, $sp, 4
  lw $t4, 0($sp)
  addi $sp, $sp, 4
  lw $t3, 0($sp)
  addi $sp, $sp, 4
  lw $t2, 0($sp)
  addi $sp, $sp, 4
  lw $t1, 0($sp)
  addi $sp, $sp, 4
  lw $t0, 0($sp)
  addi $sp, $sp, 52
  move $t0, $v0
  li $t0, 0
  move $v0, $t0
  lw $s7, -32($sp)
  lw $s6, -28($sp)
  lw $s5, -24($sp)
  lw $s4, -20($sp)
  lw $s3, -16($sp)
  lw $s2, -12($sp)
  lw $s1, -8($sp)
  lw $s0, -4($sp)
  jr $ra


