// Register12: load and hold the edges and each bit on its own, then 24 random cycles (seed 4004)
chip Register12
set in 0x000
set load 1
tick
tock
expect out 0x000
set in 0xFFF
set load 0
tick
expect out 0x000
tock
expect out 0x000
set in 0xFFF
set load 1
tick
expect out 0x000
tock
expect out 0xFFF
set in 0x000
set load 0
tick
expect out 0xFFF
tock
expect out 0xFFF
set in 0x001
set load 1
tick
expect out 0xFFF
tock
expect out 0x001
set in 0xFFE
set load 0
tick
expect out 0x001
tock
expect out 0x001
set in 0x002
set load 1
tick
expect out 0x001
tock
expect out 0x002
set in 0xFFD
set load 0
tick
expect out 0x002
tock
expect out 0x002
set in 0x004
set load 1
tick
expect out 0x002
tock
expect out 0x004
set in 0xFFB
set load 0
tick
expect out 0x004
tock
expect out 0x004
set in 0x008
set load 1
tick
expect out 0x004
tock
expect out 0x008
set in 0xFF7
set load 0
tick
expect out 0x008
tock
expect out 0x008
set in 0x010
set load 1
tick
expect out 0x008
tock
expect out 0x010
set in 0xFEF
set load 0
tick
expect out 0x010
tock
expect out 0x010
set in 0x020
set load 1
tick
expect out 0x010
tock
expect out 0x020
set in 0xFDF
set load 0
tick
expect out 0x020
tock
expect out 0x020
set in 0x040
set load 1
tick
expect out 0x020
tock
expect out 0x040
set in 0xFBF
set load 0
tick
expect out 0x040
tock
expect out 0x040
set in 0x080
set load 1
tick
expect out 0x040
tock
expect out 0x080
set in 0xF7F
set load 0
tick
expect out 0x080
tock
expect out 0x080
set in 0x100
set load 1
tick
expect out 0x080
tock
expect out 0x100
set in 0xEFF
set load 0
tick
expect out 0x100
tock
expect out 0x100
set in 0x200
set load 1
tick
expect out 0x100
tock
expect out 0x200
set in 0xDFF
set load 0
tick
expect out 0x200
tock
expect out 0x200
set in 0x400
set load 1
tick
expect out 0x200
tock
expect out 0x400
set in 0xBFF
set load 0
tick
expect out 0x400
tock
expect out 0x400
set in 0x800
set load 1
tick
expect out 0x400
tock
expect out 0x800
set in 0x7FF
set load 0
tick
expect out 0x800
tock
expect out 0x800
set in 0x555
set load 1
tick
expect out 0x800
tock
expect out 0x555
set in 0xAAA
set load 0
tick
expect out 0x555
tock
expect out 0x555
set in 0xAAA
set load 1
tick
expect out 0x555
tock
expect out 0xAAA
set in 0x415
set load 1
tick
expect out 0xAAA
tock
expect out 0x415
set in 0x322
set load 1
tick
expect out 0x415
tock
expect out 0x322
set in 0x50E
set load 0
tick
expect out 0x322
tock
expect out 0x322
set in 0x713
set load 0
tick
expect out 0x322
tock
expect out 0x322
set in 0x179
set load 1
tick
expect out 0x322
tock
expect out 0x179
set in 0xF6E
set load 0
tick
expect out 0x179
tock
expect out 0x179
set in 0x407
set load 0
tick
expect out 0x179
tock
expect out 0x179
set in 0x0CF
set load 1
tick
expect out 0x179
tock
expect out 0x0CF
set in 0x651
set load 1
tick
expect out 0x0CF
tock
expect out 0x651
set in 0x4C8
set load 0
tick
expect out 0x651
tock
expect out 0x651
set in 0xB18
set load 1
tick
expect out 0x651
tock
expect out 0xB18
set in 0xFE1
set load 1
tick
expect out 0xB18
tock
expect out 0xFE1
set in 0xD0A
set load 0
tick
expect out 0xFE1
tock
expect out 0xFE1
set in 0xBD2
set load 1
tick
expect out 0xFE1
tock
expect out 0xBD2
set in 0x2E4
set load 0
tick
expect out 0xBD2
tock
expect out 0xBD2
set in 0xAF5
set load 1
tick
expect out 0xBD2
tock
expect out 0xAF5
set in 0x94D
set load 0
tick
expect out 0xAF5
tock
expect out 0xAF5
set in 0x0C3
set load 0
tick
expect out 0xAF5
tock
expect out 0xAF5
set in 0x04F
set load 0
tick
expect out 0xAF5
tock
expect out 0xAF5
set in 0x2BF
set load 0
tick
expect out 0xAF5
tock
expect out 0xAF5
set in 0x524
set load 0
tick
expect out 0xAF5
tock
expect out 0xAF5
set in 0x4D6
set load 0
tick
expect out 0xAF5
tock
expect out 0xAF5
set in 0x50D
set load 1
tick
expect out 0xAF5
tock
expect out 0x50D
set in 0x535
set load 1
tick
expect out 0x50D
tock
expect out 0x535
