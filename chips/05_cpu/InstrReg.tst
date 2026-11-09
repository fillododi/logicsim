// InstrReg: OPR at M1 (period 3) and OPA at M2 (period 4), or the second word into
// data when second is 1. Every cycle puts a new digit on din, so a load at any other
// period shows. Checked after each tick (old values) and each tock. Generated from a
// model, seed 4004.
chip InstrReg
// One-word instructions, then a two-word one, in period order as Timing runs.
set din 0xF
set period 0
set second 0
tick
expect opr *
expect opa *
expect data *
tock
expect opr *
expect opa *
expect data *
set din 0xB
set period 1
set second 0
tick
expect opr *
expect opa *
expect data *
tock
expect opr *
expect opa *
expect data *
set din 0xF
set period 2
set second 0
tick
expect opr *
expect opa *
expect data *
tock
expect opr *
expect opa *
expect data *
set din 0x1
set period 3
set second 0
tick
expect opr *
expect opa *
expect data *
tock
expect opr 0x1
expect opa *
expect data *
set din 0xC
set period 4
set second 0
tick
expect opr 0x1
expect opa *
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0x0
set period 5
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0xE
set period 6
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0x0
set period 7
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0x6
set period 0
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0x7
set period 1
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0x6
set period 2
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0x1
expect opa 0xC
expect data *
set din 0xA
set period 3
set second 0
tick
expect opr 0x1
expect opa 0xC
expect data *
tock
expect opr 0xA
expect opa 0xC
expect data *
set din 0x7
set period 4
set second 0
tick
expect opr 0xA
expect opa 0xC
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x0
set period 5
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x2
set period 6
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x6
set period 7
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x3
set period 0
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x6
set period 1
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x9
set period 2
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0xF
set period 3
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data *
set din 0x8
set period 4
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data *
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0x4
set period 5
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0x2
set period 6
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0x6
set period 7
set second 1
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0x4
set period 0
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0x1
set period 1
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0x6
set period 2
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xA
expect opa 0x7
expect data 0xF8
set din 0xE
set period 3
set second 0
tick
expect opr 0xA
expect opa 0x7
expect data 0xF8
tock
expect opr 0xE
expect opa 0x7
expect data 0xF8
set din 0x5
set period 4
set second 0
tick
expect opr 0xE
expect opa 0x7
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0xC
set period 5
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0x0
set period 6
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0x0
set period 7
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0xB
set period 0
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0x4
set period 1
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0x6
set period 2
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0xF8
set din 0x7
set period 3
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xF8
tock
expect opr 0xE
expect opa 0x5
expect data 0x78
set din 0xA
set period 4
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x78
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0xB
set period 5
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0xB
set period 6
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0xF
set period 7
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0x1
set period 0
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0x6
set period 1
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0x1
set period 2
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0x7A
set din 0xC
set period 3
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0x7A
tock
expect opr 0xE
expect opa 0x5
expect data 0xCA
set din 0xF
set period 4
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xCA
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0xA
set period 5
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0x9
set period 6
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0x9
set period 7
set second 1
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0x2
set period 0
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0xA
set period 1
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0x3
set period 2
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0xE
expect opa 0x5
expect data 0xCF
set din 0x7
set period 3
set second 0
tick
expect opr 0xE
expect opa 0x5
expect data 0xCF
tock
expect opr 0x7
expect opa 0x5
expect data 0xCF
set din 0xA
set period 4
set second 0
tick
expect opr 0x7
expect opa 0x5
expect data 0xCF
tock
expect opr 0x7
expect opa 0xA
expect data 0xCF
set din 0x4
set period 5
set second 0
tick
expect opr 0x7
expect opa 0xA
expect data 0xCF
tock
expect opr 0x7
expect opa 0xA
expect data 0xCF
set din 0xE
set period 6
set second 0
tick
expect opr 0x7
expect opa 0xA
expect data 0xCF
tock
expect opr 0x7
expect opa 0xA
expect data 0xCF
set din 0x3
set period 7
set second 0
tick
expect opr 0x7
expect opa 0xA
expect data 0xCF
tock
expect opr 0x7
expect opa 0xA
expect data 0xCF
// second changing between M1 and M2: each digit follows second at its own period.
set din 0xE
set period 3
set second 0
tick
expect opr 0x7
expect opa 0xA
expect data 0xCF
tock
expect opr 0xE
expect opa 0xA
expect data 0xCF
set din 0x5
set period 4
set second 1
tick
expect opr 0xE
expect opa 0xA
expect data 0xCF
tock
expect opr 0xE
expect opa 0xA
expect data 0xC5
set din 0x7
set period 3
set second 1
tick
expect opr 0xE
expect opa 0xA
expect data 0xC5
tock
expect opr 0xE
expect opa 0xA
expect data 0x75
set din 0x4
set period 4
set second 0
tick
expect opr 0xE
expect opa 0xA
expect data 0x75
tock
expect opr 0xE
expect opa 0x4
expect data 0x75
// Random periods and second.
set din 0xF
set period 0
set second 1
tick
expect opr 0xE
expect opa 0x4
expect data 0x75
tock
expect opr 0xE
expect opa 0x4
expect data 0x75
set din 0x3
set period 1
set second 0
tick
expect opr 0xE
expect opa 0x4
expect data 0x75
tock
expect opr 0xE
expect opa 0x4
expect data 0x75
set din 0x6
set period 0
set second 1
tick
expect opr 0xE
expect opa 0x4
expect data 0x75
tock
expect opr 0xE
expect opa 0x4
expect data 0x75
set din 0xB
set period 6
set second 0
tick
expect opr 0xE
expect opa 0x4
expect data 0x75
tock
expect opr 0xE
expect opa 0x4
expect data 0x75
set din 0xC
set period 4
set second 1
tick
expect opr 0xE
expect opa 0x4
expect data 0x75
tock
expect opr 0xE
expect opa 0x4
expect data 0x7C
set din 0xB
set period 6
set second 0
tick
expect opr 0xE
expect opa 0x4
expect data 0x7C
tock
expect opr 0xE
expect opa 0x4
expect data 0x7C
set din 0x0
set period 4
set second 0
tick
expect opr 0xE
expect opa 0x4
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x9
set period 5
set second 1
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x4
set period 1
set second 0
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x2
set period 0
set second 0
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x5
set period 2
set second 0
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x5
set period 2
set second 0
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0xF
set period 5
set second 0
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x4
set period 7
set second 1
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x7C
set din 0x5
set period 3
set second 1
tick
expect opr 0xE
expect opa 0x0
expect data 0x7C
tock
expect opr 0xE
expect opa 0x0
expect data 0x5C
set din 0x2
set period 3
set second 0
tick
expect opr 0xE
expect opa 0x0
expect data 0x5C
tock
expect opr 0x2
expect opa 0x0
expect data 0x5C
set din 0xB
set period 3
set second 0
tick
expect opr 0x2
expect opa 0x0
expect data 0x5C
tock
expect opr 0xB
expect opa 0x0
expect data 0x5C
set din 0x6
set period 3
set second 1
tick
expect opr 0xB
expect opa 0x0
expect data 0x5C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0x2
set period 5
set second 1
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0xA
set period 7
set second 1
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0xF
set period 5
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0x1
set period 5
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0x9
set period 2
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0x5
set period 1
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0x5
set period 7
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0x5
set period 1
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0x0
expect data 0x6C
set din 0xE
set period 4
set second 0
tick
expect opr 0xB
expect opa 0x0
expect data 0x6C
tock
expect opr 0xB
expect opa 0xE
expect data 0x6C
set din 0x1
set period 5
set second 0
tick
expect opr 0xB
expect opa 0xE
expect data 0x6C
tock
expect opr 0xB
expect opa 0xE
expect data 0x6C
set din 0x8
set period 6
set second 1
tick
expect opr 0xB
expect opa 0xE
expect data 0x6C
tock
expect opr 0xB
expect opa 0xE
expect data 0x6C
set din 0x4
set period 1
set second 0
tick
expect opr 0xB
expect opa 0xE
expect data 0x6C
tock
expect opr 0xB
expect opa 0xE
expect data 0x6C
set din 0xA
set period 7
set second 1
tick
expect opr 0xB
expect opa 0xE
expect data 0x6C
tock
expect opr 0xB
expect opa 0xE
expect data 0x6C
set din 0xF
set period 4
set second 0
tick
expect opr 0xB
expect opa 0xE
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0xA
set period 6
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x0
set period 1
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x8
set period 1
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x5
set period 5
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0xE
set period 7
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x2
set period 7
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x3
set period 2
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0xE
set period 1
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x9
set period 5
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x4
set period 5
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x2
set period 1
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x1
set period 2
set second 1
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x5
set period 7
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0xF
expect data 0x6C
set din 0x4
set period 4
set second 0
tick
expect opr 0xB
expect opa 0xF
expect data 0x6C
tock
expect opr 0xB
expect opa 0x4
expect data 0x6C
set din 0x1
set period 5
set second 1
tick
expect opr 0xB
expect opa 0x4
expect data 0x6C
tock
expect opr 0xB
expect opa 0x4
expect data 0x6C
set din 0x0
set period 4
set second 1
tick
expect opr 0xB
expect opa 0x4
expect data 0x6C
tock
expect opr 0xB
expect opa 0x4
expect data 0x60
set din 0x7
set period 6
set second 1
tick
expect opr 0xB
expect opa 0x4
expect data 0x60
tock
expect opr 0xB
expect opa 0x4
expect data 0x60
set din 0xD
set period 3
set second 0
tick
expect opr 0xB
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0x1
set period 5
set second 0
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0xF
set period 6
set second 1
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0xE
set period 7
set second 0
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0x2
set period 0
set second 0
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0x7
set period 6
set second 0
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0x8
set period 0
set second 1
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0x9
set period 7
set second 1
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0xA
set period 0
set second 1
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0x1
set period 6
set second 0
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xD
expect opa 0x4
expect data 0x60
set din 0xC
set period 3
set second 0
tick
expect opr 0xD
expect opa 0x4
expect data 0x60
tock
expect opr 0xC
expect opa 0x4
expect data 0x60
set din 0x3
set period 0
set second 1
tick
expect opr 0xC
expect opa 0x4
expect data 0x60
tock
expect opr 0xC
expect opa 0x4
expect data 0x60
set din 0x2
set period 7
set second 0
tick
expect opr 0xC
expect opa 0x4
expect data 0x60
tock
expect opr 0xC
expect opa 0x4
expect data 0x60
set din 0x3
set period 1
set second 1
tick
expect opr 0xC
expect opa 0x4
expect data 0x60
tock
expect opr 0xC
expect opa 0x4
expect data 0x60
set din 0xD
set period 4
set second 0
tick
expect opr 0xC
expect opa 0x4
expect data 0x60
tock
expect opr 0xC
expect opa 0xD
expect data 0x60
set din 0x3
set period 5
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x60
tock
expect opr 0xC
expect opa 0xD
expect data 0x60
set din 0xF
set period 6
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x60
tock
expect opr 0xC
expect opa 0xD
expect data 0x60
set din 0x5
set period 0
set second 0
tick
expect opr 0xC
expect opa 0xD
expect data 0x60
tock
expect opr 0xC
expect opa 0xD
expect data 0x60
set din 0x3
set period 4
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x60
tock
expect opr 0xC
expect opa 0xD
expect data 0x63
set din 0x7
set period 1
set second 0
tick
expect opr 0xC
expect opa 0xD
expect data 0x63
tock
expect opr 0xC
expect opa 0xD
expect data 0x63
set din 0x1
set period 5
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x63
tock
expect opr 0xC
expect opa 0xD
expect data 0x63
set din 0x7
set period 3
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x63
tock
expect opr 0xC
expect opa 0xD
expect data 0x73
set din 0x2
set period 3
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x73
tock
expect opr 0xC
expect opa 0xD
expect data 0x23
set din 0xA
set period 2
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x23
tock
expect opr 0xC
expect opa 0xD
expect data 0x23
set din 0x4
set period 7
set second 0
tick
expect opr 0xC
expect opa 0xD
expect data 0x23
tock
expect opr 0xC
expect opa 0xD
expect data 0x23
set din 0x8
set period 6
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x23
tock
expect opr 0xC
expect opa 0xD
expect data 0x23
set din 0x4
set period 4
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x23
tock
expect opr 0xC
expect opa 0xD
expect data 0x24
set din 0x0
set period 0
set second 0
tick
expect opr 0xC
expect opa 0xD
expect data 0x24
tock
expect opr 0xC
expect opa 0xD
expect data 0x24
set din 0x1
set period 7
set second 1
tick
expect opr 0xC
expect opa 0xD
expect data 0x24
tock
expect opr 0xC
expect opa 0xD
expect data 0x24
set din 0x7
set period 7
set second 0
tick
expect opr 0xC
expect opa 0xD
expect data 0x24
tock
expect opr 0xC
expect opa 0xD
expect data 0x24
set din 0x1
set period 3
set second 0
tick
expect opr 0xC
expect opa 0xD
expect data 0x24
tock
expect opr 0x1
expect opa 0xD
expect data 0x24
set din 0x8
set period 7
set second 1
tick
expect opr 0x1
expect opa 0xD
expect data 0x24
tock
expect opr 0x1
expect opa 0xD
expect data 0x24
set din 0xE
set period 3
set second 0
tick
expect opr 0x1
expect opa 0xD
expect data 0x24
tock
expect opr 0xE
expect opa 0xD
expect data 0x24
set din 0xB
set period 2
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x24
tock
expect opr 0xE
expect opa 0xD
expect data 0x24
set din 0x0
set period 1
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x24
tock
expect opr 0xE
expect opa 0xD
expect data 0x24
set din 0xA
set period 7
set second 0
tick
expect opr 0xE
expect opa 0xD
expect data 0x24
tock
expect opr 0xE
expect opa 0xD
expect data 0x24
set din 0xA
set period 4
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x24
tock
expect opr 0xE
expect opa 0xD
expect data 0x2A
set din 0x7
set period 5
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x2A
tock
expect opr 0xE
expect opa 0xD
expect data 0x2A
set din 0x4
set period 0
set second 0
tick
expect opr 0xE
expect opa 0xD
expect data 0x2A
tock
expect opr 0xE
expect opa 0xD
expect data 0x2A
set din 0xF
set period 5
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x2A
tock
expect opr 0xE
expect opa 0xD
expect data 0x2A
set din 0xF
set period 2
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x2A
tock
expect opr 0xE
expect opa 0xD
expect data 0x2A
set din 0x8
set period 0
set second 0
tick
expect opr 0xE
expect opa 0xD
expect data 0x2A
tock
expect opr 0xE
expect opa 0xD
expect data 0x2A
set din 0x6
set period 4
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x2A
tock
expect opr 0xE
expect opa 0xD
expect data 0x26
set din 0xA
set period 1
set second 0
tick
expect opr 0xE
expect opa 0xD
expect data 0x26
tock
expect opr 0xE
expect opa 0xD
expect data 0x26
set din 0x0
set period 6
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x26
tock
expect opr 0xE
expect opa 0xD
expect data 0x26
set din 0x8
set period 7
set second 1
tick
expect opr 0xE
expect opa 0xD
expect data 0x26
tock
expect opr 0xE
expect opa 0xD
expect data 0x26
set din 0xB
set period 2
set second 0
tick
expect opr 0xE
expect opa 0xD
expect data 0x26
tock
expect opr 0xE
expect opa 0xD
expect data 0x26
