// DataRAM: in each of the 8 banks, main characters 0, 1, 2, 4, ..., 128 and 255,
// and status characters at addresses 0, 64, 128 and 255, one in each chip. Fill
// them, rewrite each with a different value, read them all back. No two cells of
// a bank hold the same value, and no cell shares its value with the same cell in
// another bank. Then 200 random cycles (seed 4004) on those cells.
// Each write checks out after its tick (the old value) and after its tock.
chip DataRAM
// Fill: the same cells in every bank
set in 0xA
set addr 0
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0xB
set addr 1
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 2
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x6
set addr 4
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xC
set addr 8
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xE
set addr 16
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x8
set addr 32
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x7
set addr 64
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x4
set addr 128
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x0
set addr 255
set bank 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x2
set addr 0
set bank 0
set load 1
set status 1
tick
expect out *
tock
expect out 0x2
set in 0xF
set addr 64
set bank 0
set load 1
set status 1
tick
expect out *
tock
expect out 0xF
set in 0x5
set addr 128
set bank 0
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0x3
set addr 255
set bank 0
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0xB
set addr 0
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xC
set addr 1
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x2
set addr 2
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x7
set addr 4
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xD
set addr 8
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xF
set addr 16
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x9
set addr 32
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x8
set addr 64
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x5
set addr 128
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x1
set addr 255
set bank 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x3
set addr 0
set bank 1
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0x0
set addr 64
set bank 1
set load 1
set status 1
tick
expect out *
tock
expect out 0x0
set in 0x6
set addr 128
set bank 1
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0x4
set addr 255
set bank 1
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0xC
set addr 0
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xD
set addr 1
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x3
set addr 2
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x8
set addr 4
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0xE
set addr 8
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x0
set addr 16
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0xA
set addr 32
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x9
set addr 64
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x6
set addr 128
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x2
set addr 255
set bank 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x4
set addr 0
set bank 2
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0x1
set addr 64
set bank 2
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0x7
set addr 128
set bank 2
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x5
set addr 255
set bank 2
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xD
set addr 0
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xE
set addr 1
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x4
set addr 2
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x9
set addr 4
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xF
set addr 8
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x1
set addr 16
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xB
set addr 32
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0xA
set addr 64
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 128
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x3
set addr 255
set bank 3
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x5
set addr 0
set bank 3
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0x2
set addr 64
set bank 3
set load 1
set status 1
tick
expect out *
tock
expect out 0x2
set in 0x8
set addr 128
set bank 3
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0x6
set addr 255
set bank 3
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 0
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xF
set addr 1
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x5
set addr 2
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xA
set addr 4
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x0
set addr 8
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x2
set addr 16
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xC
set addr 32
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xB
set addr 64
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x8
set addr 128
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x4
set addr 255
set bank 4
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x6
set addr 0
set bank 4
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0x3
set addr 64
set bank 4
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0x9
set addr 128
set bank 4
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0x7
set addr 255
set bank 4
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0xF
set addr 0
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x0
set addr 1
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x6
set addr 2
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xB
set addr 4
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 8
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x3
set addr 16
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xD
set addr 32
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xC
set addr 64
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x9
set addr 128
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x5
set addr 255
set bank 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x7
set addr 0
set bank 5
set load 1
set status 1
tick
expect out *
tock
expect out 0x7
set in 0x4
set addr 64
set bank 5
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0xA
set addr 128
set bank 5
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x8
set addr 255
set bank 5
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0x0
set addr 0
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x1
set addr 1
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x7
set addr 2
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xC
set addr 4
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0x2
set addr 8
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x4
set addr 16
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xE
set addr 32
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xD
set addr 64
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xA
set addr 128
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x6
set addr 255
set bank 6
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x8
set addr 0
set bank 6
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0x5
set addr 64
set bank 6
set load 1
set status 1
tick
expect out *
tock
expect out 0x5
set in 0xB
set addr 128
set bank 6
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0x9
set addr 255
set bank 6
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0x1
set addr 0
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x2
set addr 1
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x8
set addr 2
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0xD
set addr 4
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x3
set addr 8
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x5
set addr 16
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xF
set addr 32
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xE
set addr 64
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xB
set addr 128
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x7
set addr 255
set bank 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x9
set addr 0
set bank 7
set load 1
set status 1
tick
expect out *
tock
expect out 0x9
set in 0x6
set addr 64
set bank 7
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0xC
set addr 128
set bank 7
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xA
set addr 255
set bank 7
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
// Rewrite: every cell again, each with a different value
set in 0x8
set addr 0
set bank 0
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x8
set in 0x9
set addr 1
set bank 0
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x9
set in 0xF
set addr 2
set bank 0
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0x4
set addr 4
set bank 0
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0xA
set addr 8
set bank 0
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0xC
set addr 16
set bank 0
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0x6
set addr 32
set bank 0
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0x5
set addr 64
set bank 0
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0x2
set addr 128
set bank 0
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x2
set in 0xE
set addr 255
set bank 0
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0x0
set addr 0
set bank 0
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x0
set in 0xD
set addr 64
set bank 0
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0xD
set in 0x3
set addr 128
set bank 0
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x3
set in 0x1
set addr 255
set bank 0
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x1
set in 0x9
set addr 0
set bank 1
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x9
set in 0xA
set addr 1
set bank 1
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x0
set addr 2
set bank 1
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0x5
set addr 4
set bank 1
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0xB
set addr 8
set bank 1
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0xD
set addr 16
set bank 1
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0x7
set addr 32
set bank 1
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x7
set in 0x6
set addr 64
set bank 1
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0x3
set addr 128
set bank 1
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x3
set in 0xF
set addr 255
set bank 1
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0x1
set addr 0
set bank 1
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x1
set in 0xE
set addr 64
set bank 1
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0xE
set in 0x4
set addr 128
set bank 1
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x4
set in 0x2
set addr 255
set bank 1
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x2
set in 0xA
set addr 0
set bank 2
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0xB
set addr 1
set bank 2
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0x1
set addr 2
set bank 2
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x1
set in 0x6
set addr 4
set bank 2
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0xC
set addr 8
set bank 2
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0xE
set addr 16
set bank 2
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0x8
set addr 32
set bank 2
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x8
set in 0x7
set addr 64
set bank 2
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x7
set in 0x4
set addr 128
set bank 2
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0x0
set addr 255
set bank 2
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0x2
set addr 0
set bank 2
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x2
set in 0xF
set addr 64
set bank 2
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0xF
set in 0x5
set addr 128
set bank 2
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x5
set in 0x3
set addr 255
set bank 2
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x3
set in 0xB
set addr 0
set bank 3
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0xC
set addr 1
set bank 3
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0x2
set addr 2
set bank 3
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x2
set in 0x7
set addr 4
set bank 3
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x7
set in 0xD
set addr 8
set bank 3
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0xF
set addr 16
set bank 3
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0x9
set addr 32
set bank 3
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x9
set in 0x8
set addr 64
set bank 3
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x8
set in 0x5
set addr 128
set bank 3
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0x1
set addr 255
set bank 3
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x1
set in 0x3
set addr 0
set bank 3
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x3
set in 0x0
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x0
set in 0x6
set addr 128
set bank 3
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x6
set in 0x4
set addr 255
set bank 3
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x4
set in 0xC
set addr 0
set bank 4
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0xD
set addr 1
set bank 4
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0x3
set addr 2
set bank 4
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x3
set in 0x8
set addr 4
set bank 4
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x8
set in 0xE
set addr 8
set bank 4
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0x0
set addr 16
set bank 4
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0xA
set addr 32
set bank 4
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x9
set addr 64
set bank 4
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x9
set in 0x6
set addr 128
set bank 4
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0x2
set addr 255
set bank 4
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x2
set in 0x4
set addr 0
set bank 4
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x4
set in 0x1
set addr 64
set bank 4
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x1
set in 0x7
set addr 128
set bank 4
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x7
set in 0x5
set addr 255
set bank 4
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x5
set in 0xD
set addr 0
set bank 5
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0xE
set addr 1
set bank 5
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0x4
set addr 2
set bank 5
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0x9
set addr 4
set bank 5
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x9
set in 0xF
set addr 8
set bank 5
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0x1
set addr 16
set bank 5
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x1
set in 0xB
set addr 32
set bank 5
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0xA
set addr 64
set bank 5
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x7
set addr 128
set bank 5
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x7
set in 0x3
set addr 255
set bank 5
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x3
set in 0x5
set addr 0
set bank 5
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x5
set in 0x2
set addr 64
set bank 5
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x2
set in 0x8
set addr 128
set bank 5
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x8
set in 0x6
set addr 255
set bank 5
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x6
set in 0xE
set addr 0
set bank 6
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xE
set in 0xF
set addr 1
set bank 6
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0x5
set addr 2
set bank 6
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0xA
set addr 4
set bank 6
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x0
set addr 8
set bank 6
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0x2
set addr 16
set bank 6
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x2
set in 0xC
set addr 32
set bank 6
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0xB
set addr 64
set bank 6
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0x8
set addr 128
set bank 6
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x8
set in 0x4
set addr 255
set bank 6
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0x6
set addr 0
set bank 6
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x6
set in 0x3
set addr 64
set bank 6
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x3
set in 0x9
set addr 128
set bank 6
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x9
set in 0x7
set addr 255
set bank 6
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x7
set in 0xF
set addr 0
set bank 7
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xF
set in 0x0
set addr 1
set bank 7
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0x6
set addr 2
set bank 7
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x6
set in 0xB
set addr 4
set bank 7
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xB
set in 0x1
set addr 8
set bank 7
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x1
set in 0x3
set addr 16
set bank 7
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x3
set in 0xD
set addr 32
set bank 7
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xD
set in 0xC
set addr 64
set bank 7
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xC
set in 0x9
set addr 128
set bank 7
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x9
set in 0x5
set addr 255
set bank 7
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0x7
set addr 0
set bank 7
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0x7
set in 0x4
set addr 64
set bank 7
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x4
set in 0xA
set addr 128
set bank 7
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0xA
set in 0x8
set addr 255
set bank 7
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x8
// Read everything back
set in 0x0
set addr 0
set bank 0
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 1
set bank 0
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 2
set bank 0
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 4
set bank 0
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 8
set bank 0
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 16
set bank 0
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 32
set bank 0
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 64
set bank 0
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 128
set bank 0
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 255
set bank 0
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 0
set bank 0
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 64
set bank 0
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 128
set bank 0
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 255
set bank 0
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 0
set bank 1
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 1
set bank 1
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 2
set bank 1
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 4
set bank 1
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 8
set bank 1
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 16
set bank 1
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 32
set bank 1
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 64
set bank 1
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 128
set bank 1
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 255
set bank 1
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 0
set bank 1
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 64
set bank 1
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 128
set bank 1
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 255
set bank 1
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 0
set bank 2
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 1
set bank 2
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 2
set bank 2
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 4
set bank 2
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 8
set bank 2
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 16
set bank 2
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 32
set bank 2
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 64
set bank 2
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 128
set bank 2
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 255
set bank 2
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 0
set bank 2
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 64
set bank 2
set load 0
set status 1
eval
expect out 0xF
set in 0x0
set addr 128
set bank 2
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 255
set bank 2
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 0
set bank 3
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 1
set bank 3
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 2
set bank 3
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 4
set bank 3
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 8
set bank 3
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 16
set bank 3
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 32
set bank 3
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 64
set bank 3
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 128
set bank 3
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 255
set bank 3
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 0
set bank 3
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 64
set bank 3
set load 0
set status 1
eval
expect out 0x0
set in 0x0
set addr 128
set bank 3
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 255
set bank 3
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 0
set bank 4
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 1
set bank 4
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 2
set bank 4
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 4
set bank 4
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 8
set bank 4
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 16
set bank 4
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 32
set bank 4
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 64
set bank 4
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 128
set bank 4
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 255
set bank 4
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 0
set bank 4
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 64
set bank 4
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 128
set bank 4
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 255
set bank 4
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 0
set bank 5
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 1
set bank 5
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 2
set bank 5
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 4
set bank 5
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 8
set bank 5
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 16
set bank 5
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 32
set bank 5
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 64
set bank 5
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 128
set bank 5
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 255
set bank 5
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 0
set bank 5
set load 0
set status 1
eval
expect out 0x5
set in 0x0
set addr 64
set bank 5
set load 0
set status 1
eval
expect out 0x2
set in 0x0
set addr 128
set bank 5
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 255
set bank 5
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 0
set bank 6
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 1
set bank 6
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 2
set bank 6
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 4
set bank 6
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 8
set bank 6
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 16
set bank 6
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 32
set bank 6
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 64
set bank 6
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 128
set bank 6
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 255
set bank 6
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 0
set bank 6
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 64
set bank 6
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 128
set bank 6
set load 0
set status 1
eval
expect out 0x9
set in 0x0
set addr 255
set bank 6
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 0
set bank 7
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 1
set bank 7
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 2
set bank 7
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 4
set bank 7
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 8
set bank 7
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 16
set bank 7
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 32
set bank 7
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 64
set bank 7
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 128
set bank 7
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 255
set bank 7
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 0
set bank 7
set load 0
set status 1
eval
expect out 0x7
set in 0x0
set addr 64
set bank 7
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 128
set bank 7
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 255
set bank 7
set load 0
set status 1
eval
expect out 0x8
// 200 random cycles on the cells above, load on about 60% of them
set in 0xF
set addr 4
set bank 2
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0xC
set addr 64
set bank 6
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xC
set in 0xC
set addr 64
set bank 1
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xC
set in 0xE
set addr 32
set bank 4
set load 0
set status 0
tick
expect out 0xA
tock
expect out 0xA
set in 0xC
set addr 128
set bank 2
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0x8
set addr 128
set bank 2
set load 0
set status 0
tick
expect out 0x4
tock
expect out 0x4
set in 0xB
set addr 8
set bank 1
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0xC
set addr 32
set bank 7
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0x1
set addr 2
set bank 1
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x1
set in 0x4
set addr 128
set bank 4
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x4
set in 0x0
set addr 255
set bank 3
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x0
set in 0x5
set addr 64
set bank 6
set load 0
set status 1
tick
expect out 0x3
tock
expect out 0x3
set in 0x3
set addr 128
set bank 7
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0x9
set addr 255
set bank 1
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x9
set in 0x7
set addr 128
set bank 5
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0xC
set addr 32
set bank 0
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x1
set addr 64
set bank 0
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x1
set in 0x5
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0x5
set in 0xB
set addr 128
set bank 3
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0xB
set in 0x5
set addr 0
set bank 5
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0x8
set addr 0
set bank 0
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xC
set addr 255
set bank 2
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0xC
set in 0xD
set addr 1
set bank 3
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x7
set addr 255
set bank 1
set load 0
set status 1
tick
expect out 0x9
tock
expect out 0x9
set in 0x9
set addr 128
set bank 6
set load 0
set status 1
tick
expect out 0x9
tock
expect out 0x9
set in 0x2
set addr 2
set bank 1
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x2
set in 0x3
set addr 2
set bank 6
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x3
set in 0xC
set addr 128
set bank 0
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0xC
set in 0xB
set addr 0
set bank 3
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0xC
set addr 128
set bank 5
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0xC
set in 0xF
set addr 16
set bank 2
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xF
set in 0x8
set addr 128
set bank 2
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0xD
set addr 255
set bank 1
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xD
set in 0xE
set addr 1
set bank 3
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xE
set in 0x3
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x3
set in 0x3
set addr 255
set bank 6
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x3
set in 0x9
set addr 0
set bank 1
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0x6
set addr 64
set bank 0
set load 0
set status 1
tick
expect out 0xD
tock
expect out 0xD
set in 0x9
set addr 64
set bank 1
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x9
set in 0xF
set addr 4
set bank 2
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0xA
set addr 64
set bank 0
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0xA
set in 0xC
set addr 4
set bank 5
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xC
set in 0x0
set addr 64
set bank 5
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x0
set in 0xC
set addr 255
set bank 7
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xC
set in 0x8
set addr 0
set bank 4
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x8
set in 0x7
set addr 4
set bank 4
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xC
set addr 1
set bank 2
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xC
set in 0x7
set addr 0
set bank 2
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x7
set in 0x4
set addr 128
set bank 7
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x1
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x1
set in 0xF
set addr 128
set bank 3
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0xF
set in 0xD
set addr 0
set bank 4
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xF
set addr 0
set bank 1
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0xF
set in 0xB
set addr 32
set bank 0
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xB
set in 0x8
set addr 8
set bank 7
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x8
set in 0x1
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x1
set in 0x2
set addr 255
set bank 1
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x0
set addr 64
set bank 6
set load 0
set status 1
tick
expect out 0x3
tock
expect out 0x3
set in 0xC
set addr 64
set bank 7
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0xC
set in 0xC
set addr 128
set bank 6
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xC
set in 0xC
set addr 255
set bank 1
set load 0
set status 1
tick
expect out 0xD
tock
expect out 0xD
set in 0x8
set addr 1
set bank 4
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0xA
set addr 255
set bank 7
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0x8
set addr 16
set bank 1
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0xA
set addr 0
set bank 1
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0xA
set in 0x1
set addr 255
set bank 2
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x1
set in 0x6
set addr 32
set bank 3
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xC
set addr 1
set bank 2
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x1
set addr 16
set bank 5
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x2
set addr 2
set bank 0
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x2
set in 0xE
set addr 32
set bank 0
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0xF
set addr 0
set bank 2
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0xF
set in 0x7
set addr 8
set bank 6
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x7
set in 0x3
set addr 16
set bank 4
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x3
set in 0xB
set addr 8
set bank 7
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xB
set in 0x2
set addr 64
set bank 1
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x2
set in 0xC
set addr 128
set bank 2
set load 0
set status 0
tick
expect out 0x4
tock
expect out 0x4
set in 0x5
set addr 0
set bank 5
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0x4
set addr 64
set bank 1
set load 0
set status 1
tick
expect out 0x2
tock
expect out 0x2
set in 0x9
set addr 0
set bank 6
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x9
set in 0xC
set addr 255
set bank 3
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0xD
set addr 0
set bank 6
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xD
set in 0xE
set addr 64
set bank 4
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xE
set in 0x6
set addr 2
set bank 7
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x1
set addr 2
set bank 5
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x1
set in 0x9
set addr 2
set bank 5
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x9
set in 0x9
set addr 4
set bank 3
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x9
set in 0xD
set addr 2
set bank 7
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xD
set in 0x2
set addr 255
set bank 7
set load 0
set status 1
tick
expect out 0x8
tock
expect out 0x8
set in 0xB
set addr 32
set bank 3
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xB
set in 0x0
set addr 128
set bank 5
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x0
set in 0xC
set addr 16
set bank 1
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xC
set in 0x4
set addr 0
set bank 3
set load 0
set status 1
tick
expect out 0x3
tock
expect out 0x3
set in 0xD
set addr 64
set bank 0
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xD
set in 0xF
set addr 2
set bank 0
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xF
set in 0x2
set addr 4
set bank 3
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0x8
set addr 4
set bank 1
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0x8
set in 0xE
set addr 32
set bank 1
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0xA
set addr 255
set bank 4
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0xA
set in 0xD
set addr 128
set bank 2
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0xD
set addr 32
set bank 5
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xD
set in 0xA
set addr 2
set bank 3
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x8
set addr 64
set bank 5
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x8
set in 0x8
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x8
set in 0x8
set addr 1
set bank 2
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x2
set addr 255
set bank 5
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x2
set in 0x7
set addr 8
set bank 2
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x7
set in 0xB
set addr 16
set bank 6
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x5
set addr 128
set bank 5
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0x5
set in 0x9
set addr 16
set bank 6
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0xA
set addr 0
set bank 4
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xA
set in 0xE
set addr 16
set bank 0
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xC
set addr 0
set bank 5
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0x4
set addr 255
set bank 2
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x4
set in 0xC
set addr 128
set bank 0
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xC
set in 0x2
set addr 0
set bank 0
set load 0
set status 1
tick
expect out 0x0
tock
expect out 0x0
set in 0xA
set addr 32
set bank 5
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xA
set in 0x6
set addr 8
set bank 5
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x9
set addr 64
set bank 7
set load 0
set status 1
tick
expect out 0xC
tock
expect out 0xC
set in 0xB
set addr 2
set bank 6
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xB
set in 0x5
set addr 4
set bank 1
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x5
set in 0x3
set addr 128
set bank 2
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x3
set in 0x6
set addr 1
set bank 7
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x2
set addr 8
set bank 1
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x2
set in 0xB
set addr 128
set bank 5
set load 0
set status 1
tick
expect out 0x5
tock
expect out 0x5
set in 0x6
set addr 255
set bank 2
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x6
set in 0x9
set addr 0
set bank 3
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x8
set addr 0
set bank 5
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x8
set in 0x6
set addr 2
set bank 2
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0xB
set addr 64
set bank 3
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0xB
set in 0x6
set addr 1
set bank 5
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0x2
set addr 1
set bank 4
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0x6
set addr 4
set bank 2
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x6
set addr 255
set bank 1
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x6
set in 0x6
set addr 255
set bank 4
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x5
set addr 0
set bank 2
set load 0
set status 0
tick
expect out 0xF
tock
expect out 0xF
set in 0x9
set addr 16
set bank 6
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x9
set in 0xF
set addr 4
set bank 1
set load 0
set status 0
tick
expect out 0x5
tock
expect out 0x5
set in 0xC
set addr 16
set bank 4
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0xC
set in 0xD
set addr 1
set bank 5
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xD
set in 0x8
set addr 64
set bank 5
set load 1
set status 1
tick
expect out 0x2
tock
expect out 0x8
set in 0x6
set addr 128
set bank 7
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x6
set in 0x9
set addr 255
set bank 5
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x9
set in 0x0
set addr 255
set bank 5
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x0
set in 0x7
set addr 64
set bank 0
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x7
set in 0x5
set addr 255
set bank 6
set load 0
set status 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x3
set addr 4
set bank 5
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x3
set in 0x5
set addr 32
set bank 6
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x0
set addr 16
set bank 5
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x9
set addr 4
set bank 5
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x9
set in 0xA
set addr 255
set bank 0
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xA
set in 0x3
set addr 0
set bank 1
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x3
set in 0xE
set addr 32
set bank 5
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xE
set in 0x8
set addr 64
set bank 5
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x0
set addr 255
set bank 3
set load 1
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x6
set addr 128
set bank 6
set load 0
set status 1
tick
expect out 0xC
tock
expect out 0xC
set in 0x0
set addr 2
set bank 5
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x0
set in 0x3
set addr 64
set bank 4
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0xD
set addr 128
set bank 1
set load 0
set status 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x7
set addr 255
set bank 0
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x7
set in 0x2
set addr 32
set bank 4
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x2
set in 0xA
set addr 64
set bank 1
set load 0
set status 1
tick
expect out 0x2
tock
expect out 0x2
set in 0xA
set addr 128
set bank 0
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x7
set addr 0
set bank 1
set load 0
set status 0
tick
expect out 0x3
tock
expect out 0x3
set in 0x4
set addr 64
set bank 4
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0x7
set addr 255
set bank 6
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x7
set in 0x9
set addr 255
set bank 3
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x9
set in 0xC
set addr 32
set bank 7
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xC
set in 0xB
set addr 255
set bank 2
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0xB
set in 0x8
set addr 0
set bank 3
set load 1
set status 1
tick
expect out 0x3
tock
expect out 0x8
set in 0x3
set addr 16
set bank 2
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x3
set in 0xB
set addr 128
set bank 4
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0xB
set in 0x0
set addr 32
set bank 7
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0xE
set addr 0
set bank 4
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xE
set in 0xD
set addr 32
set bank 2
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0x4
set addr 0
set bank 1
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x8
set addr 2
set bank 3
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0xC
set addr 1
set bank 6
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0xC
set in 0xB
set addr 255
set bank 2
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x4
set addr 255
set bank 1
set load 0
set status 1
tick
expect out 0xD
tock
expect out 0xD
set in 0xB
set addr 255
set bank 2
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x5
set addr 64
set bank 2
set load 0
set status 1
tick
expect out 0xF
tock
expect out 0xF
set in 0x6
set addr 128
set bank 2
set load 1
set status 1
tick
expect out 0x5
tock
expect out 0x6
set in 0x4
set addr 255
set bank 0
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x4
set in 0xA
set addr 64
set bank 7
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0xA
set in 0x9
set addr 0
set bank 1
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x9
set in 0x5
set addr 32
set bank 7
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x5
set in 0x9
set addr 32
set bank 6
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x1
set addr 0
set bank 1
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x1
set in 0xE
set addr 8
set bank 7
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xE
set in 0x7
set addr 8
set bank 3
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0x7
set addr 32
set bank 0
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x7
set in 0x7
set addr 255
set bank 6
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x7
set in 0x3
set addr 32
set bank 5
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x3
set in 0x8
set addr 4
set bank 6
set load 0
set status 0
tick
expect out 0xA
tock
expect out 0xA
set in 0xE
set addr 8
set bank 1
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xE
set in 0x3
set addr 2
set bank 0
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x3
set in 0x2
set addr 8
set bank 6
set load 0
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x3
set addr 64
set bank 1
set load 0
set status 1
tick
expect out 0x2
tock
expect out 0x2
set in 0xA
set addr 255
set bank 3
set load 1
set status 1
tick
expect out 0x9
tock
expect out 0xA
