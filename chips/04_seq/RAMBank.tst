// RAMBank: the same characters written in all four chips and read back, the first and
// last character of each register and every status character in every chip, then
// 160 random cycles (seed 4004). Each write checks out after its tick and its tock.
chip RAMBank
// One address in each chip: chip addr[6..7]
set in 0x1
set addr 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xC
set addr 64
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x3
set addr 128
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x8
set addr 192
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x0
set addr 0
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 64
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 128
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 192
set load 0
set status 0
eval
expect out 0x8
set in 0xA
set addr 42
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xF
set addr 106
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xB
set addr 170
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x4
set addr 234
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x0
set addr 42
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 106
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 170
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 234
set load 0
set status 0
eval
expect out 0x4
set in 0xF
set addr 63
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x9
set addr 127
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 191
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x3
set addr 255
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x0
set addr 63
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 127
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 191
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 255
set load 0
set status 0
eval
expect out 0x3
// First and last character of each register, every status character
set in 0xE
set addr 0
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xE
set in 0x8
set addr 15
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x9
set addr 12
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0x0
set addr 9
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0x4
set addr 14
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0x3
set addr 15
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0x8
set addr 16
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x2
set addr 31
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x9
set addr 28
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0xE
set addr 17
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x7
set addr 26
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xB
set addr 31
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x6
set addr 32
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xA
set addr 47
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xA
set addr 40
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xE
set addr 45
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x5
set addr 46
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0x4
set addr 35
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0x0
set addr 48
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x5
set addr 63
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x5
set in 0x5
set addr 52
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xB
set addr 53
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xE
set addr 54
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0xE
set addr 51
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x1
set addr 64
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x1
set in 0xC
set addr 79
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xB
set addr 72
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xD
set addr 77
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0xA
set addr 74
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x4
set addr 67
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0xB
set addr 80
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xF
set addr 95
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x7
set addr 80
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xA
set addr 89
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xB
set addr 86
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xD
set addr 83
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x6
set addr 96
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 111
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x2
set addr 100
set load 1
set status 1
tick
expect out *
tock
expect out 0x2
set in 0x6
set addr 109
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0x6
set addr 98
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0xA
set addr 111
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xB
set addr 112
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xD
set addr 127
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xD
set in 0x0
set addr 112
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0x6
set addr 113
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0x7
set addr 118
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xD
set addr 115
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x8
set addr 128
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x8
set in 0xF
set addr 143
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x0
set addr 136
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0x0
set addr 141
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0x7
set addr 142
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x5
set addr 131
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0x6
set addr 144
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 159
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x8
set addr 148
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0xD
set addr 145
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0xE
set addr 158
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0xF
set addr 151
set load 1
set status 1
tick
expect out *
tock
expect out 0xF
set in 0x5
set addr 160
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xD
set addr 175
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xB
set addr 160
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xA
set addr 161
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 174
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xE
set addr 171
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0xD
set addr 176
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xA
set addr 191
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xA
set in 0xC
set addr 184
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xD
set addr 189
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x1
set addr 178
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0xC
set addr 183
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xD
set addr 192
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xD
set in 0x8
set addr 207
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x7
set addr 200
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x4
set addr 197
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0x1
set addr 194
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0xD
set addr 195
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0xA
set addr 208
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x2
set addr 223
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xE
set addr 216
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x7
set addr 213
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x0
set addr 214
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0x8
set addr 211
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0x6
set addr 224
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 239
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x5
set addr 236
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0x7
set addr 225
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xA
set addr 226
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xE
set addr 239
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x9
set addr 240
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xC
set addr 255
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xC
set in 0xE
set addr 244
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0xA
set addr 241
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x1
set addr 250
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0xA
set addr 247
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x0
set addr 0
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 15
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 0
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 1
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 2
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 3
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 16
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 31
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 16
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 17
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 18
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 19
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 32
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 47
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 32
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 33
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 34
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 35
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 48
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 63
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 48
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 49
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 50
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 51
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 64
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 79
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 64
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 65
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 66
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 67
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 80
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 95
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 80
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 81
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 82
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 83
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 96
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 111
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 96
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 97
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 98
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 99
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 112
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 127
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 112
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 113
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 114
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 115
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 128
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 143
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 128
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 129
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 130
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 131
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 144
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 159
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 144
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 145
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 146
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 147
set load 0
set status 1
eval
expect out 0xF
set in 0x0
set addr 160
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 175
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 160
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 161
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 162
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 163
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 176
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 191
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 176
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 177
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 178
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 179
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 192
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 207
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 192
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 193
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 194
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 195
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 208
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 223
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 208
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 209
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 210
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 211
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 224
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 239
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 224
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 225
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 226
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 227
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 240
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 255
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 240
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 241
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 242
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 243
set load 0
set status 1
eval
expect out 0xA
// Random cycles
set in 0xE
set addr 161
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x5
set addr 144
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x5
set in 0x1
set addr 246
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xE
set addr 17
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xE
set addr 94
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xB
set addr 166
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xA
set addr 56
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0xA
set in 0x2
set addr 144
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x2
set in 0x9
set addr 151
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x1
set addr 57
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xE
set addr 189
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0xE
set in 0x5
set addr 23
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x1
set addr 180
set load 0
set status 1
tick
expect out 0xC
tock
expect out 0xC
set in 0xA
set addr 254
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xB
set addr 226
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xC
set addr 55
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0xC
set in 0x1
set addr 25
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x3
set addr 239
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x3
set in 0x3
set addr 185
set load 0
set status 1
tick
expect out 0xE
tock
expect out 0xE
set in 0x9
set addr 193
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x9
set addr 115
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xF
set addr 17
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x1
set addr 179
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x5
set addr 120
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x0
set addr 236
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x7
set addr 202
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xF
set addr 47
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xF
set in 0xC
set addr 34
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xB
set addr 127
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0x4
set addr 52
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xC
set addr 225
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xC
set in 0x9
set addr 177
set load 0
set status 1
tick
expect out 0xE
tock
expect out 0xE
set in 0xD
set addr 227
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x5
set addr 21
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x7
set addr 113
set load 0
set status 1
tick
expect out 0x6
tock
expect out 0x6
set in 0x7
set addr 238
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x4
set addr 89
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x4
set in 0x7
set addr 196
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xC
set addr 124
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0xC
set in 0xB
set addr 154
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 8
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x5
set addr 216
set load 0
set status 1
tick
expect out 0xE
tock
expect out 0xE
set in 0x2
set addr 18
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x9
set addr 241
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x9
set in 0x5
set addr 140
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xE
set addr 69
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0xE
set in 0x9
set addr 95
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x9
set in 0x2
set addr 49
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x2
set in 0x9
set addr 46
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x3
set addr 38
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xB
set addr 16
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xB
set in 0x2
set addr 207
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x2
set in 0x7
set addr 102
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x9
set addr 69
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xE
set addr 92
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xE
set in 0xA
set addr 205
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xA
set addr 141
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x4
set addr 201
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x5
set addr 180
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x2
set addr 70
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x8
set addr 221
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0xE
set addr 104
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0xE
set in 0xB
set addr 28
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xB
set in 0xB
set addr 223
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x5
set addr 232
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x9
set addr 179
set load 0
set status 1
tick
expect out 0xC
tock
expect out 0xC
set in 0x7
set addr 91
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x2
set addr 130
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x7
set addr 161
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xF
set addr 196
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xF
set in 0x2
set addr 235
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x3
set addr 20
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x3
set in 0x4
set addr 9
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x1
set addr 218
set load 0
set status 1
tick
expect out 0x0
tock
expect out 0x0
set in 0x4
set addr 201
set load 0
set status 0
tick
expect out 0x4
tock
expect out 0x4
set in 0xD
set addr 61
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x7
set addr 190
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x3
set addr 123
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xA
set addr 141
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0xA
set in 0xE
set addr 96
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xE
set in 0xF
set addr 42
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xF
set in 0xF
set addr 112
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xF
set in 0xA
set addr 243
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x8
set addr 73
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x8
set addr 39
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x9
set addr 32
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x9
set in 0x5
set addr 236
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x5
set in 0x7
set addr 170
set load 0
set status 1
tick
expect out 0x7
tock
expect out 0x7
set in 0xE
set addr 243
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xB
set addr 238
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x0
set addr 73
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x7
set addr 227
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x7
set in 0x1
set addr 72
set load 0
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0x7
set addr 17
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x5
set addr 162
set load 0
set status 1
tick
expect out 0x7
tock
expect out 0x7
set in 0xC
set addr 144
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x1
set addr 114
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x9
set addr 131
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x1
set addr 109
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x7
set addr 3
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xA
set addr 186
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xE
set addr 213
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xF
set addr 195
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x1
set addr 109
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xF
set addr 1
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x4
set addr 59
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xD
set addr 97
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0xD
set in 0x6
set addr 66
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x9
set addr 226
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x9
set in 0xD
set addr 217
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xD
set in 0xE
set addr 143
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0xE
set in 0xC
set addr 43
set load 0
set status 1
tick
expect out 0x4
tock
expect out 0x4
set in 0xE
set addr 31
set load 0
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0xC
set addr 3
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xC
set in 0x9
set addr 116
set load 0
set status 1
tick
expect out 0xC
tock
expect out 0xC
set in 0x2
set addr 177
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xA
set addr 72
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0xA
set in 0x7
set addr 31
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x7
set in 0x4
set addr 86
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xD
set addr 54
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xE
set addr 39
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xC
set addr 245
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x0
set addr 241
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x6
set addr 237
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x0
set addr 125
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x0
set addr 84
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xB
set addr 51
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x9
set addr 204
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x0
set addr 187
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x9
set addr 227
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x9
set in 0xB
set addr 241
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xB
set in 0xF
set addr 101
set load 0
set status 1
tick
expect out 0xD
tock
expect out 0xD
set in 0x1
set addr 135
set load 0
set status 1
tick
expect out 0xE
tock
expect out 0xE
set in 0xC
set addr 29
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x4
set addr 82
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x0
set addr 31
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x0
set in 0x7
set addr 55
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xC
set addr 138
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x1
set addr 120
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0x1
set in 0x0
set addr 155
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0xA
set addr 23
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xA
set in 0x6
set addr 118
set load 0
set status 1
tick
expect out 0x7
tock
expect out 0x7
set in 0x8
set addr 113
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0xB
set addr 106
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x8
set addr 133
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x4
set addr 248
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xC
set addr 135
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x7
set addr 21
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x7
set in 0xA
set addr 152
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0xA
set in 0xD
set addr 141
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xD
set in 0x4
set addr 120
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x9
set addr 218
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 6
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x5
set addr 138
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xF
set addr 41
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x0
set addr 248
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x0
set in 0x8
set addr 115
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x8
set in 0x1
set addr 189
set load 0
set status 0
tick
expect out *
tock
expect out *
set in 0x8
set addr 178
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0xC
set addr 76
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0xC
