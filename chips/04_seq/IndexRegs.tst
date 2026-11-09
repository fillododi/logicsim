// IndexRegs: each register and each pair written and read back, a cycle with neither
// load, load and loadpair together, then 64 random cycles (seed 4004), all with reset
// at 0. Each clock cycle checks out and pairout after its tick (still the old value) and
// after its tock. Then reset: it wins over load and loadpair and clears all 16 registers.
chip IndexRegs
set reset 0
// Each register on its own, the high half of in ignored
set in 0x8F
set addr 0
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0xF
expect pairout *
set in 0x9E
set addr 1
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0xE
expect pairout 0xFE
set in 0xAD
set addr 2
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0xD
expect pairout *
set in 0xBC
set addr 3
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0xC
expect pairout 0xDC
set in 0xCB
set addr 4
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0xB
expect pairout *
set in 0xDA
set addr 5
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0xA
expect pairout 0xBA
set in 0xE9
set addr 6
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x9
expect pairout *
set in 0xF8
set addr 7
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x8
expect pairout 0x98
set in 0x07
set addr 8
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x7
expect pairout *
set in 0x16
set addr 9
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x6
expect pairout 0x76
set in 0x25
set addr 10
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x5
expect pairout *
set in 0x34
set addr 11
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x4
expect pairout 0x54
set in 0x43
set addr 12
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x3
expect pairout *
set in 0x52
set addr 13
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x2
expect pairout 0x32
set in 0x61
set addr 14
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x1
expect pairout *
set in 0x70
set addr 15
set load 1
set loadpair 0
tick
expect out *
expect pairout *
tock
expect out 0x0
expect pairout 0x10
// Read every register back, with load off
set addr 0
set load 0
set loadpair 0
eval
expect out 0xF
expect pairout 0xFE
set addr 1
set load 0
set loadpair 0
eval
expect out 0xE
expect pairout 0xFE
set addr 2
set load 0
set loadpair 0
eval
expect out 0xD
expect pairout 0xDC
set addr 3
set load 0
set loadpair 0
eval
expect out 0xC
expect pairout 0xDC
set addr 4
set load 0
set loadpair 0
eval
expect out 0xB
expect pairout 0xBA
set addr 5
set load 0
set loadpair 0
eval
expect out 0xA
expect pairout 0xBA
set addr 6
set load 0
set loadpair 0
eval
expect out 0x9
expect pairout 0x98
set addr 7
set load 0
set loadpair 0
eval
expect out 0x8
expect pairout 0x98
set addr 8
set load 0
set loadpair 0
eval
expect out 0x7
expect pairout 0x76
set addr 9
set load 0
set loadpair 0
eval
expect out 0x6
expect pairout 0x76
set addr 10
set load 0
set loadpair 0
eval
expect out 0x5
expect pairout 0x54
set addr 11
set load 0
set loadpair 0
eval
expect out 0x4
expect pairout 0x54
set addr 12
set load 0
set loadpair 0
eval
expect out 0x3
expect pairout 0x32
set addr 13
set load 0
set loadpair 0
eval
expect out 0x2
expect pairout 0x32
set addr 14
set load 0
set loadpair 0
eval
expect out 0x1
expect pairout 0x10
set addr 15
set load 0
set loadpair 0
eval
expect out 0x0
expect pairout 0x10
// Each pair, named by an odd addr half the time
set in 0xF3
set addr 0
set load 0
set loadpair 1
tick
expect out 0xF
expect pairout 0xFE
tock
expect out 0xF
expect pairout 0xF3
set in 0xB5
set addr 3
set load 0
set loadpair 1
tick
expect out 0xC
expect pairout 0xDC
tock
expect out 0x5
expect pairout 0xB5
set in 0xFF
set addr 4
set load 0
set loadpair 1
tick
expect out 0xB
expect pairout 0xBA
tock
expect out 0xF
expect pairout 0xFF
set in 0x1B
set addr 7
set load 0
set loadpair 1
tick
expect out 0x8
expect pairout 0x98
tock
expect out 0xB
expect pairout 0x1B
set in 0xCC
set addr 8
set load 0
set loadpair 1
tick
expect out 0x7
expect pairout 0x76
tock
expect out 0xC
expect pairout 0xCC
set in 0x0E
set addr 11
set load 0
set loadpair 1
tick
expect out 0x4
expect pairout 0x54
tock
expect out 0xE
expect pairout 0x0E
set in 0xE5
set addr 12
set load 0
set loadpair 1
tick
expect out 0x3
expect pairout 0x32
tock
expect out 0xE
expect pairout 0xE5
set in 0x00
set addr 15
set load 0
set loadpair 1
tick
expect out 0x0
expect pairout 0x10
tock
expect out 0x0
expect pairout 0x00
set addr 0
set load 0
set loadpair 0
eval
expect out 0xF
expect pairout 0xF3
set addr 1
set load 0
set loadpair 0
eval
expect out 0x3
expect pairout 0xF3
set addr 2
set load 0
set loadpair 0
eval
expect out 0xB
expect pairout 0xB5
set addr 3
set load 0
set loadpair 0
eval
expect out 0x5
expect pairout 0xB5
set addr 4
set load 0
set loadpair 0
eval
expect out 0xF
expect pairout 0xFF
set addr 5
set load 0
set loadpair 0
eval
expect out 0xF
expect pairout 0xFF
set addr 6
set load 0
set loadpair 0
eval
expect out 0x1
expect pairout 0x1B
set addr 7
set load 0
set loadpair 0
eval
expect out 0xB
expect pairout 0x1B
set addr 8
set load 0
set loadpair 0
eval
expect out 0xC
expect pairout 0xCC
set addr 9
set load 0
set loadpair 0
eval
expect out 0xC
expect pairout 0xCC
set addr 10
set load 0
set loadpair 0
eval
expect out 0x0
expect pairout 0x0E
set addr 11
set load 0
set loadpair 0
eval
expect out 0xE
expect pairout 0x0E
set addr 12
set load 0
set loadpair 0
eval
expect out 0xE
expect pairout 0xE5
set addr 13
set load 0
set loadpair 0
eval
expect out 0x5
expect pairout 0xE5
set addr 14
set load 0
set loadpair 0
eval
expect out 0x0
expect pairout 0x00
set addr 15
set load 0
set loadpair 0
eval
expect out 0x0
expect pairout 0x00
// Neither load: nothing changes, whatever in is
set in 0xC1
set addr 0
set load 0
set loadpair 0
tick
expect out 0xF
expect pairout 0xF3
tock
expect out 0xF
expect pairout 0xF3
set in 0x6F
set addr 1
set load 0
set loadpair 0
tick
expect out 0x3
expect pairout 0xF3
tock
expect out 0x3
expect pairout 0xF3
set in 0x7F
set addr 2
set load 0
set loadpair 0
tick
expect out 0xB
expect pairout 0xB5
tock
expect out 0xB
expect pairout 0xB5
set in 0xCF
set addr 3
set load 0
set loadpair 0
tick
expect out 0x5
expect pairout 0xB5
tock
expect out 0x5
expect pairout 0xB5
set in 0x6C
set addr 4
set load 0
set loadpair 0
tick
expect out 0xF
expect pairout 0xFF
tock
expect out 0xF
expect pairout 0xFF
set in 0xAB
set addr 5
set load 0
set loadpair 0
tick
expect out 0xF
expect pairout 0xFF
tock
expect out 0xF
expect pairout 0xFF
set in 0x76
set addr 6
set load 0
set loadpair 0
tick
expect out 0x1
expect pairout 0x1B
tock
expect out 0x1
expect pairout 0x1B
set in 0x09
set addr 7
set load 0
set loadpair 0
tick
expect out 0xB
expect pairout 0x1B
tock
expect out 0xB
expect pairout 0x1B
set in 0x26
set addr 8
set load 0
set loadpair 0
tick
expect out 0xC
expect pairout 0xCC
tock
expect out 0xC
expect pairout 0xCC
set in 0x67
set addr 9
set load 0
set loadpair 0
tick
expect out 0xC
expect pairout 0xCC
tock
expect out 0xC
expect pairout 0xCC
set in 0x3D
set addr 10
set load 0
set loadpair 0
tick
expect out 0x0
expect pairout 0x0E
tock
expect out 0x0
expect pairout 0x0E
set in 0x60
set addr 11
set load 0
set loadpair 0
tick
expect out 0xE
expect pairout 0x0E
tock
expect out 0xE
expect pairout 0x0E
set in 0x72
set addr 12
set load 0
set loadpair 0
tick
expect out 0xE
expect pairout 0xE5
tock
expect out 0xE
expect pairout 0xE5
set in 0x92
set addr 13
set load 0
set loadpair 0
tick
expect out 0x5
expect pairout 0xE5
tock
expect out 0x5
expect pairout 0xE5
set in 0xFB
set addr 14
set load 0
set loadpair 0
tick
expect out 0x0
expect pairout 0x00
tock
expect out 0x0
expect pairout 0x00
set in 0x8E
set addr 15
set load 0
set loadpair 0
tick
expect out 0x0
expect pairout 0x00
tock
expect out 0x0
expect pairout 0x00
// load and loadpair together: the pair wins
set in 0x4E
set addr 0
set load 1
set loadpair 1
tick
expect out 0xF
expect pairout 0xF3
tock
expect out 0x4
expect pairout 0x4E
set in 0x27
set addr 7
set load 1
set loadpair 1
tick
expect out 0xB
expect pairout 0x1B
tock
expect out 0x7
expect pairout 0x27
set in 0x64
set addr 10
set load 1
set loadpair 1
tick
expect out 0x0
expect pairout 0x0E
tock
expect out 0x6
expect pairout 0x64
set in 0x41
set addr 15
set load 1
set loadpair 1
tick
expect out 0x0
expect pairout 0x00
tock
expect out 0x1
expect pairout 0x41
// Random cycles
set in 0x6E
set addr 14
set load 0
set loadpair 0
tick
expect out 0x4
expect pairout 0x41
tock
expect out 0x4
expect pairout 0x41
set in 0x89
set addr 0
set load 1
set loadpair 0
tick
expect out 0x4
expect pairout 0x4E
tock
expect out 0x9
expect pairout 0x9E
set in 0xB9
set addr 4
set load 1
set loadpair 0
tick
expect out 0xF
expect pairout 0xFF
tock
expect out 0x9
expect pairout 0x9F
set in 0x66
set addr 5
set load 1
set loadpair 0
tick
expect out 0xF
expect pairout 0x9F
tock
expect out 0x6
expect pairout 0x96
set in 0xAF
set addr 7
set load 0
set loadpair 0
tick
expect out 0x7
expect pairout 0x27
tock
expect out 0x7
expect pairout 0x27
set in 0xED
set addr 11
set load 1
set loadpair 0
tick
expect out 0x4
expect pairout 0x64
tock
expect out 0xD
expect pairout 0x6D
set in 0x12
set addr 6
set load 1
set loadpair 0
tick
expect out 0x2
expect pairout 0x27
tock
expect out 0x2
expect pairout 0x27
set in 0xCC
set addr 15
set load 0
set loadpair 0
tick
expect out 0x1
expect pairout 0x41
tock
expect out 0x1
expect pairout 0x41
set in 0x9F
set addr 9
set load 0
set loadpair 1
tick
expect out 0xC
expect pairout 0xCC
tock
expect out 0xF
expect pairout 0x9F
set in 0x3C
set addr 12
set load 0
set loadpair 0
tick
expect out 0xE
expect pairout 0xE5
tock
expect out 0xE
expect pairout 0xE5
set in 0x7B
set addr 10
set load 0
set loadpair 1
tick
expect out 0x6
expect pairout 0x6D
tock
expect out 0x7
expect pairout 0x7B
set in 0x50
set addr 7
set load 1
set loadpair 0
tick
expect out 0x7
expect pairout 0x27
tock
expect out 0x0
expect pairout 0x20
set in 0x4F
set addr 1
set load 0
set loadpair 0
tick
expect out 0xE
expect pairout 0x9E
tock
expect out 0xE
expect pairout 0x9E
set in 0x33
set addr 0
set load 1
set loadpair 0
tick
expect out 0x9
expect pairout 0x9E
tock
expect out 0x3
expect pairout 0x3E
set in 0xBA
set addr 6
set load 0
set loadpair 0
tick
expect out 0x2
expect pairout 0x20
tock
expect out 0x2
expect pairout 0x20
set in 0x7A
set addr 11
set load 0
set loadpair 0
tick
expect out 0xB
expect pairout 0x7B
tock
expect out 0xB
expect pairout 0x7B
set in 0xFE
set addr 12
set load 0
set loadpair 0
tick
expect out 0xE
expect pairout 0xE5
tock
expect out 0xE
expect pairout 0xE5
set in 0x9C
set addr 2
set load 1
set loadpair 0
tick
expect out 0xB
expect pairout 0xB5
tock
expect out 0xC
expect pairout 0xC5
set in 0xAF
set addr 9
set load 0
set loadpair 1
tick
expect out 0xF
expect pairout 0x9F
tock
expect out 0xF
expect pairout 0xAF
set in 0x37
set addr 0
set load 0
set loadpair 1
tick
expect out 0x3
expect pairout 0x3E
tock
expect out 0x3
expect pairout 0x37
set in 0x2B
set addr 5
set load 1
set loadpair 0
tick
expect out 0x6
expect pairout 0x96
tock
expect out 0xB
expect pairout 0x9B
set in 0x4D
set addr 2
set load 1
set loadpair 0
tick
expect out 0xC
expect pairout 0xC5
tock
expect out 0xD
expect pairout 0xD5
set in 0xA6
set addr 5
set load 1
set loadpair 0
tick
expect out 0xB
expect pairout 0x9B
tock
expect out 0x6
expect pairout 0x96
set in 0xF5
set addr 13
set load 1
set loadpair 0
tick
expect out 0x5
expect pairout 0xE5
tock
expect out 0x5
expect pairout 0xE5
set in 0x4A
set addr 6
set load 0
set loadpair 0
tick
expect out 0x2
expect pairout 0x20
tock
expect out 0x2
expect pairout 0x20
set in 0x7A
set addr 2
set load 1
set loadpair 0
tick
expect out 0xD
expect pairout 0xD5
tock
expect out 0xA
expect pairout 0xA5
set in 0x59
set addr 11
set load 1
set loadpair 0
tick
expect out 0xB
expect pairout 0x7B
tock
expect out 0x9
expect pairout 0x79
set in 0xCB
set addr 6
set load 1
set loadpair 0
tick
expect out 0x2
expect pairout 0x20
tock
expect out 0xB
expect pairout 0xB0
set in 0xC1
set addr 2
set load 1
set loadpair 0
tick
expect out 0xA
expect pairout 0xA5
tock
expect out 0x1
expect pairout 0x15
set in 0xA5
set addr 10
set load 1
set loadpair 0
tick
expect out 0x7
expect pairout 0x79
tock
expect out 0x5
expect pairout 0x59
set in 0xFE
set addr 10
set load 0
set loadpair 0
tick
expect out 0x5
expect pairout 0x59
tock
expect out 0x5
expect pairout 0x59
set in 0xB0
set addr 1
set load 1
set loadpair 0
tick
expect out 0x7
expect pairout 0x37
tock
expect out 0x0
expect pairout 0x30
set in 0x99
set addr 3
set load 1
set loadpair 0
tick
expect out 0x5
expect pairout 0x15
tock
expect out 0x9
expect pairout 0x19
set in 0x53
set addr 15
set load 1
set loadpair 0
tick
expect out 0x1
expect pairout 0x41
tock
expect out 0x3
expect pairout 0x43
set in 0x5C
set addr 2
set load 1
set loadpair 0
tick
expect out 0x1
expect pairout 0x19
tock
expect out 0xC
expect pairout 0xC9
set in 0x53
set addr 8
set load 1
set loadpair 0
tick
expect out 0xA
expect pairout 0xAF
tock
expect out 0x3
expect pairout 0x3F
set in 0xBC
set addr 6
set load 1
set loadpair 0
tick
expect out 0xB
expect pairout 0xB0
tock
expect out 0xC
expect pairout 0xC0
set in 0x40
set addr 11
set load 1
set loadpair 0
tick
expect out 0x9
expect pairout 0x59
tock
expect out 0x0
expect pairout 0x50
set in 0x1D
set addr 13
set load 1
set loadpair 0
tick
expect out 0x5
expect pairout 0xE5
tock
expect out 0xD
expect pairout 0xED
set in 0xE3
set addr 12
set load 1
set loadpair 0
tick
expect out 0xE
expect pairout 0xED
tock
expect out 0x3
expect pairout 0x3D
set in 0xEA
set addr 8
set load 0
set loadpair 0
tick
expect out 0x3
expect pairout 0x3F
tock
expect out 0x3
expect pairout 0x3F
set in 0x42
set addr 14
set load 1
set loadpair 0
tick
expect out 0x4
expect pairout 0x43
tock
expect out 0x2
expect pairout 0x23
set in 0xA0
set addr 9
set load 0
set loadpair 1
tick
expect out 0xF
expect pairout 0x3F
tock
expect out 0x0
expect pairout 0xA0
set in 0xD7
set addr 7
set load 0
set loadpair 0
tick
expect out 0x0
expect pairout 0xC0
tock
expect out 0x0
expect pairout 0xC0
set in 0x0C
set addr 2
set load 1
set loadpair 0
tick
expect out 0xC
expect pairout 0xC9
tock
expect out 0xC
expect pairout 0xC9
set in 0x98
set addr 15
set load 0
set loadpair 0
tick
expect out 0x3
expect pairout 0x23
tock
expect out 0x3
expect pairout 0x23
set in 0x8B
set addr 11
set load 0
set loadpair 1
tick
expect out 0x0
expect pairout 0x50
tock
expect out 0xB
expect pairout 0x8B
set in 0x03
set addr 12
set load 1
set loadpair 0
tick
expect out 0x3
expect pairout 0x3D
tock
expect out 0x3
expect pairout 0x3D
set in 0xE6
set addr 15
set load 0
set loadpair 1
tick
expect out 0x3
expect pairout 0x23
tock
expect out 0x6
expect pairout 0xE6
set in 0x42
set addr 0
set load 0
set loadpair 0
tick
expect out 0x3
expect pairout 0x30
tock
expect out 0x3
expect pairout 0x30
set in 0x31
set addr 7
set load 1
set loadpair 0
tick
expect out 0x0
expect pairout 0xC0
tock
expect out 0x1
expect pairout 0xC1
set in 0xE9
set addr 11
set load 0
set loadpair 0
tick
expect out 0xB
expect pairout 0x8B
tock
expect out 0xB
expect pairout 0x8B
set in 0xF5
set addr 12
set load 0
set loadpair 0
tick
expect out 0x3
expect pairout 0x3D
tock
expect out 0x3
expect pairout 0x3D
set in 0xAB
set addr 6
set load 0
set loadpair 0
tick
expect out 0xC
expect pairout 0xC1
tock
expect out 0xC
expect pairout 0xC1
set in 0x4A
set addr 3
set load 1
set loadpair 0
tick
expect out 0x9
expect pairout 0xC9
tock
expect out 0xA
expect pairout 0xCA
set in 0xC1
set addr 2
set load 0
set loadpair 0
tick
expect out 0xC
expect pairout 0xCA
tock
expect out 0xC
expect pairout 0xCA
set in 0x4E
set addr 8
set load 0
set loadpair 1
tick
expect out 0xA
expect pairout 0xA0
tock
expect out 0x4
expect pairout 0x4E
set in 0xEA
set addr 7
set load 0
set loadpair 0
tick
expect out 0x1
expect pairout 0xC1
tock
expect out 0x1
expect pairout 0xC1
set in 0x5F
set addr 9
set load 0
set loadpair 0
tick
expect out 0xE
expect pairout 0x4E
tock
expect out 0xE
expect pairout 0x4E
set in 0x65
set addr 4
set load 0
set loadpair 0
tick
expect out 0x9
expect pairout 0x96
tock
expect out 0x9
expect pairout 0x96
set in 0x1C
set addr 8
set load 1
set loadpair 0
tick
expect out 0x4
expect pairout 0x4E
tock
expect out 0xC
expect pairout 0xCE
set in 0x02
set addr 12
set load 0
set loadpair 1
tick
expect out 0x3
expect pairout 0x3D
tock
expect out 0x0
expect pairout 0x02
set in 0x72
set addr 6
set load 0
set loadpair 1
tick
expect out 0xC
expect pairout 0xC1
tock
expect out 0x7
expect pairout 0x72
set in 0xDA
set addr 10
set load 0
set loadpair 0
tick
expect out 0x8
expect pairout 0x8B
tock
expect out 0x8
expect pairout 0x8B
// Reset, with a load asked for at the same time: reset wins, every register is 0.
set in 0x77
set addr 5
set load 1
set loadpair 0
set reset 1
tick
expect out *
tock
expect out 0
expect pairout 0
set load 0
set reset 0
set addr 0
eval
expect out 0
expect pairout 0
set addr 1
eval
expect out 0
expect pairout 0
set addr 2
eval
expect out 0
expect pairout 0
set addr 3
eval
expect out 0
expect pairout 0
set addr 4
eval
expect out 0
expect pairout 0
set addr 5
eval
expect out 0
expect pairout 0
set addr 6
eval
expect out 0
expect pairout 0
set addr 7
eval
expect out 0
expect pairout 0
set addr 8
eval
expect out 0
expect pairout 0
set addr 9
eval
expect out 0
expect pairout 0
set addr 10
eval
expect out 0
expect pairout 0
set addr 11
eval
expect out 0
expect pairout 0
set addr 12
eval
expect out 0
expect pairout 0
set addr 13
eval
expect out 0
expect pairout 0
set addr 14
eval
expect out 0
expect pairout 0
set addr 15
eval
expect out 0
expect pairout 0
// Writes work again after reset.
set in 0x35
set addr 3
set load 1
tick
expect out 0
tock
expect out 0x5
expect pairout 0x05
// Reset wins over loadpair too.
set load 0
set loadpair 1
set in 0xA9
set addr 6
set reset 1
tick
expect pairout 0
tock
expect pairout 0
set addr 3
set loadpair 0
set reset 0
eval
expect out 0
