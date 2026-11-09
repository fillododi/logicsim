// Accumulator: with write at 1, the instruction's effect on A, CY and DCL's bank, from
// a set A, CY, register and bus value; with reset at 1, all three clear. Random
// instructions (every OPR and OPA appears) with seed 4005, from tools/model4004.py.
chip Accumulator
// Before any reset everything is unknown; without write nothing changes.
set opr 13
set opa 5
set reg 0
set din 0
set write 0
set reset 0
tick
expect acc *
expect carry *
expect bank *
tock
expect acc *
expect carry *
expect bank *
// Reset, then every OPR and OPA once with write at 1, from changing A and CY.
set opr 0
set opa 0
set reg 0
set din 0
set write 0
set reset 1
tick
expect acc *
expect carry *
expect bank *
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 0
set reg 7
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 1
set reg 4
set din 9
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 2
set reg 0
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 3
set reg 5
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 4
set reg 4
set din 9
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 5
set reg 1
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 6
set reg 0
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 7
set reg 12
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 8
set reg 8
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 9
set reg 0
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 10
set reg 0
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 11
set reg 0
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 12
set reg 6
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 13
set reg 8
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 14
set reg 7
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 15
set reg 10
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 0
set reg 6
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 1
set reg 3
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 2
set reg 0
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 3
set reg 10
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 4
set reg 12
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 5
set reg 1
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 6
set reg 2
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 7
set reg 7
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 8
set reg 13
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 9
set reg 4
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 10
set reg 4
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 11
set reg 12
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 12
set reg 15
set din 9
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 13
set reg 7
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 14
set reg 1
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 1
set opa 15
set reg 0
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 0
set reg 0
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 1
set reg 6
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 2
set reg 3
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 3
set reg 9
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 4
set reg 1
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 5
set reg 4
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 6
set reg 6
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 7
set reg 7
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 8
set reg 14
set din 4
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 9
set reg 0
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 10
set reg 5
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 11
set reg 11
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 12
set reg 6
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 13
set reg 9
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 14
set reg 6
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 2
set opa 15
set reg 13
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 0
set reg 7
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 1
set reg 1
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 2
set reg 4
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 3
set reg 12
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 4
set reg 0
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 5
set reg 5
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 6
set reg 14
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 7
set reg 0
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 8
set reg 10
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 9
set reg 2
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 10
set reg 9
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 11
set reg 10
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 12
set reg 4
set din 4
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 13
set reg 4
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 14
set reg 14
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 15
set reg 1
set din 4
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 0
set reg 2
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 1
set reg 3
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 2
set reg 13
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 3
set reg 3
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 4
set reg 2
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 5
set reg 8
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 6
set reg 13
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 7
set reg 1
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 8
set reg 14
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 9
set reg 3
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 10
set reg 7
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 11
set reg 10
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 12
set reg 2
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 13
set reg 3
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 14
set reg 0
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 15
set reg 14
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 0
set reg 0
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 1
set reg 11
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 2
set reg 3
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 3
set reg 14
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 4
set reg 9
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 5
set reg 2
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 6
set reg 0
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 7
set reg 12
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 8
set reg 2
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 9
set reg 1
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 10
set reg 6
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 11
set reg 5
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 12
set reg 11
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 13
set reg 11
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 14
set reg 10
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 15
set reg 12
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 0
set reg 9
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 1
set reg 5
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 2
set reg 11
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 3
set reg 0
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 4
set reg 13
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 5
set reg 8
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 6
set reg 3
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 7
set reg 10
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 8
set reg 3
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 9
set reg 4
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 10
set reg 0
set din 9
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 11
set reg 6
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 12
set reg 3
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 13
set reg 5
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 14
set reg 12
set din 4
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 15
set reg 8
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 0
set reg 1
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 1
set reg 1
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 2
set reg 6
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 3
set reg 14
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 4
set reg 6
set din 1
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 5
set reg 9
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 6
set reg 8
set din 9
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 7
set reg 0
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 8
set reg 7
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 9
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 10
set reg 15
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 11
set reg 2
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 12
set reg 0
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 13
set reg 10
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 14
set reg 2
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 7
set opa 15
set reg 6
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 0
set reg 10
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 8
set opa 1
set reg 3
set din 7
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 8
set opa 2
set reg 15
set din 7
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x1
expect bank 0x0
set opr 8
set opa 3
set reg 11
set din 6
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 8
set opa 4
set reg 11
set din 5
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x4
expect carry 0x1
expect bank 0x0
set opr 8
set opa 5
set reg 7
set din 3
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x1
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 8
set opa 6
set reg 0
set din 9
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 8
set opa 7
set reg 12
set din 14
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 8
set opa 8
set reg 8
set din 3
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 8
set opa 9
set reg 8
set din 6
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 8
set opa 10
set reg 2
set din 5
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 8
set opa 11
set reg 0
set din 12
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 8
set opa 12
set reg 3
set din 10
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 8
set opa 13
set reg 4
set din 6
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 8
set opa 14
set reg 10
set din 7
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 8
set opa 15
set reg 10
set din 3
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 9
set opa 0
set reg 1
set din 4
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x6
expect carry 0x1
expect bank 0x0
set opr 9
set opa 1
set reg 7
set din 10
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 9
set opa 2
set reg 11
set din 12
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 9
set opa 3
set reg 5
set din 11
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 9
set opa 4
set reg 0
set din 4
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 9
set opa 5
set reg 2
set din 0
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 9
set opa 6
set reg 12
set din 8
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 9
set opa 7
set reg 7
set din 0
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x1
expect bank 0x0
set opr 9
set opa 8
set reg 3
set din 5
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x1
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 9
set opa 9
set reg 10
set din 8
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 9
set opa 10
set reg 2
set din 0
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x1
expect bank 0x0
set opr 9
set opa 11
set reg 2
set din 4
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x1
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 9
set opa 12
set reg 5
set din 5
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 9
set opa 13
set reg 6
set din 15
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x1
expect bank 0x0
set opr 9
set opa 14
set reg 10
set din 1
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 9
set opa 15
set reg 13
set din 15
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 10
set opa 0
set reg 1
set din 6
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 10
set opa 1
set reg 2
set din 1
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 10
set opa 2
set reg 12
set din 11
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 10
set opa 3
set reg 9
set din 6
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 10
set opa 4
set reg 12
set din 4
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 10
set opa 5
set reg 13
set din 3
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 10
set opa 6
set reg 5
set din 0
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 10
set opa 7
set reg 13
set din 11
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 10
set opa 8
set reg 3
set din 12
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 10
set opa 9
set reg 1
set din 10
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 10
set opa 10
set reg 12
set din 3
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 10
set opa 11
set reg 12
set din 0
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 10
set opa 12
set reg 6
set din 3
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 10
set opa 13
set reg 7
set din 3
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 10
set opa 14
set reg 6
set din 13
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 10
set opa 15
set reg 6
set din 12
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 11
set opa 0
set reg 13
set din 3
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 11
set opa 1
set reg 13
set din 11
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 11
set opa 2
set reg 7
set din 2
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 11
set opa 3
set reg 14
set din 5
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 11
set opa 4
set reg 7
set din 3
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 11
set opa 5
set reg 6
set din 3
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 11
set opa 6
set reg 9
set din 14
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 11
set opa 7
set reg 1
set din 4
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 11
set opa 8
set reg 6
set din 12
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 11
set opa 9
set reg 0
set din 2
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 11
set opa 10
set reg 12
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 11
set opa 11
set reg 11
set din 15
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 11
set opa 12
set reg 8
set din 9
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 11
set opa 13
set reg 2
set din 4
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 11
set opa 14
set reg 7
set din 6
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 11
set opa 15
set reg 2
set din 10
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 12
set opa 0
set reg 1
set din 12
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 12
set opa 1
set reg 15
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 12
set opa 2
set reg 9
set din 4
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 12
set opa 3
set reg 11
set din 0
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 12
set opa 4
set reg 15
set din 13
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 12
set opa 5
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 12
set opa 6
set reg 6
set din 15
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 12
set opa 7
set reg 7
set din 10
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 12
set opa 8
set reg 9
set din 7
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 12
set opa 9
set reg 6
set din 11
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 12
set opa 10
set reg 0
set din 10
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 12
set opa 11
set reg 12
set din 9
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 12
set opa 12
set reg 12
set din 4
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 12
set opa 13
set reg 10
set din 2
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 12
set opa 14
set reg 1
set din 2
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 12
set opa 15
set reg 14
set din 8
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 13
set opa 0
set reg 0
set din 9
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 13
set opa 1
set reg 12
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 13
set opa 2
set reg 0
set din 4
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 13
set opa 3
set reg 9
set din 1
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 13
set opa 4
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 13
set opa 5
set reg 13
set din 6
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 13
set opa 6
set reg 10
set din 10
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 13
set opa 7
set reg 14
set din 11
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 13
set opa 8
set reg 10
set din 5
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 13
set opa 9
set reg 8
set din 12
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 13
set opa 10
set reg 15
set din 15
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 13
set opa 11
set reg 2
set din 10
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 13
set opa 12
set reg 4
set din 12
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 13
set opa 13
set reg 8
set din 3
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 13
set opa 14
set reg 5
set din 13
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 13
set opa 15
set reg 9
set din 5
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 0
set reg 2
set din 8
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 1
set reg 0
set din 13
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 2
set reg 7
set din 0
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 3
set reg 4
set din 10
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 4
set reg 6
set din 2
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 5
set reg 2
set din 5
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 6
set reg 1
set din 13
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 7
set reg 15
set din 13
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 6
set din 8
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x1
expect bank 0x0
set opr 14
set opa 9
set reg 0
set din 8
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 14
set opa 10
set reg 3
set din 3
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 14
set opa 11
set reg 3
set din 0
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 14
set opa 12
set reg 3
set din 5
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 14
set opa 13
set reg 11
set din 8
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 14
set opa 14
set reg 5
set din 12
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 14
set opa 15
set reg 7
set din 15
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 15
set opa 0
set reg 10
set din 7
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 13
set opa 9
set reg 0
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 15
set opa 1
set reg 8
set din 2
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 15
set opa 2
set reg 12
set din 12
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 15
set opa 3
set reg 6
set din 9
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 15
set opa 4
set reg 4
set din 1
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0x5
expect carry 0x1
expect bank 0x0
set opr 15
set opa 5
set reg 6
set din 2
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 15
set opa 6
set reg 1
set din 9
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x1
expect bank 0x0
set opr 15
set opa 7
set reg 2
set din 13
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 15
set opa 8
set reg 6
set din 7
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 15
set opa 9
set reg 10
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 15
set opa 10
set reg 13
set din 4
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 15
set opa 11
set reg 6
set din 10
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 15
set opa 12
set reg 11
set din 4
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 15
set opa 13
set reg 8
set din 10
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 15
set opa 14
set reg 0
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 15
set opa 15
set reg 2
set din 12
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
// Random instructions; write at 0 now and then, reset rarely.
set opr 15
set opa 13
set reg 3
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 15
set opa 10
set reg 1
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 6
set opa 4
set reg 5
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 12
set opa 8
set reg 1
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 13
set opa 7
set reg 12
set din 7
set write 1
set reset 1
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 15
set reg 0
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 0
set opa 14
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 14
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 8
set opa 14
set reg 6
set din 9
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 12
set opa 3
set reg 13
set din 7
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 11
set opa 1
set reg 4
set din 7
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0x4
expect carry 0x1
expect bank 0x0
set opr 0
set opa 13
set reg 2
set din 15
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x1
expect bank 0x0
tock
expect acc 0x4
expect carry 0x1
expect bank 0x0
set opr 10
set opa 5
set reg 13
set din 10
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 9
set opa 9
set reg 8
set din 2
set write 1
set reset 1
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 11
set opa 2
set reg 7
set din 2
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 8
set opa 10
set reg 10
set din 6
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 3
set opa 3
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 10
set opa 9
set reg 9
set din 3
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x1
expect bank 0x0
set opr 15
set opa 1
set reg 10
set din 8
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 14
set opa 7
set reg 1
set din 2
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 15
set opa 2
set reg 15
set din 14
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 8
set opa 5
set reg 0
set din 13
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 12
set opa 9
set reg 1
set din 7
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 14
set opa 9
set reg 15
set din 15
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 12
set opa 14
set reg 0
set din 11
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 15
set opa 0
set reg 0
set din 12
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 12
set opa 12
set reg 5
set din 1
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 10
set opa 3
set reg 12
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 10
set opa 10
set reg 2
set din 3
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 14
set opa 5
set reg 8
set din 5
set write 0
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 14
set opa 15
set reg 13
set din 13
set write 0
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 15
set opa 13
set reg 3
set din 0
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x2
set opr 15
set opa 14
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x2
tock
expect acc 0x2
expect carry 0x0
expect bank 0x2
set opr 14
set opa 6
set reg 15
set din 4
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x2
tock
expect acc 0x2
expect carry 0x0
expect bank 0x2
set opr 13
set opa 4
set reg 11
set din 6
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x2
tock
expect acc 0x4
expect carry 0x0
expect bank 0x2
set opr 11
set opa 6
set reg 10
set din 11
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x2
tock
expect acc 0xA
expect carry 0x0
expect bank 0x2
set opr 15
set opa 10
set reg 0
set din 9
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x2
tock
expect acc 0xA
expect carry 0x1
expect bank 0x2
set opr 11
set opa 3
set reg 0
set din 3
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x2
tock
expect acc 0x0
expect carry 0x1
expect bank 0x2
set opr 15
set opa 11
set reg 7
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x2
tock
expect acc 0x6
expect carry 0x1
expect bank 0x2
set opr 8
set opa 12
set reg 3
set din 7
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x1
expect bank 0x2
tock
expect acc 0xA
expect carry 0x0
expect bank 0x2
set opr 9
set opa 2
set reg 11
set din 5
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x2
tock
expect acc 0xF
expect carry 0x0
expect bank 0x2
set opr 8
set opa 5
set reg 2
set din 0
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x2
tock
expect acc 0x1
expect carry 0x1
expect bank 0x2
set opr 10
set opa 4
set reg 0
set din 3
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x2
tock
expect acc 0x0
expect carry 0x1
expect bank 0x2
set opr 9
set opa 11
set reg 5
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x2
tock
expect acc 0xA
expect carry 0x0
expect bank 0x2
set opr 3
set opa 15
set reg 6
set din 15
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x2
tock
expect acc 0xA
expect carry 0x0
expect bank 0x2
set opr 14
set opa 14
set reg 0
set din 12
set write 1
set reset 1
tick
expect acc 0xA
expect carry 0x0
expect bank 0x2
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 14
set opa 6
set reg 2
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 14
set opa 2
set reg 4
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 5
set opa 14
set reg 13
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 9
set reg 0
set din 15
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 6
set din 13
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 11
set opa 7
set reg 13
set din 6
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 14
set opa 5
set reg 14
set din 7
set write 1
set reset 1
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 15
set opa 12
set reg 5
set din 7
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 11
set opa 9
set reg 7
set din 7
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 3
set opa 2
set reg 4
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 11
set opa 9
set reg 11
set din 11
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 13
set opa 1
set reg 3
set din 4
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 13
set opa 14
set reg 8
set din 10
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 15
set opa 8
set reg 1
set din 8
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 15
set opa 9
set reg 8
set din 14
set write 0
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 5
set opa 9
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 8
set opa 12
set reg 4
set din 9
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 4
set opa 15
set reg 10
set din 5
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 11
set opa 13
set reg 2
set din 10
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 10
set opa 10
set reg 12
set din 2
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0xC
expect carry 0x1
expect bank 0x0
set opr 15
set opa 12
set reg 6
set din 8
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x1
expect bank 0x0
tock
expect acc 0xF
expect carry 0x1
expect bank 0x0
set opr 15
set opa 8
set reg 4
set din 11
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 11
set opa 12
set reg 14
set din 9
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 10
set opa 12
set reg 1
set din 9
set write 0
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 10
set opa 12
set reg 5
set din 1
set write 0
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 9
set opa 8
set reg 3
set din 3
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 14
set opa 7
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 10
set opa 13
set reg 2
set din 15
set write 0
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 15
set opa 7
set reg 7
set din 7
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 8
set opa 11
set reg 6
set din 12
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 8
set opa 4
set reg 5
set din 14
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 12
set opa 8
set reg 14
set din 11
set write 0
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 14
set opa 12
set reg 6
set din 10
set write 0
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 0
set opa 7
set reg 10
set din 9
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 11
set opa 6
set reg 9
set din 7
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 12
set opa 13
set reg 7
set din 12
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 15
set opa 14
set reg 2
set din 5
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 7
set opa 2
set reg 13
set din 13
set write 0
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 12
set opa 0
set reg 11
set din 5
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 15
set reg 6
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 11
set opa 7
set reg 14
set din 10
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 15
set opa 11
set reg 14
set din 5
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x1
expect bank 0x0
set opr 11
set opa 7
set reg 14
set din 0
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 15
set opa 9
set reg 0
set din 1
set write 0
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 8
set opa 5
set reg 12
set din 3
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 5
set opa 10
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 14
set opa 2
set reg 1
set din 5
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 10
set opa 6
set reg 15
set din 9
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xF
expect carry 0x1
expect bank 0x0
set opr 9
set opa 13
set reg 13
set din 1
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 2
set opa 6
set reg 8
set din 11
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 15
set opa 14
set reg 6
set din 14
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 14
set opa 15
set reg 0
set din 11
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 15
set opa 4
set reg 4
set din 15
set write 0
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 9
set opa 15
set reg 0
set din 14
set write 0
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 9
set opa 14
set reg 10
set din 8
set write 0
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 8
set opa 14
set reg 1
set din 9
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 12
set opa 7
set reg 15
set din 9
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 15
set opa 6
set reg 15
set din 2
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 15
set opa 4
set reg 8
set din 11
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0xC
expect carry 0x1
expect bank 0x0
set opr 11
set opa 10
set reg 9
set din 0
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x1
expect bank 0x0
set opr 8
set opa 10
set reg 15
set din 8
set write 0
set reset 0
tick
expect acc 0x9
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x1
expect bank 0x0
set opr 15
set opa 9
set reg 8
set din 9
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 13
set opa 12
set reg 13
set din 15
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 14
set opa 4
set reg 6
set din 3
set write 1
set reset 1
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 6
set opa 0
set reg 10
set din 2
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 10
set opa 6
set reg 5
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 1
set opa 1
set reg 4
set din 1
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 10
set opa 15
set reg 12
set din 2
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 15
set opa 4
set reg 0
set din 1
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 7
set opa 14
set reg 3
set din 5
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 11
set opa 4
set reg 10
set din 15
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 11
set opa 2
set reg 9
set din 3
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 10
set opa 2
set reg 10
set din 9
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 11
set opa 7
set reg 4
set din 13
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 14
set opa 6
set reg 3
set din 15
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 8
set opa 6
set reg 4
set din 7
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 11
set opa 2
set reg 3
set din 3
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 15
set opa 7
set reg 7
set din 7
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 13
set opa 7
set reg 15
set din 3
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 7
set reg 5
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 12
set opa 1
set reg 1
set din 15
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 11
set opa 4
set reg 5
set din 11
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 4
set opa 8
set reg 4
set din 8
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 15
set opa 5
set reg 8
set din 10
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 9
set opa 13
set reg 7
set din 0
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 15
set opa 10
set reg 8
set din 1
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 8
set opa 4
set reg 15
set din 7
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0x3
expect carry 0x1
expect bank 0x0
set opr 9
set opa 3
set reg 8
set din 5
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 11
set opa 9
set reg 6
set din 6
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 8
set opa 3
set reg 4
set din 6
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 9
set opa 10
set reg 0
set din 13
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 10
set opa 10
set reg 12
set din 2
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0xC
expect carry 0x1
expect bank 0x0
set opr 15
set opa 11
set reg 9
set din 13
set write 1
set reset 1
tick
expect acc 0xC
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 15
set opa 3
set reg 1
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 14
set opa 12
set reg 10
set din 10
set write 1
set reset 1
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 15
set opa 9
set reg 9
set din 5
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 12
set opa 0
set reg 13
set din 11
set write 0
set reset 1
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 9
set opa 2
set reg 11
set din 7
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 10
set opa 5
set reg 12
set din 9
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 0
set opa 7
set reg 3
set din 2
set write 0
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 10
set opa 7
set reg 2
set din 0
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 8
set opa 14
set reg 13
set din 6
set write 0
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 11
set opa 4
set reg 7
set din 8
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 12
set opa 14
set reg 14
set din 3
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 11
set opa 3
set reg 1
set din 3
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 15
set opa 4
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 9
set opa 10
set reg 5
set din 8
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x1
expect bank 0x0
set opr 13
set opa 11
set reg 10
set din 3
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 15
set opa 10
set reg 11
set din 4
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xB
expect carry 0x1
expect bank 0x0
set opr 15
set opa 8
set reg 2
set din 6
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 15
set opa 10
set reg 12
set din 11
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0xA
expect carry 0x1
expect bank 0x0
set opr 8
set opa 8
set reg 13
set din 13
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 14
set opa 2
set reg 9
set din 7
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 10
set opa 5
set reg 11
set din 2
set write 0
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 3
set opa 6
set reg 8
set din 15
set write 0
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 15
set opa 2
set reg 14
set din 12
set write 0
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0x8
expect carry 0x1
expect bank 0x0
set opr 15
set opa 11
set reg 1
set din 12
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 15
set opa 1
set reg 5
set din 2
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 13
set opa 8
set reg 2
set din 0
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 12
set opa 8
set reg 4
set din 3
set write 0
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 14
set opa 15
set reg 8
set din 4
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 14
set opa 5
set reg 12
set din 6
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 10
set opa 8
set reg 8
set din 11
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 11
set opa 11
set reg 6
set din 9
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 10
set opa 9
set reg 14
set din 9
set write 0
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 10
set opa 7
set reg 3
set din 5
set write 0
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 15
set opa 11
set reg 9
set din 12
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 3
set opa 1
set reg 15
set din 7
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 3
set opa 2
set reg 10
set din 13
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 14
set opa 12
set reg 7
set din 12
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 12
set opa 4
set reg 4
set din 3
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 13
set opa 10
set reg 4
set din 9
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 14
set opa 0
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 12
set opa 7
set reg 2
set din 11
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 14
set opa 6
set reg 4
set din 15
set write 1
set reset 1
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 4
set opa 6
set reg 4
set din 13
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 9
set opa 9
set reg 6
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 14
set opa 10
set reg 3
set din 4
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 14
set opa 5
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 2
set opa 6
set reg 15
set din 13
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 10
set opa 10
set reg 4
set din 7
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 8
set opa 11
set reg 2
set din 8
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 1
set opa 4
set reg 1
set din 13
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 12
set opa 13
set reg 0
set din 15
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 14
set opa 15
set reg 11
set din 10
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 6
set opa 4
set reg 7
set din 15
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 14
set opa 15
set reg 5
set din 9
set write 0
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 2
set opa 6
set reg 3
set din 14
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 11
set opa 14
set reg 9
set din 10
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 14
set opa 9
set reg 4
set din 10
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 9
set opa 13
set reg 3
set din 5
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x1
expect bank 0x0
set opr 15
set opa 5
set reg 2
set din 5
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x1
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 15
set opa 3
set reg 10
set din 0
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x1
expect bank 0x0
set opr 15
set opa 8
set reg 6
set din 2
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 8
set opa 0
set reg 10
set din 0
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x1
expect bank 0x0
set opr 15
set opa 3
set reg 12
set din 12
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 12
set opa 14
set reg 8
set din 2
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 10
set opa 15
set reg 6
set din 14
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 12
set din 9
set write 0
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 15
set opa 2
set reg 13
set din 15
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 8
set opa 4
set reg 9
set din 12
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 8
set opa 5
set reg 4
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 15
set opa 5
set reg 3
set din 14
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0xA
expect carry 0x0
expect bank 0x0
set opr 15
set opa 7
set reg 5
set din 1
set write 1
set reset 0
tick
expect acc 0xA
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 13
set opa 3
set reg 3
set din 6
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 12
set opa 10
set reg 13
set din 7
set write 0
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 14
set opa 7
set reg 1
set din 15
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 12
set opa 12
set reg 5
set din 0
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 15
set opa 15
set reg 8
set din 5
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 11
set opa 8
set reg 1
set din 8
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 15
set opa 2
set reg 15
set din 0
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 15
set opa 12
set reg 7
set din 3
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 9
set opa 14
set reg 13
set din 8
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 15
set opa 4
set reg 8
set din 9
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 2
set din 7
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x1
expect bank 0x0
set opr 11
set opa 2
set reg 7
set din 6
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x1
expect bank 0x0
tock
expect acc 0x7
expect carry 0x1
expect bank 0x0
set opr 15
set opa 8
set reg 3
set din 15
set write 0
set reset 0
tick
expect acc 0x7
expect carry 0x1
expect bank 0x0
tock
expect acc 0x7
expect carry 0x1
expect bank 0x0
set opr 15
set opa 10
set reg 14
set din 12
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x1
expect bank 0x0
tock
expect acc 0x7
expect carry 0x1
expect bank 0x0
set opr 11
set opa 1
set reg 12
set din 13
set write 1
set reset 1
tick
expect acc 0x7
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 9
set opa 0
set reg 11
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 14
set opa 14
set reg 8
set din 4
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 10
set opa 8
set reg 8
set din 10
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 12
set opa 13
set reg 9
set din 6
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 8
set opa 10
set reg 5
set din 3
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 9
set opa 12
set reg 13
set din 14
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 15
set opa 6
set reg 14
set din 2
set write 1
set reset 1
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 12
set opa 12
set reg 14
set din 8
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 13
set opa 9
set reg 8
set din 10
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 13
set opa 1
set reg 3
set din 1
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 4
set opa 10
set reg 12
set din 8
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 14
set opa 3
set reg 14
set din 14
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 5
set opa 2
set reg 3
set din 3
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 8
set opa 3
set reg 2
set din 3
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 12
set opa 8
set reg 14
set din 4
set write 1
set reset 0
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x8
expect carry 0x0
expect bank 0x0
set opr 12
set opa 15
set reg 0
set din 3
set write 1
set reset 0
tick
expect acc 0x8
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 11
set opa 6
set reg 11
set din 9
set write 0
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 14
set opa 4
set reg 12
set din 4
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 8
set opa 3
set reg 1
set din 10
set write 0
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 9
set opa 0
set reg 2
set din 7
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 15
set opa 13
set reg 9
set din 15
set write 0
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 10
set opa 6
set reg 13
set din 8
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 10
set opa 3
set reg 11
set din 3
set write 0
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 14
set opa 5
set reg 0
set din 4
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 2
set opa 6
set reg 6
set din 12
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xD
expect carry 0x1
expect bank 0x0
set opr 15
set opa 6
set reg 9
set din 15
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x1
expect bank 0x0
tock
expect acc 0xE
expect carry 0x1
expect bank 0x0
set opr 15
set opa 7
set reg 7
set din 1
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 2
set din 1
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 12
set opa 3
set reg 0
set din 7
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x3
expect carry 0x0
expect bank 0x0
set opr 14
set opa 3
set reg 4
set din 12
set write 1
set reset 1
tick
expect acc 0x3
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 5
set reg 4
set din 0
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 11
set opa 2
set reg 14
set din 14
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 15
set opa 14
set reg 2
set din 4
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 10
set opa 6
set reg 6
set din 15
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 15
set opa 2
set reg 8
set din 7
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 2
set opa 4
set reg 0
set din 9
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 14
set opa 3
set reg 10
set din 9
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0x7
expect carry 0x0
expect bank 0x0
set opr 15
set opa 12
set reg 4
set din 13
set write 1
set reset 0
tick
expect acc 0x7
expect carry 0x0
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
set opr 12
set opa 5
set reg 12
set din 13
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 15
set opa 7
set reg 14
set din 1
set write 0
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 14
set opa 5
set reg 4
set din 15
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0x5
expect carry 0x0
expect bank 0x0
set opr 9
set opa 1
set reg 9
set din 4
set write 1
set reset 0
tick
expect acc 0x5
expect carry 0x0
expect bank 0x0
tock
expect acc 0xC
expect carry 0x0
expect bank 0x0
set opr 12
set opa 1
set reg 2
set din 6
set write 1
set reset 0
tick
expect acc 0xC
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 13
set opa 5
set reg 12
set din 0
set write 0
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x1
expect carry 0x0
expect bank 0x0
set opr 14
set opa 15
set reg 10
set din 2
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 4
set opa 14
set reg 0
set din 1
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 8
set opa 7
set reg 4
set din 11
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 14
set opa 7
set reg 1
set din 14
set write 0
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 14
set opa 7
set reg 1
set din 10
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x0
expect bank 0x0
set opr 8
set opa 4
set reg 8
set din 7
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x0
expect bank 0x0
tock
expect acc 0xE
expect carry 0x0
expect bank 0x0
set opr 14
set opa 13
set reg 9
set din 4
set write 1
set reset 0
tick
expect acc 0xE
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 11
set opa 13
set reg 15
set din 15
set write 0
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x0
expect bank 0x0
set opr 15
set opa 10
set reg 8
set din 15
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x0
expect bank 0x0
tock
expect acc 0x4
expect carry 0x1
expect bank 0x0
set opr 15
set opa 5
set reg 2
set din 0
set write 1
set reset 0
tick
expect acc 0x4
expect carry 0x1
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 15
set opa 3
set reg 1
set din 11
set write 0
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 11
set opa 6
set reg 11
set din 15
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 2
set opa 12
set reg 9
set din 9
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 13
set opa 0
set reg 6
set din 6
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 14
set opa 8
set reg 3
set din 0
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 12
set opa 1
set reg 9
set din 15
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x1
expect bank 0x0
set opr 14
set opa 3
set reg 2
set din 1
set write 1
set reset 1
tick
expect acc 0x0
expect carry 0x1
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 1
set reg 7
set din 14
set write 0
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x0
expect carry 0x0
expect bank 0x0
set opr 8
set opa 11
set reg 9
set din 3
set write 1
set reset 0
tick
expect acc 0x0
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 15
set opa 15
set reg 5
set din 8
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 14
set opa 14
set reg 14
set din 12
set write 0
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 0
set opa 2
set reg 10
set din 6
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x9
expect carry 0x0
expect bank 0x0
set opr 12
set opa 2
set reg 12
set din 2
set write 1
set reset 0
tick
expect acc 0x9
expect carry 0x0
expect bank 0x0
tock
expect acc 0x2
expect carry 0x0
expect bank 0x0
set opr 11
set opa 15
set reg 13
set din 14
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 9
set opa 12
set reg 11
set din 0
set write 0
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xD
expect carry 0x0
expect bank 0x0
set opr 10
set opa 0
set reg 11
set din 9
set write 1
set reset 0
tick
expect acc 0xD
expect carry 0x0
expect bank 0x0
tock
expect acc 0xB
expect carry 0x0
expect bank 0x0
set opr 8
set opa 13
set reg 11
set din 8
set write 1
set reset 0
tick
expect acc 0xB
expect carry 0x0
expect bank 0x0
tock
expect acc 0x6
expect carry 0x1
expect bank 0x0
set opr 9
set opa 9
set reg 3
set din 12
set write 1
set reset 0
tick
expect acc 0x6
expect carry 0x1
expect bank 0x0
tock
expect acc 0x2
expect carry 0x1
expect bank 0x0
set opr 8
set opa 4
set reg 14
set din 6
set write 1
set reset 0
tick
expect acc 0x2
expect carry 0x1
expect bank 0x0
tock
expect acc 0x1
expect carry 0x1
expect bank 0x0
set opr 14
set opa 10
set reg 13
set din 15
set write 1
set reset 0
tick
expect acc 0x1
expect carry 0x1
expect bank 0x0
tock
expect acc 0xF
expect carry 0x1
expect bank 0x0
set opr 15
set opa 3
set reg 13
set din 14
set write 1
set reset 0
tick
expect acc 0xF
expect carry 0x1
expect bank 0x0
tock
expect acc 0xF
expect carry 0x0
expect bank 0x0
