# The 24 Game Solver

This is a python3 program that can solve the 24 game by enumerating all possible expressions. It also supports advanced rules(e.g.exponentiation and logarithm).

## Examples

### Basic 24 Game

	Allow advanced operators?
	Advanced operators disabled
	
	Allow unary operator?
	Unary operator disabled
	
	Enumerate all target?
	Just solve one target
	
	Enter a target:
	Target is 24
	
	--------------------
	Enter some numbers:4 6 8 10
	
	24 = 4-10*(6-8)
	24 = 10*(8-6)+4
	24 = 8-4*(6-10)
	24 = (10-6)*4+8
	
	4 solution(s) in 0.266 seconds
	28 duplication(s)
	31104 combination(s)
	--------------------
	Enter some numbers:6 6 7 8
	
	
	0 solution(s) in 0.266 seconds
	0 duplication(s)
	28800 combination(s)
	--------------------
	Enter some numbers:4 4 10 10
	
	24 = (10*10-4)/4
	
	1 solution(s) in 0.229 seconds
	15 duplication(s)
	26496 combination(s)
	--------------------
	Enter some numbers:3 3 8 8
	
	24 = 8/(3-8/3)
	
	1 solution(s) in 0.234 seconds
	31 duplication(s)
	26496 combination(s)
	--------------------

----------------

	Allow advanced operators?
	Advanced operators disabled
	
	Allow unary operator?
	Unary operator disabled
	
	Enumerate all target?
	Just solve one target
	
	Enter a target:36
	Target is 36
	
	--------------------
	Enter some numbers:4 9 8 4
	
	36 = 8*(9-4)-4
	
	1 solution(s) in 0.252 seconds
	15 duplication(s)
	28800 combination(s)
	--------------------
	Enter some numbers:4 1 7 3
	
	36 = (1+4+7)*3
	36 = (1+7+4)*3
	36 = (3-(1-7))*4
	36 = (3+7-1)*4
	36 = 4*(7-(1-3))
	36 = (3-1+7)*4
	
	6 solution(s) in 0.270 seconds
	58 duplication(s)
	31104 combination(s)

### Using Advanced Operators

Exponentiation, logarithm, permutation number and combination number are supported.
    
	Allow advanced operators?y
	Advanced operators enabled
	
	Allow unary operator?
	Unary operator disabled
	
	Enumerate all target?
	Just solve one target
	
	Enter a target:
	Target is 24
	
	--------------------
	Enter some numbers:2 3 10 10
	
	24 = 2/10*C(10, 3)
	24 = C(10, 3)/(10/2)
	24 = 2^10-10^3
	24 = 10-2*(3-10)
	24 = (10-3)*2+10
	24 = 2*C(10, 3)/10
	24 = 2/(10/C(10, 3))
	
	7 solution(s) in 3.184 seconds
	169 duplication(s)
	357504 combination(s)
	--------------------
	Enter some numbers:2 2 2 6
	
	24 = P(6-2, 2/2)
	24 = P(6-2, log_2(2))
	24 = P(6-2, C(2, 2))
	24 = P(6-2, P(2, 2))
	24 = 2*P(6-2, 2)
	24 = 2^(2+log_2(6))
	
	6 solution(s) in 2.461 seconds
	282 duplication(s)
	282240 combination(s)
	--------------------
	Enter some numbers:6 7 9 10
	
	24 = 10*6-C(9, 7)
	24 = 6^(10-7)/9
	
	2 solution(s) in 3.517 seconds
	22 duplication(s)
	395136 combination(s)
	--------------------

### Using Unary Operators

