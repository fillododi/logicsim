// Jumps: step adds one to the PC; exec at 1 runs the instruction's jump: in a second
// cycle JUN, JMS, and JCN and ISZ when they jump; in a first cycle JIN and BBL. Reset
// clears the PC and the stack. step and exec are never 1 together. Random cycles with
// seed 4007, from a model of the 4004's 4-level stack.
chip Jumps
// Before any reset the PC is unknown.
set opr 3
set opa 8
set data 64
set pair 81
set reg 12
set acc 1
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc *
tock
expect pc *
// Reset, then steps, calls four deep, returns, and every kind of jump.
set opr 7
set opa 1
set data 243
set pair 22
set reg 7
set acc 8
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc *
tock
expect pc 0x000
set opr 3
set opa 0
set data 103
set pair 14
set reg 0
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 7
set opa 5
set data 148
set pair 193
set reg 12
set acc 1
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 4
set opa 0
set data 34
set pair 219
set reg 12
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 5
set opa 15
set data 237
set pair 75
set reg 1
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0xFED
set opr 7
set opa 1
set data 141
set pair 100
set reg 15
set acc 11
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xFED
tock
expect pc 0xFEE
set opr 5
set opa 8
set data 230
set pair 106
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xFEE
tock
expect pc 0x8E6
set opr 4
set opa 12
set data 142
set pair 162
set reg 10
set acc 12
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x8E6
tock
expect pc 0x8E7
set opr 5
set opa 4
set data 196
set pair 122
set reg 0
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x8E7
tock
expect pc 0x4C4
set opr 7
set opa 2
set data 187
set pair 108
set reg 2
set acc 2
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x4C4
tock
expect pc 0x4C5
set opr 5
set opa 9
set data 119
set pair 12
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x4C5
tock
expect pc 0x977
set opr 3
set opa 15
set data 162
set pair 111
set reg 7
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x977
tock
expect pc 0x978
set opr 12
set opa 14
set data 213
set pair 190
set reg 5
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x978
tock
expect pc 0x4C5
set opr 12
set opa 12
set data 102
set pair 30
set reg 5
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x4C5
tock
expect pc 0x8E7
set opr 12
set opa 12
set data 49
set pair 141
set reg 1
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8E7
tock
expect pc 0xFEE
set opr 12
set opa 2
set data 233
set pair 167
set reg 11
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xFEE
tock
expect pc 0x978
set opr 12
set opa 0
set data 169
set pair 166
set reg 9
set acc 15
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x978
tock
expect pc 0x4C5
// Random cycles: a step, an exec or nothing; reset now and then.
set opr 12
set opa 0
set data 240
set pair 108
set reg 5
set acc 1
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x4C5
tock
expect pc 0x8E7
set opr 5
set opa 15
set data 21
set pair 74
set reg 12
set acc 9
set carry 0
set test 0
set second 1
set step 0
set exec 0
set reset 1
tick
expect pc 0x8E7
tock
expect pc 0x000
set opr 12
set opa 14
set data 214
set pair 8
set reg 11
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 13
set data 75
set pair 9
set reg 2
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 3
set opa 3
set data 106
set pair 13
set reg 10
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x00D
set opr 12
set opa 12
set data 64
set pair 211
set reg 10
set acc 6
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x00D
tock
expect pc 0x00E
set opr 7
set opa 6
set data 184
set pair 94
set reg 15
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x00E
tock
expect pc 0x00E
set opr 7
set opa 6
set data 126
set pair 163
set reg 5
set acc 10
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x00E
tock
expect pc 0x00E
set opr 12
set opa 9
set data 236
set pair 114
set reg 8
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x00E
tock
expect pc 0x00E
set opr 12
set opa 9
set data 187
set pair 150
set reg 15
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x00E
tock
expect pc 0x00F
set opr 7
set opa 14
set data 121
set pair 236
set reg 3
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x00F
tock
expect pc 0x010
set opr 1
set opa 1
set data 237
set pair 240
set reg 1
set acc 7
set carry 0
set test 1
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x010
tock
expect pc 0x010
set opr 1
set opa 12
set data 208
set pair 48
set reg 12
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x010
tock
expect pc 0x010
set opr 1
set opa 5
set data 119
set pair 242
set reg 1
set acc 9
set carry 0
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x010
tock
expect pc 0x010
set opr 1
set opa 15
set data 87
set pair 239
set reg 6
set acc 14
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x010
tock
expect pc 0x010
set opr 7
set opa 1
set data 158
set pair 136
set reg 15
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x010
tock
expect pc 0x010
set opr 12
set opa 0
set data 116
set pair 78
set reg 5
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x010
tock
expect pc 0x000
set opr 3
set opa 10
set data 230
set pair 210
set reg 7
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 4
set opa 14
set data 252
set pair 176
set reg 3
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 12
set data 28
set pair 7
set reg 7
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 7
set data 98
set pair 161
set reg 3
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 7
set opa 4
set data 210
set pair 27
set reg 1
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x0D2
set opr 7
set opa 7
set data 74
set pair 209
set reg 3
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D2
tock
expect pc 0x0D3
set opr 1
set opa 14
set data 183
set pair 230
set reg 8
set acc 13
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0D3
tock
expect pc 0x0D3
set opr 1
set opa 2
set data 1
set pair 46
set reg 1
set acc 5
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D3
tock
expect pc 0x0D4
set opr 5
set opa 15
set data 222
set pair 120
set reg 8
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x0D4
tock
expect pc 0x0D4
set opr 5
set opa 10
set data 172
set pair 171
set reg 6
set acc 0
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D4
tock
expect pc 0x0D5
set opr 4
set opa 11
set data 48
set pair 111
set reg 15
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D5
tock
expect pc 0x0D6
set opr 7
set opa 4
set data 101
set pair 44
set reg 12
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D6
tock
expect pc 0x0D7
set opr 13
set opa 14
set data 58
set pair 88
set reg 8
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D7
tock
expect pc 0x0D8
set opr 5
set opa 11
set data 40
set pair 216
set reg 2
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0D8
tock
expect pc 0xB28
set opr 5
set opa 6
set data 114
set pair 74
set reg 9
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xB28
tock
expect pc 0xB28
set opr 1
set opa 7
set data 89
set pair 98
set reg 0
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xB28
tock
expect pc 0xB28
set opr 4
set opa 12
set data 45
set pair 221
set reg 7
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xB28
tock
expect pc 0xB28
set opr 7
set opa 7
set data 104
set pair 106
set reg 15
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xB28
tock
expect pc 0xB28
set opr 13
set opa 8
set data 136
set pair 86
set reg 10
set acc 3
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xB28
tock
expect pc 0xB28
set opr 12
set opa 7
set data 180
set pair 83
set reg 12
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xB28
tock
expect pc 0xB28
set opr 13
set opa 7
set data 41
set pair 149
set reg 0
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 0
set reset 1
tick
expect pc 0xB28
tock
expect pc 0x000
set opr 2
set opa 14
set data 152
set pair 45
set reg 2
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 10
set data 221
set pair 27
set reg 14
set acc 15
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 7
set opa 4
set data 83
set pair 103
set reg 0
set acc 3
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 7
set opa 0
set data 133
set pair 137
set reg 12
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 5
set opa 1
set data 176
set pair 175
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x1B0
set opr 12
set opa 7
set data 238
set pair 109
set reg 3
set acc 11
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1B0
tock
expect pc 0x1B0
set opr 1
set opa 9
set data 193
set pair 177
set reg 11
set acc 12
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1B0
tock
expect pc 0x1B0
set opr 2
set opa 15
set data 161
set pair 52
set reg 9
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1B0
tock
expect pc 0x1B0
set opr 4
set opa 12
set data 2
set pair 21
set reg 6
set acc 14
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x1B0
tock
expect pc 0x1B1
set opr 5
set opa 0
set data 79
set pair 249
set reg 4
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x1B1
tock
expect pc 0x1B2
set opr 7
set opa 13
set data 198
set pair 22
set reg 10
set acc 11
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1B2
tock
expect pc 0x1C6
set opr 7
set opa 4
set data 72
set pair 51
set reg 8
set acc 7
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1C6
tock
expect pc 0x148
set opr 7
set opa 6
set data 157
set pair 223
set reg 13
set acc 13
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x148
tock
expect pc 0x19D
set opr 5
set opa 7
set data 25
set pair 47
set reg 0
set acc 13
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x19D
tock
expect pc 0x719
set opr 5
set opa 0
set data 112
set pair 12
set reg 0
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x719
tock
expect pc 0x71A
set opr 1
set opa 13
set data 231
set pair 169
set reg 0
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x71A
tock
expect pc 0x71A
set opr 1
set opa 5
set data 165
set pair 87
set reg 10
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x71A
tock
expect pc 0x71B
set opr 4
set opa 0
set data 159
set pair 131
set reg 10
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x71B
tock
expect pc 0x71C
set opr 12
set opa 3
set data 98
set pair 218
set reg 7
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0x71C
tock
expect pc 0x000
set opr 12
set opa 1
set data 147
set pair 15
set reg 14
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 7
set opa 15
set data 33
set pair 175
set reg 14
set acc 8
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 2
set opa 5
set data 82
set pair 243
set reg 2
set acc 7
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 5
set opa 0
set data 249
set pair 241
set reg 9
set acc 7
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 7
set opa 12
set data 66
set pair 14
set reg 2
set acc 10
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 7
set opa 14
set data 133
set pair 211
set reg 11
set acc 10
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 13
set opa 12
set data 114
set pair 17
set reg 9
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 5
set opa 3
set data 130
set pair 250
set reg 2
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 1
set opa 1
set data 190
set pair 255
set reg 15
set acc 1
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 2
set opa 15
set data 221
set pair 182
set reg 4
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 7
set opa 14
set data 131
set pair 123
set reg 2
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0x003
tock
expect pc 0x000
set opr 1
set opa 3
set data 89
set pair 227
set reg 5
set acc 4
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 12
set opa 11
set data 53
set pair 164
set reg 10
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x000
set opr 1
set opa 10
set data 160
set pair 158
set reg 7
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x0A0
set opr 12
set opa 13
set data 44
set pair 204
set reg 7
set acc 2
set carry 1
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x0A0
tock
expect pc 0x0A0
set opr 12
set opa 10
set data 71
set pair 8
set reg 13
set acc 13
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0A0
tock
expect pc 0x0A0
set opr 5
set opa 5
set data 160
set pair 201
set reg 1
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x0A0
tock
expect pc 0x0A0
set opr 7
set opa 4
set data 131
set pair 142
set reg 15
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0A0
tock
expect pc 0x0A1
set opr 2
set opa 6
set data 211
set pair 29
set reg 8
set acc 5
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0A1
tock
expect pc 0x0A2
set opr 1
set opa 14
set data 205
set pair 196
set reg 14
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0A2
tock
expect pc 0x0A2
set opr 5
set opa 5
set data 144
set pair 185
set reg 3
set acc 1
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0A2
tock
expect pc 0x0A3
set opr 5
set opa 0
set data 62
set pair 154
set reg 7
set acc 9
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x0A3
tock
expect pc 0x0A3
set opr 4
set opa 13
set data 98
set pair 8
set reg 14
set acc 8
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0A3
tock
expect pc 0xD62
set opr 12
set opa 2
set data 187
set pair 5
set reg 8
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xD62
tock
expect pc 0xD62
set opr 13
set opa 13
set data 200
set pair 42
set reg 6
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xD62
tock
expect pc 0xD62
set opr 13
set opa 3
set data 85
set pair 80
set reg 2
set acc 1
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xD62
tock
expect pc 0xD62
set opr 13
set opa 13
set data 11
set pair 225
set reg 3
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xD62
tock
expect pc 0xD62
set opr 3
set opa 11
set data 212
set pair 84
set reg 12
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xD62
tock
expect pc 0xD54
set opr 13
set opa 14
set data 225
set pair 121
set reg 1
set acc 9
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xD54
tock
expect pc 0xD54
set opr 7
set opa 7
set data 163
set pair 142
set reg 2
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xD54
tock
expect pc 0xDA3
set opr 2
set opa 6
set data 131
set pair 110
set reg 3
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0xDA3
tock
expect pc 0x000
set opr 1
set opa 9
set data 3
set pair 168
set reg 1
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 1
set opa 7
set data 229
set pair 187
set reg 7
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 3
set opa 10
set data 228
set pair 205
set reg 10
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x002
tock
expect pc 0x002
set opr 7
set opa 15
set data 162
set pair 0
set reg 10
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 3
set opa 5
set data 122
set pair 114
set reg 13
set acc 1
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x003
tock
expect pc 0x004
set opr 2
set opa 7
set data 1
set pair 39
set reg 3
set acc 3
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x004
tock
expect pc 0x005
set opr 12
set opa 9
set data 112
set pair 205
set reg 12
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x005
tock
expect pc 0x006
set opr 12
set opa 13
set data 13
set pair 228
set reg 6
set acc 11
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x006
tock
expect pc 0x006
set opr 12
set opa 3
set data 159
set pair 185
set reg 12
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x006
tock
expect pc 0x000
set opr 1
set opa 15
set data 102
set pair 164
set reg 10
set acc 6
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 12
set opa 9
set data 79
set pair 75
set reg 11
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 5
set opa 7
set data 162
set pair 135
set reg 0
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 12
set opa 14
set data 142
set pair 210
set reg 0
set acc 2
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 13
set opa 9
set data 152
set pair 137
set reg 9
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 4
set opa 6
set data 114
set pair 18
set reg 14
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 12
set opa 0
set data 160
set pair 101
set reg 11
set acc 4
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 3
set opa 7
set data 52
set pair 66
set reg 2
set acc 5
set carry 0
set test 0
set second 1
set step 0
set exec 0
set reset 1
tick
expect pc 0x001
tock
expect pc 0x000
set opr 3
set opa 13
set data 6
set pair 238
set reg 3
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 7
set opa 4
set data 23
set pair 63
set reg 1
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 12
set opa 6
set data 100
set pair 228
set reg 8
set acc 2
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 5
set data 255
set pair 12
set reg 10
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x0FF
set opr 1
set opa 10
set data 58
set pair 233
set reg 14
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x0FF
tock
expect pc 0x0FF
set opr 12
set opa 7
set data 83
set pair 165
set reg 3
set acc 12
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0FF
tock
expect pc 0x100
set opr 12
set opa 4
set data 221
set pair 13
set reg 9
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x100
tock
expect pc 0x101
set opr 3
set opa 13
set data 98
set pair 31
set reg 12
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x101
tock
expect pc 0x101
set opr 13
set opa 7
set data 129
set pair 120
set reg 10
set acc 11
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x101
tock
expect pc 0x101
set opr 2
set opa 9
set data 59
set pair 123
set reg 10
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x101
tock
expect pc 0x101
set opr 7
set opa 8
set data 193
set pair 171
set reg 7
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x101
tock
expect pc 0x1C1
set opr 12
set opa 15
set data 37
set pair 64
set reg 2
set acc 2
set carry 1
set test 1
set second 1
set step 0
set exec 0
set reset 1
tick
expect pc 0x1C1
tock
expect pc 0x000
set opr 4
set opa 2
set data 13
set pair 210
set reg 11
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 5
set opa 1
set data 100
set pair 173
set reg 2
set acc 2
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 5
set opa 10
set data 213
set pair 28
set reg 8
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x002
tock
expect pc 0xAD5
set opr 1
set opa 4
set data 21
set pair 247
set reg 6
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xAD5
tock
expect pc 0xAD6
set opr 1
set opa 5
set data 60
set pair 39
set reg 13
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAD6
tock
expect pc 0xAD6
set opr 3
set opa 13
set data 224
set pair 153
set reg 4
set acc 2
set carry 0
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0xAD6
tock
expect pc 0xAD6
set opr 2
set opa 9
set data 104
set pair 222
set reg 13
set acc 11
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xAD6
tock
expect pc 0xAD7
set opr 13
set opa 5
set data 123
set pair 35
set reg 10
set acc 6
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xAD7
tock
expect pc 0xAD7
set opr 1
set opa 12
set data 69
set pair 151
set reg 4
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0xAD7
tock
expect pc 0xAD7
set opr 5
set opa 7
set data 229
set pair 73
set reg 5
set acc 3
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xAD7
tock
expect pc 0xAD8
set opr 1
set opa 3
set data 22
set pair 189
set reg 9
set acc 13
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xAD8
tock
expect pc 0xA16
set opr 5
set opa 10
set data 120
set pair 214
set reg 3
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xA16
tock
expect pc 0xA16
set opr 1
set opa 4
set data 210
set pair 24
set reg 10
set acc 4
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA16
tock
expect pc 0xA16
set opr 7
set opa 6
set data 54
set pair 48
set reg 13
set acc 6
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xA16
tock
expect pc 0xA17
set opr 7
set opa 8
set data 211
set pair 234
set reg 2
set acc 6
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA17
tock
expect pc 0xA18
set opr 3
set opa 15
set data 18
set pair 219
set reg 15
set acc 9
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA18
tock
expect pc 0xA19
set opr 7
set opa 8
set data 23
set pair 79
set reg 3
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xA19
tock
expect pc 0xA1A
set opr 2
set opa 14
set data 50
set pair 158
set reg 3
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xA1A
tock
expect pc 0xA1B
set opr 13
set opa 15
set data 254
set pair 213
set reg 3
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA1B
tock
expect pc 0xA1B
set opr 1
set opa 1
set data 82
set pair 177
set reg 3
set acc 10
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA1B
tock
expect pc 0xA1C
set opr 4
set opa 0
set data 183
set pair 239
set reg 13
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xA1C
tock
expect pc 0xA1D
set opr 13
set opa 11
set data 59
set pair 212
set reg 9
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xA1D
tock
expect pc 0xA1D
set opr 4
set opa 11
set data 244
set pair 1
set reg 5
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA1D
tock
expect pc 0xA1E
set opr 12
set opa 4
set data 143
set pair 118
set reg 12
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xA1E
tock
expect pc 0xA1F
set opr 7
set opa 6
set data 14
set pair 250
set reg 5
set acc 8
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA1F
tock
expect pc 0xA1F
set opr 5
set opa 8
set data 140
set pair 29
set reg 11
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xA1F
tock
expect pc 0xA1F
set opr 1
set opa 4
set data 240
set pair 235
set reg 4
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA1F
tock
expect pc 0xA20
set opr 5
set opa 13
set data 101
set pair 200
set reg 5
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xA20
tock
expect pc 0xA20
set opr 7
set opa 4
set data 97
set pair 210
set reg 1
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA20
tock
expect pc 0xA21
set opr 13
set opa 8
set data 56
set pair 200
set reg 1
set acc 8
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA21
tock
expect pc 0xA22
set opr 7
set opa 1
set data 156
set pair 39
set reg 5
set acc 1
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA22
tock
expect pc 0xA22
set opr 2
set opa 7
set data 144
set pair 215
set reg 9
set acc 1
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xA22
tock
expect pc 0xA22
set opr 1
set opa 13
set data 97
set pair 148
set reg 10
set acc 13
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA22
tock
expect pc 0xA23
set opr 7
set opa 0
set data 194
set pair 234
set reg 2
set acc 2
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xA23
tock
expect pc 0xAC2
set opr 2
set opa 11
set data 56
set pair 135
set reg 15
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xAC2
tock
expect pc 0xAC2
set opr 1
set opa 7
set data 98
set pair 96
set reg 11
set acc 10
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAC2
tock
expect pc 0xAC2
set opr 7
set opa 11
set data 223
set pair 161
set reg 2
set acc 14
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xAC2
tock
expect pc 0xAC3
set opr 2
set opa 1
set data 173
set pair 22
set reg 13
set acc 11
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xAC3
tock
expect pc 0xAC4
set opr 13
set opa 11
set data 157
set pair 241
set reg 5
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAC4
tock
expect pc 0xAC4
set opr 1
set opa 7
set data 40
set pair 60
set reg 0
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xAC4
tock
expect pc 0xAC5
set opr 7
set opa 9
set data 238
set pair 41
set reg 15
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xAC5
tock
expect pc 0xAEE
set opr 5
set opa 8
set data 152
set pair 210
set reg 14
set acc 11
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAEE
tock
expect pc 0xAEE
set opr 4
set opa 8
set data 82
set pair 185
set reg 11
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xAEE
tock
expect pc 0xAEE
set opr 5
set opa 11
set data 179
set pair 122
set reg 12
set acc 1
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAEE
tock
expect pc 0xAEE
set opr 12
set opa 12
set data 203
set pair 143
set reg 0
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xAEE
tock
expect pc 0xAEF
set opr 5
set opa 3
set data 179
set pair 189
set reg 1
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAEF
tock
expect pc 0xAEF
set opr 5
set opa 0
set data 0
set pair 193
set reg 13
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xAEF
tock
expect pc 0x000
set opr 7
set opa 6
set data 105
set pair 133
set reg 6
set acc 7
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 4
set opa 12
set data 179
set pair 219
set reg 15
set acc 6
set carry 1
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 1
set opa 0
set data 56
set pair 29
set reg 5
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 7
set opa 2
set data 117
set pair 144
set reg 15
set acc 15
set carry 0
set test 1
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0x002
tock
expect pc 0x000
set opr 1
set opa 5
set data 53
set pair 119
set reg 2
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 7
set opa 11
set data 83
set pair 250
set reg 9
set acc 12
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 2
set opa 1
set data 227
set pair 98
set reg 3
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 4
set opa 8
set data 205
set pair 5
set reg 3
set acc 11
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 13
set opa 4
set data 28
set pair 73
set reg 12
set acc 15
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 3
set opa 4
set data 103
set pair 149
set reg 7
set acc 4
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 3
set opa 5
set data 20
set pair 109
set reg 13
set acc 4
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 12
set opa 5
set data 73
set pair 124
set reg 3
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x000
set opr 5
set opa 7
set data 42
set pair 225
set reg 5
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 1
set opa 1
set data 87
set pair 134
set reg 8
set acc 14
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 13
set opa 9
set data 80
set pair 237
set reg 14
set acc 5
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 7
set opa 9
set data 86
set pair 220
set reg 15
set acc 13
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 5
set opa 12
set data 8
set pair 218
set reg 13
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 12
set opa 10
set data 33
set pair 200
set reg 4
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 5
set opa 10
set data 117
set pair 109
set reg 6
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 5
set opa 13
set data 152
set pair 164
set reg 15
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 2
set opa 6
set data 196
set pair 108
set reg 3
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 7
set opa 10
set data 228
set pair 180
set reg 13
set acc 7
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 3
set opa 6
set data 169
set pair 63
set reg 8
set acc 15
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x003
set opr 7
set opa 6
set data 144
set pair 150
set reg 10
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x003
tock
expect pc 0x004
set opr 1
set opa 8
set data 113
set pair 170
set reg 0
set acc 13
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x004
tock
expect pc 0x071
set opr 7
set opa 12
set data 153
set pair 130
set reg 8
set acc 7
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x071
tock
expect pc 0x071
set opr 12
set opa 14
set data 183
set pair 111
set reg 1
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x071
tock
expect pc 0x072
set opr 2
set opa 6
set data 80
set pair 118
set reg 13
set acc 1
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x072
tock
expect pc 0x072
set opr 2
set opa 14
set data 79
set pair 2
set reg 1
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x072
tock
expect pc 0x072
set opr 5
set opa 9
set data 206
set pair 201
set reg 14
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x072
tock
expect pc 0x073
set opr 12
set opa 5
set data 35
set pair 62
set reg 13
set acc 9
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x073
tock
expect pc 0x000
set opr 3
set opa 9
set data 28
set pair 137
set reg 14
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x089
set opr 12
set opa 0
set data 48
set pair 143
set reg 10
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x089
tock
expect pc 0x000
set opr 13
set opa 7
set data 72
set pair 91
set reg 9
set acc 2
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 5
set opa 10
set data 120
set pair 219
set reg 14
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 2
set opa 10
set data 80
set pair 234
set reg 12
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 5
set opa 0
set data 244
set pair 225
set reg 3
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0x001
tock
expect pc 0x000
set opr 7
set opa 5
set data 216
set pair 234
set reg 3
set acc 13
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x0D8
set opr 1
set opa 10
set data 93
set pair 87
set reg 1
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0D8
tock
expect pc 0x0D8
set opr 13
set opa 9
set data 244
set pair 185
set reg 10
set acc 15
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x0D8
tock
expect pc 0x0D9
set opr 5
set opa 3
set data 124
set pair 61
set reg 0
set acc 4
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0D9
tock
expect pc 0x37C
set opr 5
set opa 6
set data 131
set pair 127
set reg 0
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x37C
tock
expect pc 0x37C
set opr 4
set opa 15
set data 202
set pair 157
set reg 5
set acc 11
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x37C
tock
expect pc 0x37C
set opr 12
set opa 15
set data 240
set pair 40
set reg 1
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0x37C
tock
expect pc 0x000
set opr 3
set opa 10
set data 2
set pair 21
set reg 0
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 12
set opa 2
set data 23
set pair 104
set reg 3
set acc 12
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 3
set opa 2
set data 170
set pair 177
set reg 7
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 5
set data 222
set pair 224
set reg 11
set acc 15
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 12
set opa 1
set data 63
set pair 43
set reg 0
set acc 14
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x000
set opr 7
set opa 5
set data 12
set pair 149
set reg 8
set acc 6
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 3
set opa 15
set data 62
set pair 220
set reg 3
set acc 3
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x0DC
set opr 7
set opa 8
set data 121
set pair 30
set reg 2
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x0DC
tock
expect pc 0x0DC
set opr 1
set opa 10
set data 253
set pair 45
set reg 4
set acc 15
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0DC
tock
expect pc 0x0FD
set opr 4
set opa 7
set data 208
set pair 130
set reg 6
set acc 12
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0FD
tock
expect pc 0x0FE
set opr 12
set opa 6
set data 84
set pair 167
set reg 11
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x0FE
tock
expect pc 0x000
set opr 5
set opa 2
set data 92
set pair 132
set reg 5
set acc 9
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 1
set opa 11
set data 67
set pair 95
set reg 3
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 2
set opa 11
set data 245
set pair 240
set reg 0
set acc 5
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 1
set opa 15
set data 153
set pair 87
set reg 5
set acc 10
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 2
set opa 2
set data 119
set pair 124
set reg 13
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 7
set opa 5
set data 23
set pair 255
set reg 15
set acc 6
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 12
set opa 15
set data 109
set pair 152
set reg 3
set acc 9
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 3
set opa 7
set data 224
set pair 235
set reg 4
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x0EB
set opr 7
set opa 11
set data 30
set pair 11
set reg 7
set acc 15
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x0EB
tock
expect pc 0x0EC
set opr 12
set opa 12
set data 137
set pair 35
set reg 10
set acc 11
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0EC
tock
expect pc 0x0ED
set opr 4
set opa 4
set data 114
set pair 96
set reg 12
set acc 1
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0ED
tock
expect pc 0x472
set opr 5
set opa 15
set data 175
set pair 68
set reg 10
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x472
tock
expect pc 0x473
set opr 5
set opa 7
set data 171
set pair 169
set reg 2
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x473
tock
expect pc 0x473
set opr 13
set opa 14
set data 155
set pair 244
set reg 4
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x473
tock
expect pc 0x473
set opr 12
set opa 6
set data 51
set pair 52
set reg 3
set acc 12
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x473
tock
expect pc 0x000
set opr 12
set opa 1
set data 74
set pair 202
set reg 4
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 3
set opa 6
set data 133
set pair 133
set reg 6
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 7
set opa 15
set data 59
set pair 180
set reg 1
set acc 9
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 2
set opa 9
set data 67
set pair 133
set reg 11
set acc 15
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x002
tock
expect pc 0x002
set opr 13
set opa 0
set data 37
set pair 147
set reg 7
set acc 6
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 5
set opa 7
set data 75
set pair 36
set reg 13
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x003
tock
expect pc 0x74B
set opr 1
set opa 8
set data 114
set pair 62
set reg 7
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x74B
tock
expect pc 0x772
set opr 7
set opa 4
set data 121
set pair 89
set reg 3
set acc 3
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x772
tock
expect pc 0x772
set opr 3
set opa 5
set data 106
set pair 85
set reg 14
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x772
tock
expect pc 0x772
set opr 1
set opa 1
set data 208
set pair 244
set reg 0
set acc 0
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x772
tock
expect pc 0x773
set opr 7
set opa 1
set data 97
set pair 70
set reg 10
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x773
tock
expect pc 0x761
set opr 2
set opa 1
set data 88
set pair 119
set reg 12
set acc 10
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x761
tock
expect pc 0x762
set opr 7
set opa 7
set data 215
set pair 177
set reg 10
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x762
tock
expect pc 0x762
set opr 4
set opa 9
set data 194
set pair 61
set reg 14
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x762
tock
expect pc 0x9C2
set opr 5
set opa 5
set data 51
set pair 171
set reg 2
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x9C2
tock
expect pc 0x9C3
set opr 7
set opa 14
set data 139
set pair 4
set reg 10
set acc 11
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x9C3
tock
expect pc 0x98B
set opr 12
set opa 5
set data 149
set pair 37
set reg 12
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x98B
tock
expect pc 0x98B
set opr 12
set opa 13
set data 187
set pair 190
set reg 14
set acc 11
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x98B
tock
expect pc 0x98C
set opr 2
set opa 14
set data 31
set pair 38
set reg 1
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x98C
tock
expect pc 0x98C
set opr 1
set opa 0
set data 215
set pair 216
set reg 6
set acc 11
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x98C
tock
expect pc 0x98D
set opr 4
set opa 0
set data 35
set pair 0
set reg 4
set acc 12
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x98D
tock
expect pc 0x98E
set opr 2
set opa 15
set data 142
set pair 207
set reg 14
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x98E
tock
expect pc 0x98E
set opr 2
set opa 6
set data 248
set pair 218
set reg 12
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x98E
tock
expect pc 0x98E
set opr 2
set opa 11
set data 7
set pair 206
set reg 0
set acc 13
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x98E
tock
expect pc 0x98E
set opr 7
set opa 4
set data 251
set pair 255
set reg 2
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x98E
tock
expect pc 0x98F
set opr 1
set opa 13
set data 16
set pair 239
set reg 12
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x98F
tock
expect pc 0x98F
set opr 13
set opa 3
set data 88
set pair 119
set reg 1
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x98F
tock
expect pc 0x98F
set opr 5
set opa 9
set data 15
set pair 132
set reg 14
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x98F
tock
expect pc 0x98F
set opr 5
set opa 11
set data 106
set pair 37
set reg 10
set acc 12
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x98F
tock
expect pc 0x98F
set opr 5
set opa 1
set data 135
set pair 33
set reg 7
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x98F
tock
expect pc 0x187
set opr 12
set opa 1
set data 140
set pair 52
set reg 6
set acc 9
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x187
tock
expect pc 0x188
set opr 12
set opa 11
set data 140
set pair 232
set reg 9
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x188
tock
expect pc 0x188
set opr 12
set opa 3
set data 188
set pair 14
set reg 8
set acc 2
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x188
tock
expect pc 0x188
set opr 2
set opa 10
set data 195
set pair 145
set reg 4
set acc 4
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x188
tock
expect pc 0x189
set opr 5
set opa 11
set data 66
set pair 95
set reg 9
set acc 3
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x189
tock
expect pc 0x189
set opr 7
set opa 3
set data 75
set pair 230
set reg 11
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x189
tock
expect pc 0x18A
set opr 5
set opa 9
set data 14
set pair 151
set reg 10
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x18A
tock
expect pc 0x90E
set opr 2
set opa 10
set data 30
set pair 55
set reg 7
set acc 5
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x90E
tock
expect pc 0x90E
set opr 5
set opa 9
set data 50
set pair 196
set reg 3
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x90E
tock
expect pc 0x90E
set opr 7
set opa 4
set data 87
set pair 212
set reg 5
set acc 0
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x90E
tock
expect pc 0x90F
set opr 5
set opa 1
set data 28
set pair 215
set reg 10
set acc 8
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x90F
tock
expect pc 0x910
set opr 1
set opa 7
set data 150
set pair 139
set reg 6
set acc 8
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x910
tock
expect pc 0x911
set opr 1
set opa 8
set data 144
set pair 166
set reg 4
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x911
tock
expect pc 0x912
set opr 5
set opa 3
set data 106
set pair 153
set reg 1
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x912
tock
expect pc 0x912
set opr 2
set opa 11
set data 111
set pair 225
set reg 7
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x912
tock
expect pc 0x912
set opr 4
set opa 14
set data 47
set pair 69
set reg 0
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x912
tock
expect pc 0x913
set opr 7
set opa 0
set data 195
set pair 72
set reg 15
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x913
tock
expect pc 0x913
set opr 12
set opa 10
set data 253
set pair 176
set reg 8
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x913
tock
expect pc 0x18A
set opr 1
set opa 3
set data 129
set pair 70
set reg 1
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x18A
tock
expect pc 0x18B
set opr 12
set opa 1
set data 170
set pair 41
set reg 4
set acc 3
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x18B
tock
expect pc 0x18C
set opr 1
set opa 6
set data 220
set pair 212
set reg 3
set acc 2
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x18C
tock
expect pc 0x18C
set opr 1
set opa 11
set data 55
set pair 72
set reg 15
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x18C
tock
expect pc 0x18C
set opr 1
set opa 14
set data 138
set pair 180
set reg 15
set acc 0
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x18C
tock
expect pc 0x18D
set opr 1
set opa 15
set data 31
set pair 98
set reg 7
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x18D
tock
expect pc 0x18D
set opr 12
set opa 6
set data 4
set pair 241
set reg 9
set acc 6
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x18D
tock
expect pc 0x18E
set opr 2
set opa 6
set data 202
set pair 63
set reg 4
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x18E
tock
expect pc 0x18E
set opr 12
set opa 8
set data 70
set pair 172
set reg 4
set acc 11
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x18E
tock
expect pc 0x18E
set opr 1
set opa 8
set data 172
set pair 0
set reg 11
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x18E
tock
expect pc 0x1AC
set opr 13
set opa 10
set data 187
set pair 93
set reg 13
set acc 2
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x1AC
tock
expect pc 0x1AC
set opr 5
set opa 12
set data 53
set pair 81
set reg 8
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x1AC
tock
expect pc 0x1AC
set opr 13
set opa 13
set data 157
set pair 84
set reg 5
set acc 12
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x1AC
tock
expect pc 0x1AC
set opr 1
set opa 11
set data 168
set pair 135
set reg 11
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x1AC
tock
expect pc 0x1AD
set opr 13
set opa 0
set data 139
set pair 1
set reg 13
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x1AD
tock
expect pc 0x1AD
set opr 5
set opa 10
set data 223
set pair 44
set reg 14
set acc 3
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1AD
tock
expect pc 0xADF
set opr 12
set opa 0
set data 232
set pair 110
set reg 1
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xADF
tock
expect pc 0xADF
set opr 12
set opa 6
set data 22
set pair 179
set reg 10
set acc 13
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xADF
tock
expect pc 0xADF
set opr 4
set opa 2
set data 101
set pair 156
set reg 13
set acc 5
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xADF
tock
expect pc 0xADF
set opr 5
set opa 15
set data 154
set pair 194
set reg 13
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xADF
tock
expect pc 0xAE0
set opr 7
set opa 6
set data 79
set pair 154
set reg 2
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAE0
tock
expect pc 0xAE0
set opr 13
set opa 2
set data 150
set pair 127
set reg 13
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xAE0
tock
expect pc 0xAE1
set opr 13
set opa 14
set data 194
set pair 219
set reg 3
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xAE1
tock
expect pc 0xAE1
set opr 12
set opa 9
set data 100
set pair 12
set reg 13
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xAE1
tock
expect pc 0x1AD
set opr 5
set opa 8
set data 250
set pair 208
set reg 11
set acc 7
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x1AD
tock
expect pc 0x8FA
set opr 5
set opa 7
set data 41
set pair 190
set reg 6
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8FA
tock
expect pc 0x8FA
set opr 3
set opa 3
set data 149
set pair 28
set reg 5
set acc 13
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x8FA
tock
expect pc 0x8FB
set opr 1
set opa 9
set data 213
set pair 82
set reg 14
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8FB
tock
expect pc 0x8FB
set opr 5
set opa 7
set data 49
set pair 252
set reg 2
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x8FB
tock
expect pc 0x8FC
set opr 13
set opa 6
set data 30
set pair 195
set reg 2
set acc 3
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8FC
tock
expect pc 0x8FC
set opr 1
set opa 4
set data 185
set pair 64
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x8FC
tock
expect pc 0x8B9
set opr 12
set opa 6
set data 134
set pair 146
set reg 10
set acc 10
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x8B9
tock
expect pc 0x8B9
set opr 12
set opa 6
set data 179
set pair 133
set reg 1
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x8B9
tock
expect pc 0x8BA
set opr 1
set opa 2
set data 17
set pair 129
set reg 0
set acc 12
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8BA
tock
expect pc 0x8BA
set opr 13
set opa 10
set data 168
set pair 4
set reg 14
set acc 12
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8BA
tock
expect pc 0x8BA
set opr 12
set opa 10
set data 30
set pair 204
set reg 10
set acc 2
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x8BA
tock
expect pc 0x1AD
set opr 12
set opa 0
set data 105
set pair 214
set reg 10
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x1AD
tock
expect pc 0x98F
set opr 1
set opa 9
set data 251
set pair 107
set reg 13
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x98F
tock
expect pc 0x990
set opr 4
set opa 6
set data 140
set pair 49
set reg 12
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x990
tock
expect pc 0x68C
set opr 7
set opa 0
set data 84
set pair 45
set reg 12
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x68C
tock
expect pc 0x654
set opr 1
set opa 15
set data 108
set pair 83
set reg 2
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x654
tock
expect pc 0x654
set opr 1
set opa 5
set data 147
set pair 243
set reg 15
set acc 5
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x654
tock
expect pc 0x654
set opr 12
set opa 1
set data 72
set pair 199
set reg 2
set acc 9
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x654
tock
expect pc 0x655
set opr 1
set opa 4
set data 57
set pair 116
set reg 7
set acc 3
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x655
tock
expect pc 0x655
set opr 1
set opa 11
set data 48
set pair 209
set reg 3
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x655
tock
expect pc 0x655
set opr 12
set opa 4
set data 223
set pair 21
set reg 4
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x655
tock
expect pc 0x655
set opr 12
set opa 10
set data 163
set pair 73
set reg 10
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x655
tock
expect pc 0x656
set opr 3
set opa 11
set data 27
set pair 113
set reg 3
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x656
tock
expect pc 0x671
set opr 12
set opa 15
set data 189
set pair 145
set reg 2
set acc 7
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x671
tock
expect pc 0x671
set opr 12
set opa 11
set data 164
set pair 6
set reg 2
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x671
tock
expect pc 0x671
set opr 1
set opa 9
set data 4
set pair 84
set reg 7
set acc 14
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x671
tock
expect pc 0x604
set opr 3
set opa 10
set data 17
set pair 165
set reg 7
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x604
tock
expect pc 0x605
set opr 2
set opa 11
set data 89
set pair 168
set reg 14
set acc 15
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x605
tock
expect pc 0x605
set opr 5
set opa 15
set data 100
set pair 100
set reg 10
set acc 5
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x605
tock
expect pc 0x606
set opr 2
set opa 3
set data 67
set pair 111
set reg 14
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x606
tock
expect pc 0x606
set opr 5
set opa 8
set data 131
set pair 86
set reg 6
set acc 14
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0x606
tock
expect pc 0x000
set opr 1
set opa 1
set data 37
set pair 4
set reg 0
set acc 2
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 13
set opa 9
set data 168
set pair 200
set reg 3
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 3
set opa 13
set data 128
set pair 9
set reg 4
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 1
set opa 15
set data 10
set pair 190
set reg 12
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 4
set opa 15
set data 150
set pair 54
set reg 7
set acc 0
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 7
set opa 6
set data 241
set pair 200
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x002
tock
expect pc 0x0F1
set opr 5
set opa 8
set data 52
set pair 62
set reg 8
set acc 3
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x0F1
tock
expect pc 0x0F2
set opr 1
set opa 2
set data 193
set pair 80
set reg 6
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x0F2
tock
expect pc 0x0C1
set opr 3
set opa 3
set data 173
set pair 107
set reg 3
set acc 0
set carry 0
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x0C1
tock
expect pc 0x06B
set opr 5
set opa 9
set data 25
set pair 150
set reg 10
set acc 2
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x06B
tock
expect pc 0x919
set opr 12
set opa 4
set data 193
set pair 227
set reg 14
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x919
tock
expect pc 0x919
set opr 12
set opa 1
set data 167
set pair 9
set reg 6
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x919
tock
expect pc 0x06B
set opr 13
set opa 8
set data 83
set pair 35
set reg 7
set acc 0
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x06B
tock
expect pc 0x06C
set opr 3
set opa 12
set data 114
set pair 61
set reg 1
set acc 2
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x06C
tock
expect pc 0x06C
set opr 2
set opa 15
set data 244
set pair 255
set reg 8
set acc 3
set carry 0
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x06C
tock
expect pc 0x06D
set opr 2
set opa 10
set data 163
set pair 106
set reg 10
set acc 0
set carry 1
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x06D
tock
expect pc 0x06E
set opr 3
set opa 14
set data 113
set pair 60
set reg 5
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x06E
tock
expect pc 0x06E
set opr 12
set opa 8
set data 210
set pair 66
set reg 2
set acc 5
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x06E
tock
expect pc 0x06E
set opr 5
set opa 12
set data 36
set pair 130
set reg 14
set acc 15
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x06E
tock
expect pc 0xC24
set opr 7
set opa 11
set data 207
set pair 48
set reg 13
set acc 1
set carry 0
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xC24
tock
expect pc 0xC24
set opr 4
set opa 10
set data 207
set pair 39
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xC24
tock
expect pc 0xACF
set opr 3
set opa 11
set data 93
set pair 81
set reg 13
set acc 2
set carry 1
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xACF
tock
expect pc 0xACF
set opr 12
set opa 4
set data 248
set pair 211
set reg 0
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xACF
tock
expect pc 0xACF
set opr 7
set opa 15
set data 191
set pair 235
set reg 4
set acc 14
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xACF
tock
expect pc 0xABF
set opr 5
set opa 0
set data 127
set pair 91
set reg 3
set acc 15
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xABF
tock
expect pc 0xAC0
set opr 2
set opa 7
set data 201
set pair 107
set reg 2
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0xAC0
tock
expect pc 0xAC0
set opr 7
set opa 3
set data 42
set pair 165
set reg 15
set acc 11
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xAC0
tock
expect pc 0xA2A
set opr 4
set opa 3
set data 208
set pair 229
set reg 9
set acc 1
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA2A
tock
expect pc 0xA2A
set opr 13
set opa 4
set data 90
set pair 22
set reg 3
set acc 9
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0xA2A
tock
expect pc 0xA2B
set opr 13
set opa 13
set data 255
set pair 102
set reg 15
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0xA2B
tock
expect pc 0xA2B
set opr 4
set opa 3
set data 62
set pair 214
set reg 15
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0xA2B
tock
expect pc 0xA2B
set opr 1
set opa 13
set data 231
set pair 82
set reg 7
set acc 12
set carry 0
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0xA2B
tock
expect pc 0xA2C
set opr 1
set opa 9
set data 107
set pair 213
set reg 7
set acc 0
set carry 1
set test 0
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0xA2C
tock
expect pc 0xA2C
set opr 1
set opa 3
set data 193
set pair 54
set reg 7
set acc 10
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA2C
tock
expect pc 0xA2C
set opr 1
set opa 10
set data 217
set pair 17
set reg 3
set acc 6
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0xA2C
tock
expect pc 0xA2C
set opr 5
set opa 15
set data 254
set pair 140
set reg 13
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 1
tick
expect pc 0xA2C
tock
expect pc 0x000
set opr 7
set opa 15
set data 83
set pair 87
set reg 11
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 12
set opa 13
set data 116
set pair 121
set reg 15
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 1
set opa 14
set data 12
set pair 8
set reg 5
set acc 11
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 12
set opa 5
set data 245
set pair 30
set reg 4
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 1
set opa 13
set data 59
set pair 96
set reg 2
set acc 9
set carry 0
set test 1
set second 1
set step 0
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x001
set opr 13
set opa 15
set data 176
set pair 155
set reg 13
set acc 0
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x001
tock
expect pc 0x002
set opr 3
set opa 9
set data 80
set pair 25
set reg 11
set acc 0
set carry 1
set test 1
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x002
tock
expect pc 0x003
set opr 1
set opa 14
set data 148
set pair 179
set reg 12
set acc 0
set carry 1
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x003
tock
expect pc 0x004
set opr 13
set opa 8
set data 253
set pair 175
set reg 2
set acc 8
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x004
tock
expect pc 0x004
set opr 3
set opa 14
set data 120
set pair 146
set reg 4
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x004
tock
expect pc 0x004
set opr 5
set opa 2
set data 127
set pair 2
set reg 6
set acc 0
set carry 1
set test 0
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x004
tock
expect pc 0x004
set opr 1
set opa 8
set data 221
set pair 123
set reg 14
set acc 0
set carry 0
set test 1
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x004
tock
expect pc 0x005
set opr 12
set opa 14
set data 45
set pair 44
set reg 7
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x005
tock
expect pc 0x000
set opr 12
set opa 6
set data 222
set pair 155
set reg 5
set acc 0
set carry 1
set test 0
set second 1
set step 1
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x001
set opr 12
set opa 11
set data 71
set pair 192
set reg 4
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x001
tock
expect pc 0x000
set opr 1
set opa 15
set data 107
set pair 252
set reg 9
set acc 0
set carry 0
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 1
set opa 15
set data 157
set pair 111
set reg 7
set acc 5
set carry 1
set test 0
set second 0
set step 0
set exec 0
set reset 0
tick
expect pc 0x000
tock
expect pc 0x000
set opr 5
set opa 0
set data 140
set pair 241
set reg 5
set acc 0
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x000
tock
expect pc 0x08C
set opr 5
set opa 12
set data 32
set pair 116
set reg 3
set acc 0
set carry 1
set test 1
set second 0
set step 0
set exec 1
set reset 0
tick
expect pc 0x08C
tock
expect pc 0x08C
set opr 1
set opa 0
set data 208
set pair 94
set reg 12
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x08C
tock
expect pc 0x08C
set opr 1
set opa 1
set data 130
set pair 226
set reg 8
set acc 5
set carry 0
set test 0
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x08C
tock
expect pc 0x082
set opr 5
set opa 3
set data 72
set pair 216
set reg 2
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x082
tock
expect pc 0x348
set opr 3
set opa 11
set data 215
set pair 213
set reg 14
set acc 0
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x348
tock
expect pc 0x348
set opr 12
set opa 13
set data 70
set pair 175
set reg 13
set acc 7
set carry 0
set test 0
set second 0
set step 1
set exec 0
set reset 0
tick
expect pc 0x348
tock
expect pc 0x349
set opr 12
set opa 10
set data 209
set pair 2
set reg 12
set acc 7
set carry 1
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x349
tock
expect pc 0x349
set opr 12
set opa 11
set data 81
set pair 66
set reg 6
set acc 0
set carry 0
set test 1
set second 1
set step 0
set exec 1
set reset 0
tick
expect pc 0x349
tock
expect pc 0x349
