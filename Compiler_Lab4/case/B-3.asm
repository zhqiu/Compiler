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
  li $t0, 0
  sw $t0, -76($sp)
  li $t0, 10
  sw $t0, -80($sp)
  li $t0, 0
  sw $t0, -84($sp)
label1:
  lw $t0, -76($sp)
  lw $t1, -80($sp)
  blt $t0, $t1, label2
  j label3
label2:
  lw $t8, -76($sp)
  li $t9, 1
  add $t6, $t8, $t9
  lw $s0, -76($sp)
  li $s1, 1
  add $t7, $s0, $s1
  mul $t4, $t6, $t7
  lw $s2, -76($sp)
  li $s3, 1
  add $t5, $s2, $s3
  mul $t3, $t4, $t5
  sw $t3, -88($sp)
  move $t2, $t3
  lw $t4, -88($sp)
  lw $t8, -88($sp)
  lw $t9, -80($sp)
  div $t8, $t9
  mflo $t6
  lw $t7, -80($sp)
  mul $t5, $t6, $t7
  sub $t1, $t4, $t5
  lw $t2, -76($sp)
  li $t3, -4
  mul $t2, $t2, $t3
  addi $t2, $t2, -36
  add $sp, $sp, $t2
  sw $t1, 0($sp)
  sub $sp, $sp, $t2
  lw $t2, -76($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -76($sp)
  move $t0, $t1
  j label1
label3:
  li $t1, 0
  sw $t1, -76($sp)
  move $t0, $t1
label4:
  lw $t0, -76($sp)
  lw $t1, -80($sp)
  blt $t0, $t1, label5
  j label6
label5:
  lw $t3, -76($sp)
  li $t4, -4
  mul $t3, $t3, $t4
  addi $t3, $t3, -36
  add $sp, $sp, $t3
  lw $a0, 0($sp)
  sub $sp, $sp, $t3
  addi $sp, $sp, -92
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
  addi $sp, $sp, 92
  move $t2, $v0
  lw $t2, -76($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -76($sp)
  move $t0, $t1
  j label4
label6:
  li $t1, 1
  sw $t1, -76($sp)
  move $t0, $t1
label7:
  lw $t0, -76($sp)
  lw $t1, -80($sp)
  blt $t0, $t1, label8
  j label9
label8:
  lw $t4, -76($sp)
  li $t5, -4
  mul $t4, $t4, $t5
  addi $t4, $t4, -36
  add $sp, $sp, $t4
  lw $t2, 0($sp)
  sub $sp, $sp, $t4
  lw $t7, -84($sp)
  li $t8, -4
  mul $t7, $t7, $t8
  addi $t7, $t7, -36
  add $sp, $sp, $t7
  lw $t3, 0($sp)
  sub $sp, $sp, $t7
  blt $t2, $t3, label10
  j label11
label10:
  lw $s1, -76($sp)
  sw $s1, -84($sp)
  move $s0, $s1
label11:
  lw $t2, -76($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -76($sp)
  move $t0, $t1
  j label7
label9:
  lw $t1, -84($sp)
  li $t2, -4
  mul $t1, $t1, $t2
  addi $t1, $t1, -36
  add $sp, $sp, $t1
  lw $a0, 0($sp)
  sub $sp, $sp, $t1
  addi $sp, $sp, -92
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
  addi $sp, $sp, 92
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