Currently, squreroot and factorial are supported.

	Allow advanced operators?y
	Advanced operators enabled
	
	Allow unary operator?y
	Unary operator enabled
	
	Number of unary operators allowed:
	1 unary operators allowed
	
	Enumerate all target?
	Just solve one target
	
	Enter a target:
	Target is 24
	
	--------------------
	Enter some numbers:1 1 1 1
	
	24 = (1+1+1+1)!
	24 = ((1+1)*(1+1))!
	24 = ((1+1)^(1+1))!
	
	3 solution(s) in 7.457 seconds
	237 duplication(s)
	690336 combination(s)
	--------------------
	Enter some numbers:15 9 9 2
	
	24 = (15+9)*(sqrt(9)-2)
	24 = (15+9)/(sqrt(9)-2)
	24 = 15-9+2*9
	24 = (15-9+2)*sqrt(9)
	24 = sqrt(2^(15-9)*9)
	24 = ((15-9)^2/9)!
	24 = 9+C(15-9, 2)
	24 = 2*9-(9-15)
	24 = (2-(9-15))*sqrt(9)
	24 = sqrt(9/2^(9-15))
	24 = ((9-15)^2/9)!
	24 = 2*sqrt(15*9+9)
	24 = (15+2-9)*sqrt(9)
	24 = sqrt(9)-(9-15*2)
	24 = 15*2-9+sqrt(9)
	24 = 15*2-(9-sqrt(9))
	24 = 15*2+sqrt(9)-9
	24 = (15^2-9)/9
	24 = (9+9)/2+15
	24 = (log_2(15+9/9))!
	24 = (log_2(15+log_9(9)))!
	24 = (log_2(15+C(9, 9)))!
	24 = (log_2(15+P(9, 9)))!
	24 = (15-(9-2))*sqrt(9)
	24 = 15+2*9-9
	24 = 15-(9-2*9)
	24 = 15+9^2/9
	24 = sqrt(9)-(15-C(9, 2))
	24 = C(9, 2)-15+sqrt(9)
	24 = C(9, 2)-(15-sqrt(9))
	24 = C(9, 2)+sqrt(9)-15
	24 = P(9-sqrt(9), 2)/15
	24 = 2*(9*sqrt(9)-15)
	24 = (15-9/sqrt(9))*2
	24 = (9/sqrt(9))^2+15
	24 = 9-15*(2-sqrt(9))
	24 = 9-15/(2-sqrt(9))
	24 = 15-(2-sqrt(9))*9
	24 = 15-9/(2-sqrt(9))
	24 = 15*(sqrt(9)-2)+9
	24 = 15/(sqrt(9)-2)+9
	24 = 15^(sqrt(9)-2)+9
	24 = 15+9*(sqrt(9)-2)
	24 = 15+9/(sqrt(9)-2)
	24 = 15+9^(sqrt(9)-2)
	24 = 15+C(9, sqrt(9)-2)
	24 = 15+C(9, 2^sqrt(9))
	24 = 15+P(9, 2^sqrt(9))
	
	48 solution(s) in 74.951 seconds
	1288 duplication(s)
	7024936 combination(s)
	--------------------

### Enumerate All Targets

The program can enumerate all possible targets for given numbers.

	Allow advanced operators?
	Advanced operators disabled
	
	Allow unary operator?
	Unary operator disabled
	
	Enumerate all target?y
	Solve all targets
	
	--------------------
	Enter some numbers:1 2 3 4
	
	-23 = 1-2*3*4
	-22 = (1-3*4)*2
	-21 = (1-2*4)*3
	-20 = (1-2*3)*4
	-19 = 1-(2+3)*4
	-18 = (1-4)*2*3
	-17 = 1-(2+4)*3
	-16 = (1-2-3)*4
	-15 = (1-2-4)*3
	-14 = 2-(1+3)*4
	-13 = 1-2-3*4
	-12 = (1-2)*3*4
	-11 = 2-1-3*4
	-10 = 1*2-3*4
	-9 = 1+2-3*4
	-8 = 1-2-(3+4)
	-7 = (1-2)*(3+4)
	-6 = 2-1-(3+4)
	-5 = 4-(1+2)*3
	-4 = 1+2-(3+4)
	-3 = (1+2)*(3-4)
	-2 = 4-3-(1+2)
	-1 = (1-2)*(4-3)
	0 = (3-(1+2))*4
	1 = (1-2)*(3-4)
	2 = 1+2+3-4
	3 = (1+2)*(4-3)
	4 = 3+4-(1+2)
	5 = (1+2)*3-4
	6 = 1-2+3+4
	7 = 4-(1-2)*3
	8 = 3+4-(1-2)
	9 = 3*4-(1+2)
	10 = 1+2+3+4
	11 = 1-2+3*4
	12 = (2-1)*3*4
	13 = (1+2)*3+4
	14 = 1*2*(3+4)
	15 = 1+2+3*4
	16 = (3-(1-2))*4
	17 = (1+4)*3+2
	18 = (1*2+4)*3
	19 = (2+3)*4-1
	20 = (1*2+3)*4
	21 = (1+2)*(3+4)
	22 = 2*(3*4-1)
	23 = 2*3*4-1
	24 = (1+2+3)*4
	25 = (1+4)*(2+3)
	26 = (1+3*4)*2
	27 = (1+2*4)*3
	28 = (1+2*3)*4
	30 = (1+4)*2*3
	32 = (1+3)*2*4
	36 = (1+2)*3*4
	
	
	55 targets(s) in 0.304 seconds
	30976 combination(s)
	--------------------

