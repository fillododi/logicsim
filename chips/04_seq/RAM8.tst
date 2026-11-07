// RAM8: write every address, read them all back, a write with load off, then
// 48 random cycles (seed 4004). Each write checks out after its tick and its tock.
chip RAM8
// Every address, each a different value
set in 0x3
set addr 0
set load 1
tick
expect out *
tock
expect out 0x3
set in 0x8
set addr 1
set load 1
tick
expect out *
tock
expect out 0x8
set in 0xD
set addr 2
set load 1
tick
expect out *
tock
expect out 0xD
set in 0x2
set addr 3
set load 1
tick
expect out *
tock
expect out 0x2
set in 0x7
set addr 4
set load 1
tick
expect out *
tock
expect out 0x7
set in 0xC
set addr 5
set load 1
tick
expect out *
tock
expect out 0xC
set in 0x1
set addr 6
set load 1
tick
expect out *
tock
expect out 0x1
set in 0x6
set addr 7
set load 1
tick
expect out *
tock
expect out 0x6
set in 0x0
set addr 0
set load 0
eval
expect out 0x3
set in 0x0
set addr 1
set load 0
eval
expect out 0x8
set in 0x0
set addr 2
set load 0
eval
expect out 0xD
set in 0x0
set addr 3
set load 0
eval
expect out 0x2
set in 0x0
set addr 4
set load 0
eval
expect out 0x7
set in 0x0
set addr 5
set load 0
eval
expect out 0xC
set in 0x0
set addr 6
set load 0
eval
expect out 0x1
set in 0x0
set addr 7
set load 0
eval
expect out 0x6
// load off: nothing changes
set in 0xC
set addr 0
set load 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x7
set addr 1
set load 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x2
set addr 2
set load 0
tick
expect out 0xD
tock
expect out 0xD
set in 0xD
set addr 3
set load 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x8
set addr 4
set load 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x3
set addr 5
set load 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xE
set addr 6
set load 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x9
set addr 7
set load 0
tick
expect out 0x6
tock
expect out 0x6
// Random cycles
set in 0xB
set addr 7
set load 1
tick
expect out 0x6
tock
expect out 0xB
set in 0xC
set addr 0
set load 1
tick
expect out 0x3
tock
expect out 0xC
set in 0xC
set addr 0
set load 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x7
set addr 3
set load 1
tick
expect out 0x2
tock
expect out 0x7
set in 0xA
set addr 3
set load 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x2
set addr 0
set load 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x3
set addr 3
set load 1
tick
expect out 0x7
tock
expect out 0x3
set in 0x9
set addr 3
set load 1
tick
expect out 0x3
tock
expect out 0x9
set in 0x4
set addr 4
set load 1
tick
expect out 0x7
tock
expect out 0x4
set in 0x4
set addr 3
set load 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xE
set addr 3
set load 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xC
set addr 2
set load 1
tick
expect out 0xD
tock
expect out 0xC
set in 0x0
set addr 0
set load 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x4
set addr 5
set load 1
tick
expect out 0xC
tock
expect out 0x4
set in 0x5
set addr 3
set load 1
tick
expect out 0x9
tock
expect out 0x5
set in 0x7
set addr 5
set load 0
tick
expect out 0x4
tock
expect out 0x4
set in 0xE
set addr 5
set load 0
tick
expect out 0x4
tock
expect out 0x4
set in 0xF
set addr 5
set load 0
tick
expect out 0x4
tock
expect out 0x4
set in 0x6
set addr 0
set load 1
tick
expect out 0xC
tock
expect out 0x6
set in 0xF
set addr 6
set load 1
tick
expect out 0x1
tock
expect out 0xF
set in 0x9
set addr 4
set load 1
tick
expect out 0x4
tock
expect out 0x9
set in 0x3
set addr 5
set load 1
tick
expect out 0x4
tock
expect out 0x3
set in 0x7
set addr 6
set load 1
tick
expect out 0xF
tock
expect out 0x7
set in 0x3
set addr 7
set load 1
tick
expect out 0xB
tock
expect out 0x3
set in 0x7
set addr 3
set load 1
tick
expect out 0x5
tock
expect out 0x7
set in 0xF
set addr 0
set load 1
tick
expect out 0x6
tock
expect out 0xF
set in 0x3
set addr 2
set load 1
tick
expect out 0xC
tock
expect out 0x3
set in 0x6
set addr 5
set load 1
tick
expect out 0x3
tock
expect out 0x6
set in 0xB
set addr 3
set load 1
tick
expect out 0x7
tock
expect out 0xB
set in 0xF
set addr 4
set load 0
tick
expect out 0x9
tock
expect out 0x9
set in 0x1
set addr 6
set load 1
tick
expect out 0x7
tock
expect out 0x1
set in 0x0
set addr 1
set load 1
tick
expect out 0x8
tock
expect out 0x0
set in 0x3
set addr 4
set load 1
tick
expect out 0x9
tock
expect out 0x3
set in 0x6
set addr 0
set load 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x5
set addr 1
set load 1
tick
expect out 0x0
tock
expect out 0x5
set in 0x2
set addr 2
set load 1
tick
expect out 0x3
tock
expect out 0x2
set in 0x5
set addr 5
set load 1
tick
expect out 0x6
tock
expect out 0x5
set in 0xD
set addr 7
set load 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x6
set addr 2
set load 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x7
set addr 2
set load 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x2
set addr 3
set load 1
tick
expect out 0xB
tock
expect out 0x2
set in 0xB
set addr 2
set load 1
tick
expect out 0x2
tock
expect out 0xB
set in 0x6
set addr 6
set load 1
tick
expect out 0x1
tock
expect out 0x6
set in 0x2
set addr 6
set load 1
tick
expect out 0x6
tock
expect out 0x2
set in 0xA
set addr 5
set load 0
tick
expect out 0x5
tock
expect out 0x5
set in 0xA
set addr 7
set load 0
tick
expect out 0x3
tock
expect out 0x3
set in 0xB
set addr 0
set load 1
tick
expect out 0xF
tock
expect out 0xB
set in 0x9
set addr 0
set load 1
tick
expect out 0xB
tock
expect out 0x9
