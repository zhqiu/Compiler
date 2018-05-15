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
power:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  sw $a0, -36($sp)
  sw $a1, -40($sp)
  li $t0, 1
  sw $t0, -44($sp)
label1:
  lw $t0, -40($sp)
  li $t1, 0
  bgt $t0, $t1, label2
  j label3
label2:
  lw $t4, -44($sp)
  lw $t5, -36($sp)
  mul $t3, $t4, $t5
  sw $t3, -44($sp)
  move $t2, $t3
  lw $t2, -40($sp)
  li $t3, 1
  sub $t1, $t2, $t3
  sw $t1, -40($sp)
  move $t0, $t1
  j label1
label3:
  lw $t0, -44($sp)
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

mod:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  sw $a0, -36($sp)
  sw $a1, -40($sp)
  lw $t1, -36($sp)
  lw $t5, -36($sp)
  lw $t6, -40($sp)
  div $t5, $t6
  mflo $t3
  lw $t4, -40($sp)
  mul $t2, $t3, $t4
  sub $t0, $t1, $t2
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

getNumDigits:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  sw $a0, -36($sp)
  li $t0, 0
  sw $t0, -40($sp)
  lw $t0, -36($sp)
  li $t1, 0
  blt $t0, $t1, label4
  j label5
label4:
  li $t3, 1
  li $t4, 0
  sub $t2, $t4, $t3
  move $v0, $t2
  lw $s7, -32($sp)
  lw $s6, -28($sp)
  lw $s5, -24($sp)
  lw $s4, -20($sp)
  lw $s3, -16($sp)
  lw $s2, -12($sp)
  lw $s1, -8($sp)
  lw $s0, -4($sp)
  jr $ra
label5:
label6:
  lw $t0, -36($sp)
  li $t1, 0
  bgt $t0, $t1, label7
  j label8
label7:
  lw $t4, -36($sp)
  li $t5, 10
  div $t4, $t5
  mflo $t3
  sw $t3, -36($sp)
  move $t2, $t3
  lw $t2, -40($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -40($sp)
  move $t0, $t1
  j label6
label8:
  lw $t0, -40($sp)
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

isNarcissistic:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  sw $a0, -36($sp)
  lw $a0, -36($sp)
  addi $sp, $sp, -40
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
  jal getNumDigits
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
  addi $sp, $sp, 40
  move $t0, $v0
  sw $t0, -40($sp)
  li $t0, 0
  sw $t0, -44($sp)
  lw $t0, -36($sp)
  sw $t0, -48($sp)
label9:
  lw $t0, -48($sp)
  li $t1, 0
  bgt $t0, $t1, label10
  j label11
label10:
  lw $a0, -48($sp)
  li $a1, 10
  addi $sp, $sp, -56
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
  jal mod
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
  addi $sp, $sp, 56
  move $t3, $v0
  sw $t3, -52($sp)
  move $t2, $t3
  lw $t4, -48($sp)
  lw $t5, -52($sp)
  sub $t2, $t4, $t5
  li $t3, 10
  div $t2, $t3
  mflo $t1
  sw $t1, -48($sp)
  move $t0, $t1
  lw $t2, -44($sp)
  lw $a0, -52($sp)
  lw $a1, -40($sp)
  addi $sp, $sp, -56
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
  jal power
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
  addi $sp, $sp, 56
  move $t3, $v0
  add $t1, $t2, $t3
  sw $t1, -44($sp)
  move $t0, $t1
  j label9
label11:
  lw $t0, -44($sp)
  lw $t1, -36($sp)
  beq $t0, $t1, label12
  j label13
label12:
  li $t2, 1
  move $v0, $t2
  lw $s7, -32($sp)
  lw $s6, -28($sp)
  lw $s5, -24($sp)
  lw $s4, -20($sp)
  lw $s3, -16($sp)
  lw $s2, -12($sp)
  lw $s1, -8($sp)
  lw $s0, -4($sp)
  jr $ra
  j label14
label13:
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
label14:

printHexDigit:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  sw $a0, -36($sp)
  lw $t0, -36($sp)
  li $t1, 10
  blt $t0, $t1, label15
  j label16
label15:
  lw $a0, -36($sp)
  addi $sp, $sp, -40
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
  addi $sp, $sp, 40
  move $t2, $v0
  j label17
label16:
  lw $t1, -36($sp)
  li $t2, 0
  sub $a0, $t2, $t1
  addi $sp, $sp, -40
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
  addi $sp, $sp, 40
  move $t0, $v0
label17:
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

printHex:
  sw $s0, -4($sp)
  sw $s1, -8($sp)
  sw $s2, -12($sp)
  sw $s3, -16($sp)
  sw $s4, -20($sp)
  sw $s5, -24($sp)
  sw $s6, -28($sp)
  sw $s7, -32($sp)
  sw $a0, -36($sp)
  li $t0, 0
  sw $t0, -56($sp)
label18:
  lw $t0, -56($sp)
  li $t1, 4
  blt $t0, $t1, label19
  j label20
label19:
  lw $a0, -36($sp)
  li $a1, 16
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
  jal mod
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
  move $t3, $v0
  lw $t4, -56($sp)
  li $t5, -4
  mul $t4, $t4, $t5
  addi $t4, $t4, -40
  add $sp, $sp, $t4
  sw $t3, 0($sp)
  sub $sp, $sp, $t4
  lw $t2, -36($sp)
  li $t3, 16
  div $t2, $t3
  mflo $t1
  sw $t1, -36($sp)
  move $t0, $t1
  lw $t2, -56($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -56($sp)
  move $t0, $t1
  j label18
label20:
  li $t1, 3
  sw $t1, -56($sp)
  move $t0, $t1
label21:
  lw $t0, -56($sp)
  li $t1, 0
  bge $t0, $t1, label22
  j label23
label22:
  lw $t3, -56($sp)
  li $t4, -4
  mul $t3, $t3, $t4
  addi $t3, $t3, -40
  add $sp, $sp, $t3
  lw $a0, 0($sp)
  sub $sp, $sp, $t3
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
  jal printHexDigit
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
  lw $t2, -56($sp)
  li $t3, 1
  sub $t1, $t2, $t3
  sw $t1, -56($sp)
  move $t0, $t1
  j label21
label23:
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
  sw $t0, -36($sp)
  li $t0, 9474
  sw $t0, -40($sp)
label24:
  lw $t0, -40($sp)
  li $t1, 9475
  blt $t0, $t1, label25
  j label26
label25:
  lw $a0, -40($sp)
  addi $sp, $sp, -44
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
  jal isNarcissistic
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
  addi $sp, $sp, 44
  move $t2, $v0
  li $t3, 1
  beq $t2, $t3, label27
  j label28
label27:
  lw $a0, -40($sp)
  addi $sp, $sp, -44
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
  jal printHex
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
  addi $sp, $sp, 44
  move $t4, $v0
  lw $t2, -36($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -36($sp)
  move $t0, $t1
label28:
  lw $t2, -40($sp)
  li $t3, 1
  add $t1, $t2, $t3
  sw $t1, -40($sp)
  move $t0, $t1
  j label24
label26:
  lw $t0, -36($sp)
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


