// push constant 3030
@3030
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// push constant 3040
@3040
D=A
@SP
AM=M+1
A=A-1
M=D
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// push constant 32
@32
D=A
@SP
AM=M+1
A=A-1
M=D
// pop this 2
@2
D=A
@THIS
D=D+M
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
// push constant 46
@46
D=A
@SP
AM=M+1
A=A-1
M=D
// pop that 6
@6
D=A
@THAT
D=D+M
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
// push pointer 0
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
// push pointer 1
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
// add
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
D=D+M
@SP
AM=M+1
A=A-1
M=D
// push this 2
@2
D=A
@THIS
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
// push that 6
@6
D=A
@THAT
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
// add
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
D=D+M
@SP
AM=M+1
A=A-1
M=D