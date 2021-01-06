// push constant 7
@7
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
