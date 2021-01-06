// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Pseudo Code

// sum = 0
// i = 1
// LOOP:
// 		if i > R1 goto STOP
// 		sum = sum + R0
// 		i = i + 1
//		goto LOOP
// R2 = sum

// sum = 0
@sum
M=0

// i = 1
@i
M=1

//LOOP:
(LOOP)

	//if i > R1
	@i
	D=M
	@R1
	D=D-M // D = i - R1

	// goto STOP
	@STOP
	D;JGT // if D > 0

	//sum = sum + R0
	@R0
	D=M
	@sum
	M=D+M

	@i
	M=M+1

	@LOOP
	0;JMP

(STOP)
	// R2 = sum
	@sum
	D=M
	@R2
	M=D

(END)
	@END
	0;JMP





