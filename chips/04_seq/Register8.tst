// Register8: load and hold the edges and each bit on its own, then 24 random cycles (seed 4004)
chip Register8
set in 0x00
set load 1
tick
tock
expect out 0x00
set in 0xFF
set load 0
tick
expect out 0x00
tock
expect out 0x00
set in 0xFF
set load 1
tick
expect out 0x00
tock
expect out 0xFF
set in 0x00
set load 0
tick
expect out 0xFF
tock
expect out 0xFF
set in 0x01
set load 1
tick
expect out 0xFF
tock
expect out 0x01
set in 0xFE
set load 0
tick
expect out 0x01
tock
expect out 0x01
set in 0x02
set load 1
tick
expect out 0x01
tock
expect out 0x02
set in 0xFD
set load 0
tick
expect out 0x02
tock
expect out 0x02
set in 0x04
set load 1
tick
expect out 0x02
tock
expect out 0x04
set in 0xFB
set load 0
tick
expect out 0x04
tock
expect out 0x04
set in 0x08
set load 1
tick
expect out 0x04
tock
expect out 0x08
set in 0xF7
set load 0
tick
expect out 0x08
tock
expect out 0x08
set in 0x10
set load 1
tick
expect out 0x08
tock
expect out 0x10
set in 0xEF
set load 0
tick
expect out 0x10
tock
expect out 0x10
set in 0x20
set load 1
tick
expect out 0x10
tock
expect out 0x20
set in 0xDF
set load 0
tick
expect out 0x20
tock
expect out 0x20
set in 0x40
set load 1
tick
expect out 0x20
tock
expect out 0x40
set in 0xBF
set load 0
tick
expect out 0x40
tock
expect out 0x40
set in 0x80
set load 1
tick
expect out 0x40
tock
expect out 0x80
set in 0x7F
set load 0
tick
expect out 0x80
tock
expect out 0x80
set in 0x55
set load 1
tick
expect out 0x80
tock
expect out 0x55
set in 0xAA
set load 0
tick
expect out 0x55
tock
expect out 0x55
set in 0xAA
set load 1
tick
expect out 0x55
tock
expect out 0xAA
set in 0x26
set load 0
tick
expect out 0xAA
tock
expect out 0xAA
set in 0x3D
set load 0
tick
expect out 0xAA
tock
expect out 0xAA
set in 0x72
set load 1
tick
expect out 0xAA
tock
expect out 0x72
set in 0xFB
set load 1
tick
expect out 0x72
tock
expect out 0xFB
set in 0x4E
set load 0
tick
expect out 0xFB
tock
expect out 0xFB
set in 0x64
set load 0
tick
expect out 0xFB
tock
expect out 0xFB
set in 0x1A
set load 0
tick
expect out 0xFB
tock
expect out 0xFB
set in 0xEE
set load 0
tick
expect out 0xFB
tock
expect out 0xFB
set in 0xC0
set load 1
tick
expect out 0xFB
tock
expect out 0xC0
set in 0x0D
set load 0
tick
expect out 0xC0
tock
expect out 0xC0
set in 0xB9
set load 0
tick
expect out 0xC0
tock
expect out 0xC0
set in 0xEE
set load 0
tick
expect out 0xC0
tock
expect out 0xC0
set in 0x57
set load 0
tick
expect out 0xC0
tock
expect out 0xC0
set in 0xAF
set load 0
tick
expect out 0xC0
tock
expect out 0xC0
set in 0x5D
set load 1
tick
expect out 0xC0
tock
expect out 0x5D
set in 0xED
set load 1
tick
expect out 0x5D
tock
expect out 0xED
set in 0xF9
set load 0
tick
expect out 0xED
tock
expect out 0xED
set in 0x6D
set load 0
tick
expect out 0xED
tock
expect out 0xED
set in 0xCC
set load 1
tick
expect out 0xED
tock
expect out 0xCC
set in 0xA0
set load 1
tick
expect out 0xCC
tock
expect out 0xA0
set in 0x95
set load 0
tick
expect out 0xA0
tock
expect out 0xA0
set in 0xA6
set load 0
tick
expect out 0xA0
tock
expect out 0xA0
set in 0xC9
set load 1
tick
expect out 0xA0
tock
expect out 0xC9
set in 0x7B
set load 1
tick
expect out 0xC9
tock
expect out 0x7B
