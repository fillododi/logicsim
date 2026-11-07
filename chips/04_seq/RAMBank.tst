// RAMBank: all 256 main and 64 status characters of the four chips: fill every cell, rewrite each with a different value, read them all back;
// status characters named with addr[2..3] set to anything. Then 160 random
// cycles (seed 4004). Each write checks out after its tick (the old value)
// and after its tock.
chip RAMBank
// Fill: every cell once
set in 0xA
set addr 0
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x2
set addr 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xB
set addr 2
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xE
set addr 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x5
set addr 4
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x7
set addr 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x6
set addr 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x0
set addr 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x2
set addr 8
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x8
set addr 9
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x6
set addr 10
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 11
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xE
set addr 12
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x5
set addr 13
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x1
set addr 14
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x7
set addr 15
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x1
set addr 16
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xA
set addr 17
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xF
set addr 18
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xE
set addr 19
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x9
set addr 20
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xC
set addr 21
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x4
set addr 22
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xE
set addr 23
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x1
set addr 24
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xA
set addr 25
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x8
set addr 26
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x1
set addr 27
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x5
set addr 28
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xA
set addr 29
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xA
set addr 30
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xE
set addr 31
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xE
set addr 32
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x1
set addr 33
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x1
set addr 34
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x9
set addr 35
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x5
set addr 36
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xC
set addr 37
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xE
set addr 38
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xF
set addr 39
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x1
set addr 40
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x6
set addr 41
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x1
set addr 42
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xE
set addr 43
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xB
set addr 44
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x5
set addr 45
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xE
set addr 46
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x3
set addr 47
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x1
set addr 48
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xA
set addr 49
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xB
set addr 50
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xB
set addr 51
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xB
set addr 52
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x3
set addr 53
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xA
set addr 54
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 55
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xF
set addr 56
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xE
set addr 57
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x3
set addr 58
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x9
set addr 59
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x2
set addr 60
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x3
set addr 61
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xC
set addr 62
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x9
set addr 63
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x9
set addr 64
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x9
set addr 65
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x0
set addr 66
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x3
set addr 67
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x1
set addr 68
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x1
set addr 69
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xA
set addr 70
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x3
set addr 71
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xB
set addr 72
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xE
set addr 73
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x7
set addr 74
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x3
set addr 75
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x1
set addr 76
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x5
set addr 77
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xF
set addr 78
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xD
set addr 79
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xB
set addr 80
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 81
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x8
set addr 82
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x7
set addr 83
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xF
set addr 84
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xA
set addr 85
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xE
set addr 86
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xB
set addr 87
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x6
set addr 88
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xD
set addr 89
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x9
set addr 90
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x3
set addr 91
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xC
set addr 92
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x0
set addr 93
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x7
set addr 94
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x9
set addr 95
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x1
set addr 96
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x1
set addr 97
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xD
set addr 98
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x0
set addr 99
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0xE
set addr 100
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x3
set addr 101
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xD
set addr 102
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xB
set addr 103
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x3
set addr 104
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x9
set addr 105
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xE
set addr 106
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xC
set addr 107
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x9
set addr 108
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 109
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x7
set addr 110
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x7
set addr 111
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x9
set addr 112
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 113
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 114
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x1
set addr 115
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xF
set addr 116
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xF
set addr 117
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xC
set addr 118
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xB
set addr 119
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 120
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xD
set addr 121
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xE
set addr 122
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xB
set addr 123
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x7
set addr 124
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x5
set addr 125
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xE
set addr 126
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x0
set addr 127
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x4
set addr 128
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x4
set addr 129
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xB
set addr 130
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xC
set addr 131
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x7
set addr 132
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xF
set addr 133
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x2
set addr 134
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x2
set addr 135
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xF
set addr 136
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xD
set addr 137
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xC
set addr 138
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x4
set addr 139
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x2
set addr 140
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xC
set addr 141
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xA
set addr 142
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xC
set addr 143
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x0
set addr 144
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x7
set addr 145
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xB
set addr 146
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xE
set addr 147
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xF
set addr 148
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x3
set addr 149
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x4
set addr 150
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xE
set addr 151
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xE
set addr 152
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xC
set addr 153
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x4
set addr 154
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x7
set addr 155
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xB
set addr 156
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xB
set addr 157
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x9
set addr 158
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x4
set addr 159
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x3
set addr 160
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xE
set addr 161
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xD
set addr 162
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xB
set addr 163
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xC
set addr 164
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x1
set addr 165
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x5
set addr 166
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xF
set addr 167
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x3
set addr 168
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x2
set addr 169
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x7
set addr 170
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x7
set addr 171
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x9
set addr 172
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x0
set addr 173
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0xC
set addr 174
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xE
set addr 175
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x7
set addr 176
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xA
set addr 177
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 178
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x2
set addr 179
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x5
set addr 180
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x4
set addr 181
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x5
set addr 182
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xD
set addr 183
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xC
set addr 184
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x7
set addr 185
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x7
set addr 186
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x7
set addr 187
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xC
set addr 188
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x4
set addr 189
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x8
set addr 190
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x9
set addr 191
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 192
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xD
set addr 193
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xE
set addr 194
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x1
set addr 195
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x0
set addr 196
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x1
set addr 197
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x4
set addr 198
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x3
set addr 199
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xD
set addr 200
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x5
set addr 201
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x7
set addr 202
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x5
set addr 203
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x1
set addr 204
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x2
set addr 205
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xB
set addr 206
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xE
set addr 207
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xF
set addr 208
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x9
set addr 209
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x8
set addr 210
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0xE
set addr 211
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x7
set addr 212
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x8
set addr 213
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x5
set addr 214
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x9
set addr 215
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x9
set addr 216
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x6
set addr 217
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x4
set addr 218
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xE
set addr 219
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x4
set addr 220
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xF
set addr 221
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x5
set addr 222
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x9
set addr 223
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x8
set addr 224
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x5
set addr 225
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xE
set addr 226
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x1
set addr 227
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x3
set addr 228
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x2
set addr 229
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x4
set addr 230
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xD
set addr 231
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x7
set addr 232
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x0
set addr 233
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x2
set addr 234
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x9
set addr 235
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 236
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xC
set addr 237
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xB
set addr 238
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x2
set addr 239
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x3
set addr 240
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xF
set addr 241
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x1
set addr 242
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xB
set addr 243
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x5
set addr 244
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xD
set addr 245
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xC
set addr 246
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x2
set addr 247
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xE
set addr 248
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x1
set addr 249
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x6
set addr 250
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x7
set addr 251
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x5
set addr 252
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x0
set addr 253
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x4
set addr 254
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x9
set addr 255
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x5
set addr 0
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xE
set addr 5
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x2
set addr 14
set load 1
set status 1
tick
expect out *
tock
expect out 0x2
set in 0x0
set addr 11
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0xC
set addr 24
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xA
set addr 29
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xD
set addr 18
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x9
set addr 19
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0x4
set addr 32
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0x8
set addr 37
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0xA
set addr 38
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xC
set addr 39
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0x9
set addr 48
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0xF
set addr 61
set load 1
set status 1
tick
expect out *
tock
expect out 0xF
set in 0xC
set addr 58
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0x4
set addr 63
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0xF
set addr 72
set load 1
set status 1
tick
expect out *
tock
expect out 0xF
set in 0x3
set addr 65
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0x4
set addr 78
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0xB
set addr 67
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x5
set addr 92
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xD
set addr 85
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x4
set addr 82
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0x2
set addr 87
set load 1
set status 1
tick
expect out *
tock
expect out 0x2
set in 0xB
set addr 100
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xB
set addr 109
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xD
set addr 102
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x8
set addr 107
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0xE
set addr 112
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x3
set addr 125
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0x6
set addr 126
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 127
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x7
set addr 132
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x8
set addr 141
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0x1
set addr 134
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0xB
set addr 143
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 144
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0x0
set addr 153
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0xE
set addr 146
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x9
set addr 155
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0xD
set addr 172
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0xB
set addr 165
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x8
set addr 170
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0xE
set addr 175
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x5
set addr 188
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xB
set addr 185
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x6
set addr 186
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0x7
set addr 191
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xB
set addr 204
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x9
set addr 205
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0x5
set addr 194
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xD
set addr 195
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x5
set addr 212
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0x7
set addr 221
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x1
set addr 222
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0x8
set addr 219
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0x2
set addr 232
set load 1
set status 1
tick
expect out *
tock
expect out 0x2
set in 0xE
set addr 229
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x3
set addr 230
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0xA
set addr 231
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 240
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x6
set addr 241
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0xC
set addr 242
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xF
set addr 255
set load 1
set status 1
tick
expect out *
tock
expect out 0xF
// Rewrite: every cell again, each with a different value
set in 0xE
set addr 0
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xE
set in 0xD
set addr 1
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xD
set in 0xE
set addr 2
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xE
set in 0x6
set addr 3
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x6
set in 0x1
set addr 4
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x1
set in 0x2
set addr 5
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x2
set in 0xF
set addr 6
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xF
set in 0xE
set addr 7
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0xF
set addr 8
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xF
set in 0x0
set addr 9
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x0
set in 0x3
set addr 10
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x3
set in 0x7
set addr 11
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x7
set in 0x0
set addr 12
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x0
set in 0x2
set addr 13
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x2
set in 0xF
set addr 14
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0xA
set addr 15
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xA
set in 0x2
set addr 16
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x2
set in 0xC
set addr 17
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xC
set in 0x1
set addr 18
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x1
set in 0xB
set addr 19
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xB
set in 0xE
set addr 20
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xE
set in 0x9
set addr 21
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x9
set in 0x5
set addr 22
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x5
set in 0x1
set addr 23
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x1
set in 0x7
set addr 24
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x7
set in 0x5
set addr 25
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x5
set in 0x6
set addr 26
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0xA
set addr 27
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xA
set in 0xC
set addr 28
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xC
set in 0xB
set addr 29
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xB
set in 0xE
set addr 30
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xE
set in 0xF
set addr 31
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xF
set in 0x9
set addr 32
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x9
set in 0x2
set addr 33
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x2
set in 0xE
set addr 34
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xE
set in 0x0
set addr 35
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x0
set in 0x4
set addr 36
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x4
set in 0x6
set addr 37
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x6
set in 0x1
set addr 38
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x1
set in 0xC
set addr 39
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xC
set in 0xA
set addr 40
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xA
set in 0x1
set addr 41
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x1
set in 0xC
set addr 42
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xC
set in 0x0
set addr 43
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x0
set in 0x2
set addr 44
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x2
set in 0xF
set addr 45
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xF
set in 0x8
set addr 46
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x8
set in 0x6
set addr 47
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x6
set in 0xE
set addr 48
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xE
set in 0x0
set addr 49
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x0
set in 0x6
set addr 50
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x6
set in 0xF
set addr 51
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xF
set in 0x3
set addr 52
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x3
set in 0xE
set addr 53
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xE
set in 0x9
set addr 54
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x9
set in 0x1
set addr 55
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x1
set in 0x3
set addr 56
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x3
set in 0xD
set addr 57
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xD
set in 0x5
set addr 58
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x5
set in 0x1
set addr 59
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x1
set in 0x1
set addr 60
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x1
set in 0x4
set addr 61
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x4
set in 0x1
set addr 62
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x1
set in 0xE
set addr 63
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xE
set in 0xF
set addr 64
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xF
set in 0xA
set addr 65
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xA
set in 0xE
set addr 66
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0xB
set addr 67
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xB
set in 0xD
set addr 68
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xD
set in 0xC
set addr 69
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xC
set in 0xE
set addr 70
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xE
set in 0xB
set addr 71
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xB
set in 0x5
set addr 72
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x5
set in 0x2
set addr 73
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x2
set in 0x4
set addr 74
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x4
set in 0x5
set addr 75
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x5
set in 0xD
set addr 76
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xD
set in 0x4
set addr 77
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x4
set in 0x9
set addr 78
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x9
set in 0x5
set addr 79
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x5
set in 0x2
set addr 80
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x2
set in 0x3
set addr 81
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x3
set in 0x2
set addr 82
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x2
set in 0x1
set addr 83
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x1
set in 0x3
set addr 84
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x3
set in 0x8
set addr 85
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x8
set in 0x8
set addr 86
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x8
set in 0x5
set addr 87
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x5
set in 0xE
set addr 88
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xE
set in 0xB
set addr 89
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0xA
set addr 90
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xA
set in 0x8
set addr 91
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x8
set in 0x5
set addr 92
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x5
set in 0x9
set addr 93
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x9
set in 0xF
set addr 94
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xF
set in 0xF
set addr 95
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xF
set in 0x6
set addr 96
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x6
set in 0x7
set addr 97
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x7
set in 0x6
set addr 98
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x6
set in 0xF
set addr 99
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xF
set in 0xC
set addr 100
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0x6
set addr 101
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x6
set in 0x2
set addr 102
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x2
set in 0x6
set addr 103
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x6
set in 0x0
set addr 104
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x0
set in 0x8
set addr 105
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x8
set in 0xB
set addr 106
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xB
set in 0xA
set addr 107
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x2
set addr 108
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x2
set in 0x4
set addr 109
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x4
set in 0x9
set addr 110
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x9
set in 0xC
set addr 111
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xC
set in 0x8
set addr 112
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x8
set in 0x7
set addr 113
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x7
set in 0xF
set addr 114
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0xD
set addr 115
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xD
set in 0xD
set addr 116
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0x1
set addr 117
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x1
set in 0x1
set addr 118
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x1
set in 0xD
set addr 119
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xD
set in 0x9
set addr 120
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x9
set in 0x2
set addr 121
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x2
set in 0xD
set addr 122
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xD
set in 0x3
set addr 123
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x3
set in 0x4
set addr 124
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x4
set in 0x8
set addr 125
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x8
set in 0x5
set addr 126
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x5
set in 0x5
set addr 127
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x5
set in 0x9
set addr 128
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x9
set in 0x8
set addr 129
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x8
set in 0xA
set addr 130
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xA
set in 0x2
set addr 131
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x2
set in 0x6
set addr 132
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x6
set in 0xE
set addr 133
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xE
set in 0x1
set addr 134
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x1
set in 0x6
set addr 135
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x6
set in 0x2
set addr 136
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x2
set in 0x4
set addr 137
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x4
set in 0x7
set addr 138
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x7
set in 0x8
set addr 139
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x8
set in 0x0
set addr 140
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0x6
set addr 141
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x6
set in 0x2
set addr 142
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x2
set in 0xA
set addr 143
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x8
set addr 144
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x8
set in 0x2
set addr 145
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x2
set in 0x0
set addr 146
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x0
set in 0xF
set addr 147
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xF
set in 0xA
set addr 148
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xA
set in 0xB
set addr 149
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xB
set in 0x1
set addr 150
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x1
set in 0x4
set addr 151
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x4
set in 0x0
set addr 152
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x0
set in 0xB
set addr 153
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xB
set in 0x1
set addr 154
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x1
set in 0x1
set addr 155
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x1
set in 0xE
set addr 156
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xE
set in 0x4
set addr 157
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x4
set in 0xA
set addr 158
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xA
set in 0xF
set addr 159
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0xF
set in 0xD
set addr 160
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xD
set in 0xF
set addr 161
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xF
set in 0x9
set addr 162
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x9
set in 0x6
set addr 163
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x6
set in 0x7
set addr 164
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x7
set in 0x9
set addr 165
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x9
set in 0x9
set addr 166
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x9
set in 0xB
set addr 167
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xB
set in 0x9
set addr 168
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x9
set in 0x7
set addr 169
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x7
set in 0x0
set addr 170
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x0
set in 0x6
set addr 171
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x6
set in 0xC
set addr 172
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xC
set in 0x1
set addr 173
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x1
set in 0x1
set addr 174
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x1
set in 0xB
set addr 175
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xB
set in 0x6
set addr 176
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x6
set in 0x1
set addr 177
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x1
set in 0x8
set addr 178
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x8
set in 0x6
set addr 179
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x6
set in 0xD
set addr 180
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xD
set in 0x1
set addr 181
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x1
set in 0x0
set addr 182
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x0
set in 0x1
set addr 183
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x1
set in 0x2
set addr 184
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x2
set in 0x4
set addr 185
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x4
set in 0x5
set addr 186
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0xA
set addr 187
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xA
set in 0x0
set addr 188
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x0
set in 0x0
set addr 189
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x0
set in 0x6
set addr 190
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0xC
set addr 191
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xC
set in 0x4
set addr 192
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x4
set in 0x6
set addr 193
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x6
set in 0x3
set addr 194
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x3
set in 0xA
set addr 195
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xA
set in 0x7
set addr 196
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x7
set in 0xB
set addr 197
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xB
set in 0x7
set addr 198
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x7
set in 0xF
set addr 199
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xF
set in 0x2
set addr 200
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x2
set in 0x2
set addr 201
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x2
set in 0xB
set addr 202
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xB
set in 0x6
set addr 203
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x6
set in 0x8
set addr 204
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x8
set in 0xC
set addr 205
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xC
set in 0x4
set addr 206
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x4
set in 0xC
set addr 207
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0x4
set addr 208
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x4
set in 0xE
set addr 209
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xE
set in 0xF
set addr 210
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xF
set in 0xD
set addr 211
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xD
set in 0x0
set addr 212
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x0
set in 0x4
set addr 213
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x4
set in 0x9
set addr 214
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x9
set in 0x3
set addr 215
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x3
set in 0xA
set addr 216
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xA
set in 0x4
set addr 217
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0x1
set addr 218
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x1
set in 0x8
set addr 219
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x8
set in 0x1
set addr 220
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x1
set in 0x0
set addr 221
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x0
set in 0x2
set addr 222
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x2
set in 0x5
set addr 223
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x5
set in 0xC
set addr 224
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xC
set in 0xE
set addr 225
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xE
set in 0x0
set addr 226
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x0
set in 0x5
set addr 227
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x5
set in 0xC
set addr 228
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xC
set in 0x8
set addr 229
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x8
set in 0xA
set addr 230
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0xA
set in 0x6
set addr 231
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x6
set in 0x3
set addr 232
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x3
set in 0xC
set addr 233
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xC
set in 0x9
set addr 234
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x9
set in 0x1
set addr 235
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x1
set in 0x1
set addr 236
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x1
set in 0x3
set addr 237
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x3
set in 0x7
set addr 238
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x7
set in 0x4
set addr 239
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x4
set in 0xA
set addr 240
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xA
set in 0x7
set addr 241
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x7
set in 0x7
set addr 242
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x7
set in 0x2
set addr 243
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x2
set in 0xD
set addr 244
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xD
set in 0xB
set addr 245
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0x0
set addr 246
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x0
set in 0xF
set addr 247
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xF
set in 0xF
set addr 248
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xF
set in 0xD
set addr 249
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xD
set in 0xE
set addr 250
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xE
set in 0xB
set addr 251
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xB
set in 0xE
set addr 252
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xE
set in 0x1
set addr 253
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x1
set in 0xC
set addr 254
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0xC
set in 0x8
set addr 255
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x8
set in 0xA
set addr 0
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0xA
set in 0x4
set addr 5
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x4
set in 0xF
set addr 14
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0xF
set in 0x2
set addr 11
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0x2
set in 0xA
set addr 24
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0xA
set in 0x5
set addr 29
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x5
set in 0x9
set addr 18
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x9
set in 0x3
set addr 19
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x3
set in 0x0
set addr 32
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x0
set in 0xB
set addr 37
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0xB
set in 0xD
set addr 38
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0xD
set in 0x6
set addr 39
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0x6
set in 0x5
set addr 48
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x5
set in 0x9
set addr 61
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0x9
set in 0x0
set addr 58
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0x0
set in 0x2
set addr 63
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x2
set in 0xA
set addr 72
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0xA
set in 0x2
set addr 65
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x2
set in 0xB
set addr 78
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0xB
set in 0xD
set addr 67
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0xD
set in 0x6
set addr 92
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x6
set in 0x2
set addr 85
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x2
set in 0x8
set addr 82
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x8
set in 0x5
set addr 87
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x5
set in 0xF
set addr 100
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0xF
set in 0x9
set addr 109
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x9
set in 0x3
set addr 102
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x3
set in 0x4
set addr 107
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x4
set in 0x6
set addr 112
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x6
set in 0x8
set addr 125
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x8
set in 0x9
set addr 126
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x9
set in 0x4
set addr 127
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x4
set in 0x0
set addr 132
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x0
set in 0x4
set addr 141
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x4
set in 0x8
set addr 134
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x8
set in 0x5
set addr 143
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x5
set in 0xD
set addr 144
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0xD
set in 0xE
set addr 153
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0xE
set in 0x8
set addr 146
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x8
set in 0x5
set addr 155
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x5
set in 0x7
set addr 172
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x7
set in 0x2
set addr 165
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x2
set in 0xA
set addr 170
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0xA
set in 0x4
set addr 175
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x4
set in 0xC
set addr 188
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0xC
set in 0x0
set addr 185
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x0
set in 0x4
set addr 186
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x4
set in 0xF
set addr 191
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xF
set in 0xE
set addr 204
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0xE
set in 0xA
set addr 205
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xA
set in 0x6
set addr 194
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x6
set in 0x8
set addr 195
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x8
set in 0x7
set addr 212
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x7
set in 0x5
set addr 221
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x5
set in 0x8
set addr 222
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x8
set in 0xB
set addr 219
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0xB
set in 0x5
set addr 232
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x5
set in 0x5
set addr 229
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x5
set in 0x4
set addr 230
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x4
set in 0x2
set addr 231
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x2
set in 0xB
set addr 240
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xB
set in 0x8
set addr 241
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x8
set in 0x8
set addr 242
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0x8
set in 0x3
set addr 255
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0x3
// Read everything back
set in 0x0
set addr 0
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 1
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 2
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 3
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 4
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 5
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 6
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 7
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 8
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 9
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 10
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 11
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 12
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 13
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 14
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 15
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 16
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 17
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 18
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 19
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 20
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 21
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 22
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 23
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 24
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 25
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 26
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 27
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 28
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 29
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 30
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 31
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 32
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 33
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 34
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 35
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 36
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 37
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 38
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 39
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 40
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 41
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 42
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 43
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 44
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 45
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 46
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 47
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 48
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 49
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 50
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 51
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 52
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 53
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 54
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 55
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 56
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 57
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 58
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 59
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 60
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 61
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 62
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 63
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 64
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 65
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 66
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 67
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 68
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 69
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 70
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 71
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 72
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 73
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 74
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 75
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 76
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 77
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 78
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 79
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 80
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 81
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 82
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 83
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 84
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 85
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 86
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 87
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 88
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 89
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 90
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 91
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 92
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 93
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 94
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 95
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 96
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 97
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 98
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 99
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 100
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 101
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 102
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 103
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 104
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 105
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 106
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 107
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 108
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 109
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 110
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 111
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 112
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 113
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 114
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 115
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 116
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 117
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 118
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 119
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 120
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 121
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 122
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 123
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 124
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 125
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 126
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 127
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 128
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 129
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 130
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 131
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 132
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 133
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 134
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 135
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 136
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 137
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 138
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 139
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 140
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 141
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 142
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 143
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 144
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 145
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 146
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 147
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 148
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 149
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 150
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 151
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 152
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 153
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 154
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 155
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 156
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 157
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 158
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 159
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 160
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 161
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 162
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 163
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 164
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 165
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 166
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 167
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 168
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 169
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 170
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 171
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 172
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 173
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 174
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 175
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 176
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 177
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 178
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 179
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 180
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 181
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 182
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 183
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 184
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 185
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 186
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 187
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 188
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 189
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 190
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 191
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 192
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 193
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 194
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 195
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 196
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 197
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 198
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 199
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 200
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 201
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 202
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 203
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 204
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 205
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 206
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 207
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 208
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 209
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 210
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 211
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 212
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 213
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 214
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 215
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 216
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 217
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 218
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 219
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 220
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 221
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 222
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 223
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 224
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 225
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 226
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 227
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 228
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 229
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 230
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 231
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 232
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 233
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 234
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 235
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 236
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 237
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 238
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 239
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 240
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 241
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 242
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 243
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 244
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 245
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 246
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 247
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 248
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 249
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 250
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 251
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 252
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 253
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 254
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 255
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 0
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 5
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 14
set load 0
set status 1
eval
expect out 0xF
set in 0x0
set addr 11
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 24
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 29
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 18
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 19
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 32
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 37
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 38
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 39
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 48
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 61
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 58
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 63
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 72
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 65
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 78
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 67
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 92
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 85
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 82
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 87
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 100
set load 0
set status 1
eval
expect out 0xF
set in 0x0
set addr 109
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 102
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 107
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 112
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 125
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 126
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 127
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 132
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 141
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 134
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 143
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 144
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 153
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 146
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 155
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 172
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 165
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 170
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 175
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 188
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 185
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 186
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 191
set load 0
set status 1
eval
expect out 0xF
set in 0x0
set addr 204
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 205
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 194
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 195
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 212
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 221
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 222
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 219
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 232
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 229
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 230
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 231
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 240
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 241
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 242
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 255
set load 0
set status 1
eval
expect out 0x3
// 160 random cycles, load on about 60% of them
set in 0x8
set addr 187
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0x8
set in 0x6
set addr 147
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x6
set in 0x2
set addr 177
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0xA
set addr 72
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x7
set addr 31
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x7
set in 0x4
set addr 86
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0xD
set addr 54
set load 0
set status 1
tick
expect out 0x0
tock
expect out 0x0
set in 0xE
set addr 39
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0xE
set in 0xC
set addr 245
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x0
set addr 241
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x0
set in 0x6
set addr 237
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x6
set in 0x0
set addr 125
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x0
set addr 84
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x0
set in 0xB
set addr 51
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x9
set addr 204
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x9
set in 0x0
set addr 187
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x0
set in 0x9
set addr 227
set load 0
set status 1
tick
expect out 0x2
tock
expect out 0x2
set in 0xB
set addr 241
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xB
set in 0xF
set addr 101
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xF
set in 0x1
set addr 135
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x1
set in 0xC
set addr 29
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x4
set addr 82
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
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
set load 0
set status 1
tick
expect out 0x2
tock
expect out 0x2
set in 0xC
set addr 138
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0x1
set addr 120
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x1
set in 0x0
set addr 155
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x0
set in 0xA
set addr 23
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x6
set addr 118
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x6
set in 0x8
set addr 113
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0xB
set addr 106
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x8
set addr 133
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x8
set in 0x4
set addr 248
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0xC
set addr 135
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xC
set in 0x7
set addr 21
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xA
set addr 152
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0xA
set in 0xD
set addr 141
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0xD
set in 0x4
set addr 120
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x4
set in 0x9
set addr 218
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x9
set in 0xB
set addr 6
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x5
set addr 138
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0xF
set addr 41
set load 0
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0x0
set addr 248
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x0
set in 0x8
set addr 115
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x8
set in 0x1
set addr 189
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x1
set in 0x8
set addr 178
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xC
set addr 76
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xC
set in 0x3
set addr 178
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xA
set addr 101
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xA
set in 0x8
set addr 175
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x8
set in 0x3
set addr 195
set load 0
set status 0
tick
expect out 0xA
tock
expect out 0xA
set in 0x3
set addr 82
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0xC
set addr 150
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xC
set in 0x7
set addr 101
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x7
set in 0x9
set addr 119
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0xC
set addr 114
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x1
set addr 67
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x5
set addr 181
set load 0
set status 1
tick
expect out 0x0
tock
expect out 0x0
set in 0x1
set addr 106
set load 0
set status 1
tick
expect out 0x3
tock
expect out 0x3
set in 0x9
set addr 96
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0x9
set in 0xA
set addr 195
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0xF
set addr 144
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xF
set in 0xF
set addr 128
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xE
set addr 64
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0xF
set addr 196
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x9
set addr 230
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x9
set in 0xD
set addr 112
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xD
set in 0xD
set addr 20
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x9
set addr 24
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x9
set in 0xB
set addr 168
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0x1
set addr 126
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x1
set in 0xA
set addr 18
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xA
set in 0xC
set addr 231
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x0
set addr 248
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x0
set addr 186
set load 0
set status 1
tick
expect out 0x4
tock
expect out 0x4
set in 0x1
set addr 35
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x1
set in 0xB
set addr 150
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0x3
set addr 138
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0xF
set addr 137
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0xF
set in 0x3
set addr 61
set load 0
set status 1
tick
expect out 0x9
tock
expect out 0x9
set in 0x8
set addr 103
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x8
set in 0x9
set addr 55
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x9
set in 0x0
set addr 216
set load 0
set status 1
tick
expect out 0x7
tock
expect out 0x7
set in 0xC
set addr 188
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x7
set addr 144
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x7
set in 0xB
set addr 194
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xB
set in 0x4
set addr 231
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0x9
set addr 125
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x9
set addr 207
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0x8
set addr 165
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x8
set in 0x1
set addr 35
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x2
set addr 24
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x2
set in 0x9
set addr 16
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x9
set in 0xB
set addr 73
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0xD
set addr 27
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xD
set in 0x9
set addr 35
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x9
set in 0x6
set addr 46
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x6
set in 0xF
set addr 102
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0xF
set in 0xC
set addr 201
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0xC
set in 0x9
set addr 20
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0x1
set addr 76
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x5
set addr 112
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x5
set in 0x2
set addr 107
set load 0
set status 0
tick
expect out 0xA
tock
expect out 0xA
set in 0x9
set addr 164
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x4
set addr 46
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x4
set in 0x0
set addr 33
set load 0
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0x5
set addr 118
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x5
set in 0x4
set addr 215
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x4
set in 0x1
set addr 156
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0xF
set addr 23
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x7
set addr 191
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xD
set addr 230
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xD
set in 0x9
set addr 108
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x9
set in 0x8
set addr 103
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x9
set addr 112
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0x3
set addr 107
set load 0
set status 1
tick
expect out 0x4
tock
expect out 0x4
set in 0x4
set addr 205
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x4
set in 0xE
set addr 233
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xC
set addr 155
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0xA
set addr 1
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0xA
set in 0x3
set addr 191
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xD
set addr 123
set load 0
set status 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x8
set addr 123
set load 0
set status 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x3
set addr 35
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x3
set in 0x2
set addr 189
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x2
set in 0xD
set addr 125
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0xE
set addr 27
set load 0
set status 1
tick
expect out 0x0
tock
expect out 0x0
set in 0x8
set addr 183
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x0
set addr 177
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x0
set in 0x3
set addr 113
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x3
set in 0xA
set addr 240
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xA
set in 0x5
set addr 231
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x5
set in 0xD
set addr 99
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0xD
set addr 159
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0x0
set addr 205
set load 0
set status 0
tick
expect out 0x4
tock
expect out 0x4
set in 0xC
set addr 45
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xC
set in 0x2
set addr 111
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x2
set in 0x8
set addr 91
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xF
set addr 30
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xF
set in 0x2
set addr 36
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x2
set in 0x9
set addr 200
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x5
set addr 123
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x5
set in 0x7
set addr 218
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x7
set in 0xB
set addr 58
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xB
set in 0x5
set addr 49
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0xF
set addr 31
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x8
set addr 184
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0x8
set in 0x6
set addr 176
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x6
set in 0x2
set addr 110
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0x1
set addr 199
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x8
set addr 7
set load 0
set status 1
tick
expect out 0x2
tock
expect out 0x2
set in 0x3
set addr 146
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x3
set addr 238
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x3
set addr 81
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x3
set in 0x3
set addr 135
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x3
set in 0xA
set addr 162
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x9
set addr 3
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x9
set in 0xA
set addr 181
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xA
set in 0x8
set addr 70
set load 0
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0x8
set addr 217
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x8
