// function Class1.set 0
(Class1.set)
// push argument 0
@0
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
AM=M+1
A=A-1
M=D
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@StaticsTest.0
M=D
// push argument 1
@1
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
AM=M+1
A=A-1
M=D
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@StaticsTest.1
M=D
// push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
// return
@LCL
D=M
@FRAME
M=D
@FRAME
D=M
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME
A=M-1
D=M
@THAT
M=D
@FRAME
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
// function Class1.get 0
(Class1.get)
// push static 0
@StaticsTest.0
D=M
@SP
AM=M+1
A=A-1
M=D
// push static 1
@StaticsTest.1
D=M
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
M=M-1
@SP
A=M
D=M
@num1
M=D
@SP
M=M-1
@SP
A=M
D=M
@num1
D=D-M
@SP
AM=M+1
A=A-1
M=D
// return
@LCL
D=M
@FRAME
M=D
@FRAME
D=M
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME
A=M-1
D=M
@THAT
M=D
@FRAME
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
AM=M+1
A=A-1
M=D
// push constant 8
@8
D=A
@SP
AM=M+1
A=A-1
M=D
// call Class1.set 2
@StaticsTest$ret.1
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@2
D=A
@SP
D=M-D
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(StaticsTest$ret.1)
// pop temp 0
@5
D=A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// push constant 23
@23
D=A
@SP
AM=M+1
A=A-1
M=D
// push constant 15
@15
D=A
@SP
AM=M+1
A=A-1
M=D
// call Class2.set 2
@StaticsTest$ret.2
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@2
D=A
@SP
D=M-D
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(StaticsTest$ret.2)
// pop temp 0
@5
D=A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// call Class1.get 0
@StaticsTest$ret.3
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
D=M-D
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(StaticsTest$ret.3)
// call Class2.get 0
@StaticsTest$ret.4
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
D=M-D
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(StaticsTest$ret.4)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
// function Class2.set 0
(Class2.set)
// push argument 0
@0
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
AM=M+1
A=A-1
M=D
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@StaticsTest.0
M=D
// push argument 1
@1
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
AM=M+1
A=A-1
M=D
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@StaticsTest.1
M=D
// push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
// return
@LCL
D=M
@FRAME
M=D
@FRAME
D=M
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME
A=M-1
D=M
@THAT
M=D
@FRAME
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
// function Class2.get 0
(Class2.get)
// push static 0
@StaticsTest.0
D=M
@SP
AM=M+1
A=A-1
M=D
// push static 1
@StaticsTest.1
D=M
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
M=M-1
@SP
A=M
D=M
@num1
M=D
@SP
M=M-1
@SP
A=M
D=M
@num1
D=D-M
@SP
AM=M+1
A=A-1
M=D
// return
@LCL
D=M
@FRAME
M=D
@FRAME
D=M
@5
A=D-A
D=M
@RET
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME
A=M-1
D=M
@THAT
M=D
@FRAME
D=M
@2
A=D-A
D=M
@THIS
M=D
@FRAME
D=M
@3
A=D-A
D=M
@ARG
M=D
@FRAME
D=M
@4
A=D-A
D=M
@LCL
M=D
@RET
A=M
0;JMP
