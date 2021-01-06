// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// total = 255 * 32 = 8192
// Loop 1 to 8191
// keyboard address is 24576

// screen_addr = SCREEN
// n = 8191

// (START)
// i = 0

// if RAM[KEYBOARD] == 0 goto FILL_WHITE
	

	// (FILL_BLACK)
	// if i > 8191 GOTO START
		//RAM[screen_addr + i] = -1
		//i = i + 1
		//goto FILL_BLACK

	// (FILL_WHITE)
	// i = 0
	// if i > 8191 GOTO START
		// RAM[screen_addr + i] = 0
		// i = i + 1
		// goto FILL_WHITE


// screen_addr = SCREEN
@SCREEN
D=A
@screen_addr
M=D

// n = 8191
@8191
D=A
@n
M=D

(START)
// i = 0
@i
M=0

// if RAM[KEYBOARD] == 0 

// goto FILL_WHITE
@KBD
D=M
@FILL_WHITE
D;JEQ

(FILL_BLACK)
	// if i > 8191
	@i
	D=M
	@n
	D=D-M
	@START
	D;JGT // if i > n

		//RAM[screen_addr + i] = -1
		@i
		D=M
		@screen_addr
		A=M+D
		M=-1

		//i = i + 1
		@i
		M=M+1

		//goto FILL_BLACK
		@FILL_BLACK
		0;JMP



(FILL_WHITE)
	// if i > 8191
	@i
	D=M
	@n
	D=D-M
	@START
	D;JGT // if i > n

		//RAM[screen_addr + i] = 0
		@i
		D=M
		@screen_addr
		A=M+D
		M=0

		//i = i + 1
		@i
		M=M+1

		//goto FILL_WHITE
		@FILL_WHITE
		0;JMP




















