// Register4: load every value and hold it against a random in (seed 4004), and each bit on its own
chip Register4
set in 0x0
set load 1
tick
tock
expect out 0x0
set in 0xF
set load 0
tick
expect out 0x0
tock
expect out 0x0
set in 0xF
set load 1
tick
expect out 0x0
tock
expect out 0xF
set in 0x0
set load 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x1
set load 1
tick
expect out 0xF
tock
expect out 0x1
set in 0xE
set load 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x2
set load 1
tick
expect out 0x1
tock
expect out 0x2
set in 0xD
set load 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x4
set load 1
tick
expect out 0x2
tock
expect out 0x4
set in 0xB
set load 0
tick
expect out 0x4
tock
expect out 0x4
set in 0x8
set load 1
tick
expect out 0x4
tock
expect out 0x8
set in 0x7
set load 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x5
set load 1
tick
expect out 0x8
tock
expect out 0x5
set in 0xA
set load 0
tick
expect out 0x5
tock
expect out 0x5
set in 0xA
set load 1
tick
expect out 0x5
tock
expect out 0xA
set in 0x0
set load 1
tick
expect out 0xA
tock
expect out 0x0
set in 0xF
set load 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x1
set load 1
tick
expect out 0x0
tock
expect out 0x1
set in 0xB
set load 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x2
set load 1
tick
expect out 0x1
tock
expect out 0x2
set in 0xF
set load 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x3
set load 1
tick
expect out 0x2
tock
expect out 0x3
set in 0x1
set load 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x4
set load 1
tick
expect out 0x3
tock
expect out 0x4
set in 0xC
set load 0
tick
expect out 0x4
tock
expect out 0x4
set in 0x5
set load 1
tick
expect out 0x4
tock
expect out 0x5
set in 0x0
set load 0
tick
expect out 0x5
tock
expect out 0x5
set in 0x6
set load 1
tick
expect out 0x5
tock
expect out 0x6
set in 0xE
set load 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x7
set load 1
tick
expect out 0x6
tock
expect out 0x7
set in 0x0
set load 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x8
set load 1
tick
expect out 0x7
tock
expect out 0x8
set in 0xC
set load 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x9
set load 1
tick
expect out 0x8
tock
expect out 0x9
set in 0x6
set load 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xA
set load 1
tick
expect out 0x9
tock
expect out 0xA
set in 0x7
set load 0
tick
expect out 0xA
tock
expect out 0xA
set in 0xB
set load 1
tick
expect out 0xA
tock
expect out 0xB
set in 0xC
set load 0
tick
expect out 0xB
tock
expect out 0xB
set in 0xC
set load 1
tick
expect out 0xB
tock
expect out 0xC
set in 0x6
set load 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xD
set load 1
tick
expect out 0xC
tock
expect out 0xD
set in 0xA
set load 0
tick
expect out 0xD
tock
expect out 0xD
set in 0xE
set load 1
tick
expect out 0xD
tock
expect out 0xE
set in 0x7
set load 0
tick
expect out 0xE
tock
expect out 0xE
set in 0xF
set load 1
tick
expect out 0xE
tock
expect out 0xF
set in 0x0
set load 0
tick
expect out 0xF
tock
expect out 0xF
