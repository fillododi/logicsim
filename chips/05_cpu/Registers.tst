// Registers: reg and pair are register opa and its pair (pair 0 while readp0 is 1).
// With write at 1: XCH writes acc, INC and ISZ add one, in a first cycle; FIM and FIN
// write data to the pair in a second cycle. Reset clears all 16. readp0 and write are
// never 1 together. Random cycles with seed 4006, from a model.
chip Registers
// Before any reset the registers are unknown.
set opr 11
set opa 3
set acc 5
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg *
expect pair *
tick
expect reg *
expect pair *
tock
expect reg *
expect pair *
// Reset, then each register read, and written by XCH.
set opr 0
set opa 0
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 1
eval
expect reg *
expect pair *
tick
expect reg *
expect pair *
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 0
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 0
set acc 3
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x3
expect pair 0x30
set opr 10
set opa 1
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x30
tick
expect reg 0x0
expect pair 0x30
tock
expect reg 0x0
expect pair 0x30
set opr 11
set opa 1
set acc 10
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x30
tick
expect reg 0x0
expect pair 0x30
tock
expect reg 0xA
expect pair 0x3A
set opr 10
set opa 2
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 2
set acc 1
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x10
set opr 10
set opa 3
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x10
tick
expect reg 0x0
expect pair 0x10
tock
expect reg 0x0
expect pair 0x10
set opr 11
set opa 3
set acc 8
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x10
tick
expect reg 0x0
expect pair 0x10
tock
expect reg 0x8
expect pair 0x18
set opr 10
set opa 4
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 4
set acc 15
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xF
expect pair 0xF0
set opr 10
set opa 5
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xF0
tick
expect reg 0x0
expect pair 0xF0
tock
expect reg 0x0
expect pair 0xF0
set opr 11
set opa 5
set acc 6
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xF0
tick
expect reg 0x0
expect pair 0xF0
tock
expect reg 0x6
expect pair 0xF6
set opr 10
set opa 6
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 6
set acc 13
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xD
expect pair 0xD0
set opr 10
set opa 7
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xD0
tick
expect reg 0x0
expect pair 0xD0
tock
expect reg 0x0
expect pair 0xD0
set opr 11
set opa 7
set acc 4
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xD0
tick
expect reg 0x0
expect pair 0xD0
tock
expect reg 0x4
expect pair 0xD4
set opr 10
set opa 8
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 8
set acc 11
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xB
expect pair 0xB0
set opr 10
set opa 9
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xB0
tick
expect reg 0x0
expect pair 0xB0
tock
expect reg 0x0
expect pair 0xB0
set opr 11
set opa 9
set acc 2
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xB0
tick
expect reg 0x0
expect pair 0xB0
tock
expect reg 0x2
expect pair 0xB2
set opr 10
set opa 10
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 10
set acc 9
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x9
expect pair 0x90
set opr 10
set opa 11
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 11
set opa 11
set acc 0
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 10
set opa 12
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 12
set acc 7
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x7
expect pair 0x70
set opr 10
set opa 13
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x70
tick
expect reg 0x0
expect pair 0x70
tock
expect reg 0x0
expect pair 0x70
set opr 11
set opa 13
set acc 14
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x70
tick
expect reg 0x0
expect pair 0x70
tock
expect reg 0xE
expect pair 0x7E
set opr 10
set opa 14
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 14
set acc 5
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x5
expect pair 0x50
set opr 10
set opa 15
set acc 0
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x50
tick
expect reg 0x0
expect pair 0x50
tock
expect reg 0x0
expect pair 0x50
set opr 11
set opa 15
set acc 12
set data 0
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x50
tick
expect reg 0x0
expect pair 0x50
tock
expect reg 0xC
expect pair 0x5C
// Random instructions, first and second cycles, readp0 and reset now and then.
set opr 8
set opa 7
set acc 4
set data 46
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x4
expect pair 0xD4
tick
expect reg 0x4
expect pair 0xD4
tock
expect reg 0x4
expect pair 0xD4
set opr 3
set opa 4
set acc 14
set data 216
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xF
expect pair 0xF6
tick
expect reg 0xF
expect pair 0xF6
tock
expect reg 0xD
expect pair 0xD8
set opr 7
set opa 6
set acc 8
set data 72
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xD
expect pair 0xD4
tick
expect reg 0xD
expect pair 0xD4
tock
expect reg 0xE
expect pair 0xE4
set opr 2
set opa 1
set acc 8
set data 202
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x3A
tick
expect reg 0xA
expect pair 0x3A
tock
expect reg 0xA
expect pair 0x3A
set opr 4
set opa 0
set acc 6
set data 167
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 3
set opa 11
set acc 9
set data 193
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 4
set opa 12
set acc 5
set data 196
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x7E
tick
expect reg 0x7
expect pair 0x7E
tock
expect reg 0x7
expect pair 0x7E
set opr 10
set opa 10
set acc 7
set data 234
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x9
expect pair 0x90
set opr 6
set opa 0
set acc 13
set data 59
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 1
set opa 1
set acc 1
set data 249
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x3A
tick
expect reg 0xA
expect pair 0x3A
tock
expect reg 0xA
expect pair 0x3A
set opr 11
set opa 9
set acc 5
set data 87
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x2
expect pair 0xB2
tick
expect reg 0x2
expect pair 0xB2
tock
expect reg 0x5
expect pair 0xB5
set opr 3
set opa 0
set acc 0
set data 190
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 6
set opa 11
set acc 14
set data 125
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 3
set opa 13
set acc 2
set data 1
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0x7E
tick
expect reg 0xE
expect pair 0x7E
tock
expect reg 0xE
expect pair 0x7E
set opr 11
set opa 15
set acc 10
set data 147
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 6
set opa 5
set acc 3
set data 6
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x8
expect pair 0xD8
tick
expect reg 0x8
expect pair 0xD8
tock
expect reg 0x9
expect pair 0xD9
set opr 7
set opa 13
set acc 9
set data 228
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0x7E
tick
expect reg 0xE
expect pair 0x7E
tock
expect reg 0xE
expect pair 0x7E
set opr 10
set opa 5
set acc 8
set data 99
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xD9
tick
expect reg 0x9
expect pair 0xD9
tock
expect reg 0x9
expect pair 0xD9
set opr 3
set opa 6
set acc 14
set data 2
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0xE4
tick
expect reg 0xE
expect pair 0xE4
tock
expect reg 0x0
expect pair 0x02
set opr 7
set opa 2
set acc 7
set data 15
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x18
tick
expect reg 0x1
expect pair 0x18
tock
expect reg 0x1
expect pair 0x18
set opr 4
set opa 8
set acc 13
set data 90
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0xB
expect pair 0xB5
tick
expect reg 0xB
expect pair 0xB5
tock
expect reg 0xB
expect pair 0xB5
set opr 14
set opa 0
set acc 4
set data 101
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 3
set opa 14
set acc 9
set data 39
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x5
expect pair 0x5C
tick
expect reg 0x5
expect pair 0x5C
tock
expect reg 0x5
expect pair 0x5C
set opr 11
set opa 10
set acc 7
set data 229
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x7
expect pair 0x70
set opr 2
set opa 14
set acc 2
set data 255
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x5
expect pair 0x5C
tick
expect reg 0x5
expect pair 0x5C
tock
expect reg 0xF
expect pair 0xFF
set opr 2
set opa 9
set acc 10
set data 74
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x5
expect pair 0xB5
tick
expect reg 0x5
expect pair 0xB5
tock
expect reg 0x5
expect pair 0xB5
set opr 3
set opa 4
set acc 13
set data 33
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xD
expect pair 0xD9
tick
expect reg 0xD
expect pair 0xD9
tock
expect reg 0xD
expect pair 0xD9
set opr 4
set opa 4
set acc 1
set data 234
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xD
expect pair 0xD9
tick
expect reg 0xD
expect pair 0xD9
tock
expect reg 0xD
expect pair 0xD9
set opr 3
set opa 15
set acc 7
set data 173
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 6
set opa 6
set acc 2
set data 123
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x02
tick
expect reg 0x0
expect pair 0x02
tock
expect reg 0x0
expect pair 0x02
set opr 2
set opa 10
set acc 5
set data 65
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x70
tick
expect reg 0x7
expect pair 0x70
tock
expect reg 0x7
expect pair 0x70
set opr 3
set opa 7
set acc 5
set data 11
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x2
expect pair 0x02
tick
expect reg 0x2
expect pair 0x02
tock
expect reg 0x2
expect pair 0x02
set opr 3
set opa 7
set acc 12
set data 74
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x2
expect pair 0x02
tick
expect reg 0x2
expect pair 0x02
tock
expect reg 0x2
expect pair 0x02
set opr 6
set opa 10
set acc 11
set data 75
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x70
tick
expect reg 0x7
expect pair 0x70
tock
expect reg 0x8
expect pair 0x80
set opr 4
set opa 12
set acc 0
set data 63
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x7E
tick
expect reg 0x7
expect pair 0x7E
tock
expect reg 0x7
expect pair 0x7E
set opr 8
set opa 3
set acc 15
set data 86
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x8
expect pair 0x18
tick
expect reg 0x8
expect pair 0x18
tock
expect reg 0x8
expect pair 0x18
set opr 6
set opa 15
set acc 9
set data 77
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xF
expect pair 0xFF
tick
expect reg 0xF
expect pair 0xFF
tock
expect reg 0xF
expect pair 0xFF
set opr 2
set opa 1
set acc 13
set data 119
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x3A
tick
expect reg 0xA
expect pair 0x3A
tock
expect reg 0xA
expect pair 0x3A
set opr 3
set opa 11
set acc 12
set data 64
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x80
tick
expect reg 0x0
expect pair 0x80
tock
expect reg 0x0
expect pair 0x80
set opr 8
set opa 12
set acc 0
set data 161
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x7E
tick
expect reg 0x7
expect pair 0x7E
tock
expect reg 0x7
expect pair 0x7E
set opr 11
set opa 0
set acc 4
set data 199
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 3
set opa 12
set acc 3
set data 246
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x7E
tick
expect reg 0x7
expect pair 0x7E
tock
expect reg 0xF
expect pair 0xF6
set opr 2
set opa 5
set acc 4
set data 115
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xD9
tick
expect reg 0x9
expect pair 0xD9
tock
expect reg 0x9
expect pair 0xD9
set opr 3
set opa 14
set acc 4
set data 237
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xF
expect pair 0xFF
tick
expect reg 0xF
expect pair 0xFF
tock
expect reg 0xF
expect pair 0xFF
set opr 2
set opa 4
set acc 4
set data 191
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xD
expect pair 0xD9
tick
expect reg 0xD
expect pair 0xD9
tock
expect reg 0xB
expect pair 0xBF
set opr 3
set opa 4
set acc 3
set data 161
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xB
expect pair 0xBF
tick
expect reg 0xB
expect pair 0xBF
tock
expect reg 0xA
expect pair 0xA1
set opr 4
set opa 10
set acc 1
set data 9
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x8
expect pair 0x80
tick
expect reg 0x8
expect pair 0x80
tock
expect reg 0x8
expect pair 0x80
set opr 1
set opa 6
set acc 11
set data 253
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 11
set opa 13
set acc 11
set data 253
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x6
expect pair 0xF6
tick
expect reg 0x6
expect pair 0xF6
tock
expect reg 0x6
expect pair 0xF6
set opr 3
set opa 1
set acc 7
set data 25
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x3A
tick
expect reg 0xA
expect pair 0x3A
tock
expect reg 0xA
expect pair 0x3A
set opr 1
set opa 0
set acc 10
set data 136
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x3
expect pair 0x3A
set opr 10
set opa 13
set acc 10
set data 48
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x6
expect pair 0xF6
tick
expect reg 0x6
expect pair 0xF6
tock
expect reg 0x6
expect pair 0xF6
set opr 8
set opa 1
set acc 0
set data 49
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x3A
tick
expect reg 0xA
expect pair 0x3A
tock
expect reg 0xA
expect pair 0x3A
set opr 1
set opa 1
set acc 10
set data 216
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x3A
tick
expect reg 0xA
expect pair 0x3A
tock
expect reg 0xA
expect pair 0x3A
set opr 2
set opa 11
set acc 4
set data 109
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x80
tick
expect reg 0x0
expect pair 0x80
tock
expect reg 0x0
expect pair 0x80
set opr 3
set opa 14
set acc 10
set data 251
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xF
expect pair 0xFF
tick
expect reg 0xF
expect pair 0xFF
tock
expect reg 0xF
expect pair 0xFB
set opr 11
set opa 0
set acc 6
set data 90
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3A
tick
expect reg 0x3
expect pair 0x3A
tock
expect reg 0x6
expect pair 0x6A
set opr 8
set opa 13
set acc 14
set data 34
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x6
expect pair 0xF6
tick
expect reg 0x6
expect pair 0xF6
tock
expect reg 0x6
expect pair 0xF6
set opr 2
set opa 2
set acc 2
set data 56
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x18
tick
expect reg 0x1
expect pair 0x18
tock
expect reg 0x3
expect pair 0x38
set opr 4
set opa 1
set acc 0
set data 39
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0x6A
tick
expect reg 0xA
expect pair 0x6A
tock
expect reg 0xA
expect pair 0x6A
set opr 8
set opa 9
set acc 4
set data 138
set second 0
set write 1
set readp0 0
set reset 1
eval
expect reg 0x5
expect pair 0xB5
tick
expect reg 0x5
expect pair 0xB5
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 0
set acc 13
set data 147
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 15
set acc 11
set data 139
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 7
set acc 7
set data 247
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 5
set acc 6
set data 107
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 4
set opa 13
set acc 11
set data 41
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 13
set acc 15
set data 247
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 4
set opa 15
set acc 12
set data 207
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 2
set acc 1
set data 18
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 11
set acc 13
set data 255
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 15
set acc 0
set data 44
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 8
set acc 5
set data 105
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 0
set acc 15
set data 251
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 1
set acc 2
set data 182
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 11
set acc 8
set data 102
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 9
set acc 7
set data 125
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 10
set acc 7
set data 151
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 11
set acc 7
set data 97
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 12
set acc 13
set data 185
set second 1
set write 1
set readp0 0
set reset 1
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 15
set acc 11
set data 123
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 9
set acc 11
set data 225
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 5
set acc 6
set data 62
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 15
set acc 1
set data 29
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 15
set acc 9
set data 79
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 5
set acc 2
set data 210
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x01
set opr 6
set opa 6
set acc 10
set data 199
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x10
set opr 2
set opa 11
set acc 9
set data 253
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 9
set acc 0
set data 0
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 14
set acc 10
set data 6
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 0
set acc 4
set data 30
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 13
set acc 6
set data 70
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 11
set acc 14
set data 30
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xE
expect pair 0x0E
set opr 2
set opa 13
set acc 7
set data 121
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 12
set acc 5
set data 196
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 10
set acc 3
set data 50
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 2
set acc 8
set data 174
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x10
set opr 4
set opa 9
set acc 5
set data 184
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 10
set acc 5
set data 52
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x0E
tick
expect reg 0x0
expect pair 0x0E
tock
expect reg 0x0
expect pair 0x0E
set opr 8
set opa 12
set acc 5
set data 112
set second 0
set write 1
set readp0 0
set reset 1
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 12
set acc 9
set data 231
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x9
expect pair 0x90
set opr 1
set opa 12
set acc 1
set data 32
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x9
expect pair 0x90
set opr 1
set opa 8
set acc 5
set data 162
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 12
set acc 3
set data 204
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x9
expect pair 0x90
set opr 7
set opa 8
set acc 14
set data 239
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 3
set acc 14
set data 243
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 14
set acc 6
set data 180
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 7
set acc 15
set data 222
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 0
set acc 9
set data 149
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 12
set acc 8
set data 211
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 0
set acc 15
set data 171
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xA
expect pair 0xAB
set opr 4
set opa 10
set acc 5
set data 173
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 12
set acc 15
set data 67
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x9
expect pair 0x90
set opr 2
set opa 0
set acc 9
set data 42
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0xA
expect pair 0xAB
tick
expect reg 0xA
expect pair 0xAB
tock
expect reg 0xA
expect pair 0xAB
set opr 7
set opa 3
set acc 6
set data 115
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x01
set opr 2
set opa 0
set acc 11
set data 162
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0xAB
tick
expect reg 0xA
expect pair 0xAB
tock
expect reg 0xA
expect pair 0xA2
set opr 2
set opa 3
set acc 1
set data 195
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x01
tick
expect reg 0x1
expect pair 0x01
tock
expect reg 0x1
expect pair 0x01
set opr 3
set opa 2
set acc 1
set data 62
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x01
tick
expect reg 0x0
expect pair 0x01
tock
expect reg 0x3
expect pair 0x3E
set opr 7
set opa 10
set acc 6
set data 130
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 5
set acc 3
set data 79
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 0
set acc 2
set data 55
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0xA2
tick
expect reg 0xA
expect pair 0xA2
tock
expect reg 0xA
expect pair 0xA2
set opr 7
set opa 12
set acc 1
set data 72
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x9
expect pair 0x90
set opr 7
set opa 14
set acc 13
set data 1
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x10
set opr 7
set opa 0
set acc 9
set data 23
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0xA2
tick
expect reg 0xA
expect pair 0xA2
tock
expect reg 0xB
expect pair 0xB2
set opr 11
set opa 14
set acc 3
set data 31
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0xB
expect pair 0xB2
tick
expect reg 0xB
expect pair 0xB2
tock
expect reg 0xB
expect pair 0xB2
set opr 11
set opa 7
set acc 8
set data 149
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 12
set acc 9
set data 205
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x90
tick
expect reg 0x9
expect pair 0x90
tock
expect reg 0x9
expect pair 0x90
set opr 4
set opa 8
set acc 8
set data 228
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 5
set acc 11
set data 154
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0xB
expect pair 0xB2
tick
expect reg 0xB
expect pair 0xB2
tock
expect reg 0xB
expect pair 0xB2
set opr 11
set opa 4
set acc 0
set data 196
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 6
set acc 7
set data 62
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x3
expect pair 0x3E
set opr 2
set opa 8
set acc 14
set data 85
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0xB
expect pair 0xB2
tick
expect reg 0xB
expect pair 0xB2
tock
expect reg 0xB
expect pair 0xB2
set opr 11
set opa 4
set acc 2
set data 169
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 7
set acc 10
set data 1
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0x3E
tick
expect reg 0xE
expect pair 0x3E
tock
expect reg 0xE
expect pair 0x3E
set opr 10
set opa 1
set acc 3
set data 36
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x2
expect pair 0xB2
tick
expect reg 0x2
expect pair 0xB2
tock
expect reg 0x2
expect pair 0xB2
set opr 10
set opa 6
set acc 6
set data 141
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3E
tick
expect reg 0x3
expect pair 0x3E
tock
expect reg 0x3
expect pair 0x3E
set opr 11
set opa 0
set acc 7
set data 240
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xB
expect pair 0xB2
tick
expect reg 0xB
expect pair 0xB2
tock
expect reg 0x7
expect pair 0x72
set opr 8
set opa 7
set acc 1
set data 203
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x7
expect pair 0x72
tick
expect reg 0x7
expect pair 0x72
tock
expect reg 0x7
expect pair 0x72
set opr 11
set opa 0
set acc 14
set data 89
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x72
tick
expect reg 0x7
expect pair 0x72
tock
expect reg 0x7
expect pair 0x72
set opr 14
set opa 8
set acc 8
set data 27
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 6
set acc 11
set data 37
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3E
tick
expect reg 0x3
expect pair 0x3E
tock
expect reg 0x3
expect pair 0x3E
set opr 8
set opa 6
set acc 11
set data 154
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x7
expect pair 0x72
tick
expect reg 0x7
expect pair 0x72
tock
expect reg 0x7
expect pair 0x72
set opr 8
set opa 14
set acc 13
set data 175
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x10
tick
expect reg 0x1
expect pair 0x10
tock
expect reg 0x1
expect pair 0x10
set opr 2
set opa 15
set acc 3
set data 150
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x10
tick
expect reg 0x0
expect pair 0x10
tock
expect reg 0x0
expect pair 0x10
set opr 1
set opa 5
set acc 4
set data 44
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 6
set acc 8
set data 41
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x3E
tick
expect reg 0x3
expect pair 0x3E
tock
expect reg 0x2
expect pair 0x29
set opr 10
set opa 15
set acc 10
set data 201
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x10
tick
expect reg 0x0
expect pair 0x10
tock
expect reg 0x0
expect pair 0x10
set opr 6
set opa 0
set acc 3
set data 217
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x72
tick
expect reg 0x7
expect pair 0x72
tock
expect reg 0x7
expect pair 0x72
set opr 2
set opa 13
set acc 13
set data 250
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 6
set opa 0
set acc 13
set data 131
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x72
tick
expect reg 0x7
expect pair 0x72
tock
expect reg 0x7
expect pair 0x72
set opr 2
set opa 15
set acc 9
set data 192
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x10
tick
expect reg 0x0
expect pair 0x10
tock
expect reg 0x0
expect pair 0x10
set opr 3
set opa 8
set acc 9
set data 151
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x7
expect pair 0x72
tick
expect reg 0x7
expect pair 0x72
tock
expect reg 0x7
expect pair 0x72
set opr 14
set opa 4
set acc 4
set data 246
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 6
set acc 14
set data 191
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x2
expect pair 0x29
tick
expect reg 0x2
expect pair 0x29
tock
expect reg 0xB
expect pair 0xBF
set opr 1
set opa 13
set acc 6
set data 8
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 2
set opa 13
set acc 7
set data 241
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x90
tick
expect reg 0x0
expect pair 0x90
tock
expect reg 0x0
expect pair 0x90
set opr 14
set opa 1
set acc 6
set data 22
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x2
expect pair 0x72
tick
expect reg 0x2
expect pair 0x72
tock
expect reg 0x2
expect pair 0x72
set opr 14
set opa 3
set acc 5
set data 242
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0x3E
tick
expect reg 0xE
expect pair 0x3E
tock
expect reg 0xE
expect pair 0x3E
set opr 3
set opa 8
set acc 11
set data 103
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 14
set acc 8
set data 36
set second 1
set write 1
set readp0 0
set reset 1
eval
expect reg 0x1
expect pair 0x10
tick
expect reg 0x1
expect pair 0x10
tock
expect reg 0x0
expect pair 0x00
set opr 4
set opa 15
set acc 13
set data 92
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 13
set acc 4
set data 245
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 5
set acc 10
set data 115
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 4
set opa 10
set acc 13
set data 181
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 9
set acc 6
set data 225
set second 0
set write 0
set readp0 1
set reset 1
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 9
set acc 15
set data 172
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x01
set opr 11
set opa 14
set acc 6
set data 101
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 10
set acc 3
set data 18
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 6
set acc 6
set data 188
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 4
set acc 9
set data 120
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 4
set acc 0
set data 209
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 9
set acc 9
set data 13
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 14
set acc 1
set data 211
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 3
set acc 7
set data 23
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 7
set acc 5
set data 254
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 9
set acc 14
set data 246
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x01
tick
expect reg 0x1
expect pair 0x01
tock
expect reg 0x1
expect pair 0x01
set opr 3
set opa 9
set acc 14
set data 166
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x01
tick
expect reg 0x1
expect pair 0x01
tock
expect reg 0x1
expect pair 0x01
set opr 14
set opa 13
set acc 1
set data 244
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 12
set acc 5
set data 186
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xB
expect pair 0xBA
set opr 3
set opa 5
set acc 0
set data 114
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 0
set acc 14
set data 17
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 4
set acc 2
set data 113
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 10
set acc 0
set data 126
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 10
set acc 3
set data 118
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x7
expect pair 0x76
set opr 2
set opa 15
set acc 7
set data 195
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 15
set acc 15
set data 184
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xF
expect pair 0x0F
set opr 3
set opa 7
set acc 4
set data 23
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 4
set acc 0
set data 232
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 7
set acc 6
set data 130
set second 0
set write 1
set readp0 0
set reset 1
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 11
set acc 12
set data 171
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 6
set acc 8
set data 57
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 11
set acc 5
set data 255
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 13
set acc 12
set data 193
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 5
set acc 11
set data 168
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 13
set acc 1
set data 98
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 0
set acc 1
set data 23
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 11
set acc 6
set data 55
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 13
set acc 0
set data 191
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 11
set acc 8
set data 208
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 7
set acc 10
set data 0
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 7
set acc 13
set data 77
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 7
set acc 4
set data 129
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 11
set acc 13
set data 56
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 15
set acc 1
set data 93
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 5
set acc 8
set data 94
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 6
set acc 5
set data 232
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 0
set acc 10
set data 140
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 14
set acc 5
set data 68
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 9
set acc 14
set data 160
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 9
set acc 4
set data 116
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 15
set acc 10
set data 158
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 1
set acc 2
set data 181
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 11
set acc 1
set data 157
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 6
set acc 15
set data 51
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 4
set opa 5
set acc 3
set data 60
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 10
set acc 2
set data 21
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x1
expect pair 0x15
set opr 6
set opa 14
set acc 11
set data 137
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 10
set acc 10
set data 254
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x1
expect pair 0x15
tick
expect reg 0x1
expect pair 0x15
tock
expect reg 0xF
expect pair 0xFE
set opr 2
set opa 14
set acc 14
set data 117
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 13
set acc 7
set data 56
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 10
set acc 5
set data 83
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 15
set acc 14
set data 185
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xE
expect pair 0x0E
set opr 10
set opa 5
set acc 6
set data 137
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 15
set acc 8
set data 126
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 4
set opa 12
set acc 9
set data 105
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 7
set acc 14
set data 149
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 6
set acc 10
set data 244
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xA
expect pair 0xA0
set opr 3
set opa 9
set acc 9
set data 129
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 12
set acc 7
set data 181
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 5
set acc 3
set data 43
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 14
set acc 2
set data 118
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 3
set acc 7
set data 220
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 5
set acc 14
set data 75
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 4
set acc 9
set data 186
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 8
set acc 13
set data 106
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 10
set acc 10
set data 188
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xF
expect pair 0xFE
tick
expect reg 0xF
expect pair 0xFE
tock
expect reg 0x0
expect pair 0x0E
set opr 10
set opa 14
set acc 4
set data 182
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x0E
tick
expect reg 0x0
expect pair 0x0E
tock
expect reg 0x0
expect pair 0x0E
set opr 11
set opa 8
set acc 3
set data 71
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 3
set acc 5
set data 51
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 3
set acc 6
set data 18
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 11
set acc 9
set data 251
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0x0E
tick
expect reg 0xE
expect pair 0x0E
tock
expect reg 0xF
expect pair 0x0F
set opr 6
set opa 10
set acc 7
set data 52
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x0F
tick
expect reg 0x0
expect pair 0x0F
tock
expect reg 0x0
expect pair 0x0F
set opr 2
set opa 13
set acc 15
set data 199
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 5
set acc 9
set data 93
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 4
set acc 6
set data 169
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xA
expect pair 0xA9
set opr 2
set opa 4
set acc 1
set data 77
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0xA9
tick
expect reg 0xA
expect pair 0xA9
tock
expect reg 0xA
expect pair 0xA9
set opr 2
set opa 2
set acc 15
set data 201
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0xC
expect pair 0xC9
set opr 8
set opa 4
set acc 15
set data 113
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 8
set opa 0
set acc 12
set data 100
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 8
set acc 8
set data 59
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 0
set acc 8
set data 209
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 15
set acc 10
set data 140
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0xE
expect pair 0x0E
tick
expect reg 0xE
expect pair 0x0E
tock
expect reg 0xE
expect pair 0x0E
set opr 4
set opa 1
set acc 0
set data 16
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 13
set acc 2
set data 71
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 10
set acc 6
set data 57
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x0F
tick
expect reg 0x0
expect pair 0x0F
tock
expect reg 0x0
expect pair 0x0F
set opr 2
set opa 12
set acc 14
set data 198
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 4
set acc 4
set data 23
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0xA
expect pair 0xA9
tick
expect reg 0xA
expect pair 0xA9
tock
expect reg 0xA
expect pair 0xA9
set opr 8
set opa 7
set acc 4
set data 34
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0xA0
tick
expect reg 0x0
expect pair 0xA0
tock
expect reg 0x0
expect pair 0xA0
set opr 11
set opa 10
set acc 1
set data 33
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 3
set acc 5
set data 241
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xC9
tick
expect reg 0x9
expect pair 0xC9
tock
expect reg 0x9
expect pair 0xC9
set opr 4
set opa 5
set acc 8
set data 87
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xA9
tick
expect reg 0x9
expect pair 0xA9
tock
expect reg 0x9
expect pair 0xA9
set opr 10
set opa 9
set acc 7
set data 142
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 6
set opa 5
set acc 3
set data 27
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xA9
tick
expect reg 0x9
expect pair 0xA9
tock
expect reg 0x9
expect pair 0xA9
set opr 2
set opa 3
set acc 0
set data 68
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xC9
tick
expect reg 0x9
expect pair 0xC9
tock
expect reg 0x9
expect pair 0xC9
set opr 4
set opa 9
set acc 15
set data 98
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 12
set acc 11
set data 180
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 3
set acc 11
set data 134
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xC9
tick
expect reg 0x9
expect pair 0xC9
tock
expect reg 0x9
expect pair 0xC9
set opr 3
set opa 5
set acc 3
set data 124
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0xA9
tick
expect reg 0x9
expect pair 0xA9
tock
expect reg 0x9
expect pair 0xA9
set opr 10
set opa 2
set acc 0
set data 191
set second 1
set write 0
set readp0 1
set reset 1
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 0
set acc 3
set data 115
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 7
set acc 5
set data 123
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 14
set acc 8
set data 239
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 10
set acc 4
set data 184
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 9
set acc 9
set data 165
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 5
set acc 11
set data 143
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 5
set acc 11
set data 87
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 15
set acc 15
set data 230
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 14
set acc 12
set data 135
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x8
expect pair 0x87
set opr 2
set opa 8
set acc 12
set data 147
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x9
expect pair 0x93
set opr 3
set opa 1
set acc 9
set data 241
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 1
set opa 5
set acc 0
set data 198
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 3
set acc 8
set data 2
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 8
set acc 3
set data 221
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x93
tick
expect reg 0x9
expect pair 0x93
tock
expect reg 0x9
expect pair 0x93
set opr 2
set opa 5
set acc 6
set data 242
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 10
set opa 15
set acc 15
set data 214
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x87
tick
expect reg 0x7
expect pair 0x87
tock
expect reg 0x7
expect pair 0x87
set opr 8
set opa 11
set acc 14
set data 60
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 7
set acc 1
set data 22
set second 0
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 7
set opa 5
set acc 5
set data 35
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 9
set acc 1
set data 239
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x3
expect pair 0x93
tick
expect reg 0x3
expect pair 0x93
tock
expect reg 0x3
expect pair 0x93
set opr 14
set opa 11
set acc 3
set data 65
set second 1
set write 0
set readp0 1
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 11
set opa 3
set acc 14
set data 231
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 6
set acc 10
set data 114
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 3
set acc 11
set data 232
set second 1
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 14
set acc 6
set data 115
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x8
expect pair 0x87
tick
expect reg 0x8
expect pair 0x87
tock
expect reg 0x8
expect pair 0x87
set opr 8
set opa 15
set acc 8
set data 174
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x87
tick
expect reg 0x7
expect pair 0x87
tock
expect reg 0x7
expect pair 0x87
set opr 2
set opa 7
set acc 0
set data 160
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 3
set acc 4
set data 88
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 14
set opa 2
set acc 10
set data 149
set second 0
set write 0
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 2
set opa 15
set acc 12
set data 86
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x7
expect pair 0x87
tick
expect reg 0x7
expect pair 0x87
tock
expect reg 0x7
expect pair 0x87
set opr 8
set opa 5
set acc 7
set data 25
set second 0
set write 1
set readp0 0
set reset 0
eval
expect reg 0x0
expect pair 0x00
tick
expect reg 0x0
expect pair 0x00
tock
expect reg 0x0
expect pair 0x00
set opr 3
set opa 8
set acc 7
set data 12
set second 1
set write 1
set readp0 0
set reset 0
eval
expect reg 0x9
expect pair 0x93
tick
expect reg 0x9
expect pair 0x93
tock
expect reg 0x0
expect pair 0x0C
