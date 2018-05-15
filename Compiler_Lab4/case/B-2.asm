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
  addi $sp, $sp, -36
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
  jal read
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
  addi $sp, $sp, 36
  move $t0, $v0
  sw $t0, -36($sp)
  li $t0, 2
  sw $t0, -40($sp)
label1:
  lw $t0, -40($sp)
  lw $t1, -36($sp)
  ble $t0, $t1, label2
  j label3
label2:
  li $t3, 2
  sw $t3, -44($sp)
  move $t2, $t3
  lw $t2, -40($sp)
  li $t3, 2
  div $t2, $t3
  mflo $t1
  sw $t1, -48($sp)
  move $t0, $t1
  li $t1, 1
  sw $t1, -52($sp)
  move $t0, $t1
label4:
  lw $t0, -44($sp)
  lw $t1, -48($sp)
  ble $t0, $t1, label5
  j label6
label5:
  lw $t4, -40($sp)
  lw $t8, -40($sp)
  lw $t9, -44($sp)
  div $t8, $t9
  mflo $t6
  lw $t7, -44($sp)
  mul $t5, $t6, $t7
  sub $t3, $t4, $t5
  sw $t3, -56($sp)
  move $t2, $t3
  lw $t0, -56($sp)
  li $t1, 0
  beq $t0, $t1, label7
  j label8
label7:
  li $t3, 0
  sw $t3, -52($sp)
  move $t2, $t3
label8:
  lw $t2, -44($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -44($sp)
  move $t0, $t1
  j label4
label6:
  lw $t0, -52($sp)
  li $t1, 1
  beq $t0, $t1, label9
  j label10
label9:
  lw $a0, -40($sp)
  addi $sp, $sp, -60
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
  addi $sp, $sp, 60
  move $t2, $v0
label10:
  lw $t2, -40($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -40($sp)
  move $t0, $t1
  j label1
label3:
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


