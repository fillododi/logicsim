// PC: reset, counting and wrapping at 0xFFF, jumps, calls and returns three deep, a fourth
// call overwriting the oldest return, returns past the bottom wrapping around, each
// control against the ones it outranks, then 200 random cycles (seed 4004). Each clock
// cycle checks out after its tick (still the old value) and after its tock.
chip PC
// Reset: address 0
set in 0x000
set inc 0
set load 0
set push 0
set pop 0
set reset 1
tick
expect out *
tock
expect out 0x000
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x000
tock
expect out 0x001
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x001
tock
expect out 0x002
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x002
tock
expect out 0x003
// Nothing asked: nothing changes
set in 0x000
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x003
tock
expect out 0x003
// Jump near the top, then count across it
set in 0xFFE
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x003
tock
expect out 0xFFE
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xFFE
tock
expect out 0xFFF
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xFFF
tock
expect out 0x000
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x000
tock
expect out 0x001
// Calls three deep, each with inc, then the returns
set in 0x123
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x001
tock
expect out 0x123
set in 0x400
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x123
tock
expect out 0x400
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x400
tock
expect out 0x401
set in 0x7F0
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x401
tock
expect out 0x7F0
set in 0xABC
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x7F0
tock
expect out 0xABC
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xABC
tock
expect out 0xABD
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xABD
tock
expect out 0x7F1
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x7F1
tock
expect out 0x402
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x402
tock
expect out 0x124
// A push without inc returns to the call itself
set in 0x200
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x124
tock
expect out 0x200
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x200
tock
expect out 0x124
// A fourth call overwrites the oldest return
set in 0x010
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x124
tock
expect out 0x010
set in 0x111
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x010
tock
expect out 0x111
set in 0x222
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x111
tock
expect out 0x222
set in 0x333
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x222
tock
expect out 0x333
set in 0x444
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x333
tock
expect out 0x444
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x444
tock
expect out 0x334
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x334
tock
expect out 0x223
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x223
tock
expect out 0x112
// Past the bottom: the pointer wraps to the newest address
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x112
tock
expect out 0x444
set in 0x000
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x444
tock
expect out 0x334
// Each control against the ones it outranks
set in 0x555
set inc 1
set load 1
set push 1
set pop 1
set reset 0
tick
expect out 0x334
tock
expect out 0x555
set in 0x666
set inc 1
set load 1
set push 0
set pop 1
set reset 0
tick
expect out 0x555
tock
expect out 0x335
set in 0x777
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x335
tock
expect out 0x777
set in 0x888
set inc 1
set load 1
set push 1
set pop 1
set reset 1
tick
expect out 0x777
tock
expect out 0x000
set in 0x000
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x000
tock
expect out 0x001
set in 0x999
set inc 0
set load 1
set push 1
set pop 0
set reset 0
tick
expect out 0x001
tock
expect out 0x999
// Random cycles: one control or a few at once
set in 0xCCA
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x999
tock
expect out 0x99A
set in 0x6F8
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x99A
tock
expect out 0x6F8
set in 0x094
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x6F8
tock
expect out 0x99A
set in 0x3D1
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x99A
tock
expect out 0x99B
set in 0x8E9
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x99B
tock
expect out 0x001
set in 0xEED
set inc 0
set load 0
set push 1
set pop 1
set reset 0
tick
expect out 0x001
tock
expect out 0xEED
set in 0x0DA
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xEED
tock
expect out 0xEEE
set in 0x571
set inc 0
set load 0
set push 0
set pop 0
set reset 1
tick
expect out 0xEEE
tock
expect out 0x000
set in 0xB40
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x000
tock
expect out 0x001
set in 0x12B
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x001
tock
expect out 0x002
set in 0x6D5
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x002
tock
expect out 0x003
set in 0x9F4
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x003
tock
expect out 0x004
set in 0x3CB
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x004
tock
expect out 0x3CB
set in 0xEB9
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x3CB
tock
expect out 0xEB9
set in 0x713
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xEB9
tock
expect out 0x713
set in 0x0CF
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x713
tock
expect out 0xEBA
set in 0x85C
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xEBA
tock
expect out 0xEBA
set in 0xBD2
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xEBA
tock
expect out 0xEBB
set in 0x98D
set inc 0
set load 1
set push 0
set pop 1
set reset 0
tick
expect out 0xEBB
tock
expect out 0x777
set in 0x04F
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x777
tock
expect out 0x6F8
set in 0x55D
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x6F8
tock
expect out 0x713
set in 0xA64
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x713
tock
expect out 0xEBB
set in 0x4A1
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xEBB
tock
expect out 0x777
set in 0x241
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x777
tock
expect out 0x6F8
set in 0xFFF
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x6F8
tock
expect out 0x713
set in 0xF6C
set inc 0
set load 1
set push 0
set pop 1
set reset 0
tick
expect out 0x713
tock
expect out 0xEBB
set in 0x098
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xEBB
tock
expect out 0xEBC
set in 0x53B
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xEBC
tock
expect out 0x53B
set in 0x533
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x53B
tock
expect out 0x777
set in 0xE5A
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x777
tock
expect out 0x778
set in 0x1D6
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x778
tock
expect out 0x1D6
set in 0xEAD
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x1D6
tock
expect out 0x1D7
set in 0xE60
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x1D7
tock
expect out 0x6F8
set in 0xD7B
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x6F8
tock
expect out 0x6F9
set in 0x0C7
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x6F9
tock
expect out 0x713
set in 0x8BF
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x713
tock
expect out 0x8BF
set in 0xC9B
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x8BF
tock
expect out 0xC9B
set in 0x420
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xC9B
tock
expect out 0xC9C
set in 0xE92
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xC9C
tock
expect out 0xE92
set in 0xF54
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xE92
tock
expect out 0xE93
set in 0xAB9
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xE93
tock
expect out 0xE94
set in 0x34A
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xE94
tock
expect out 0xC9C
set in 0x4E8
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xC9C
tock
expect out 0xC9D
set in 0xF65
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xC9D
tock
expect out 0xF65
set in 0x72B
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xF65
tock
expect out 0xF66
set in 0x820
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xF66
tock
expect out 0xF67
set in 0xC8F
set inc 1
set load 0
set push 1
set pop 1
set reset 0
tick
expect out 0xF67
tock
expect out 0xC8F
set in 0x496
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xC8F
tock
expect out 0x496
set in 0x13E
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x496
tock
expect out 0x497
set in 0xEAC
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x497
tock
expect out 0x498
set in 0x3E4
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x498
tock
expect out 0x3E4
set in 0x819
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x3E4
tock
expect out 0x819
set in 0x99C
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x819
tock
expect out 0x99C
set in 0xAD4
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x99C
tock
expect out 0xAD4
set in 0x60A
set inc 0
set load 1
set push 0
set pop 1
set reset 0
tick
expect out 0xAD4
tock
expect out 0x99D
set in 0xE25
set inc 0
set load 1
set push 0
set pop 1
set reset 0
tick
expect out 0x99D
tock
expect out 0x3E5
set in 0x03C
set inc 0
set load 0
set push 0
set pop 0
set reset 1
tick
expect out 0x3E5
tock
expect out 0x000
set in 0xB3E
set inc 1
set load 0
set push 1
set pop 1
set reset 0
tick
expect out 0x000
tock
expect out 0xB3E
set in 0x69A
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xB3E
tock
expect out 0xB3F
set in 0x3D1
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xB3F
tock
expect out 0xB40
set in 0xED8
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xB40
tock
expect out 0xED8
set in 0x720
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xED8
tock
expect out 0x720
set in 0xDE4
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x720
tock
expect out 0x721
set in 0x7A7
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x721
tock
expect out 0x722
set in 0xF5C
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x722
tock
expect out 0xF5C
set in 0x108
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xF5C
tock
expect out 0xF5D
set in 0xE0F
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xF5D
tock
expect out 0xE0F
set in 0x10B
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xE0F
tock
expect out 0x10B
set in 0xD97
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x10B
tock
expect out 0x10C
set in 0x0AC
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x10C
tock
expect out 0x10D
set in 0xAEC
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x10D
tock
expect out 0x10E
set in 0xE6F
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x10E
tock
expect out 0xE6F
set in 0x581
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xE6F
tock
expect out 0x581
set in 0xA63
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x581
tock
expect out 0x582
set in 0xF8A
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x582
tock
expect out 0x583
set in 0x997
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x583
tock
expect out 0x997
set in 0xD70
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x997
tock
expect out 0x998
set in 0x848
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x998
tock
expect out 0x998
set in 0x8FD
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x998
tock
expect out 0x999
set in 0x219
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x999
tock
expect out 0x99A
set in 0x5E3
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x99A
tock
expect out 0x5E3
set in 0xFEB
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x5E3
tock
expect out 0xFEB
set in 0x8E2
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xFEB
tock
expect out 0x5E4
set in 0x9C0
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x5E4
tock
expect out 0xE70
set in 0x423
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xE70
tock
expect out 0xE0F
set in 0x081
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xE0F
tock
expect out 0x081
set in 0x6F8
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x081
tock
expect out 0x6F8
set in 0xAFF
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x6F8
tock
expect out 0x6F9
set in 0xAF8
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x6F9
tock
expect out 0xAF8
set in 0x160
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xAF8
tock
expect out 0x6FA
set in 0xAEC
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x6FA
tock
expect out 0x082
set in 0xB38
set inc 0
set load 0
set push 1
set pop 1
set reset 0
tick
expect out 0x082
tock
expect out 0xB38
set in 0x106
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xB38
tock
expect out 0x106
set in 0xBCA
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x106
tock
expect out 0xB39
set in 0xDBB
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xB39
tock
expect out 0xDBB
set in 0x501
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xDBB
tock
expect out 0x082
set in 0x352
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x082
tock
expect out 0x083
set in 0xFB0
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x083
tock
expect out 0xFB0
set in 0xA56
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xFB0
tock
expect out 0xA56
set in 0xF6E
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xA56
tock
expect out 0xF6E
set in 0x6F3
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xF6E
tock
expect out 0xF6E
set in 0xA24
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xF6E
tock
expect out 0xF6F
set in 0xB94
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xF6F
tock
expect out 0xF70
set in 0x159
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xF70
tock
expect out 0x159
set in 0x12D
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x159
tock
expect out 0x12D
set in 0x41D
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x12D
tock
expect out 0x12E
set in 0x410
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x12E
tock
expect out 0x410
set in 0x06E
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x410
tock
expect out 0x06E
set in 0x8ED
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x06E
tock
expect out 0x411
set in 0xB55
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x411
tock
expect out 0xB55
set in 0xDCE
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xB55
tock
expect out 0xDCE
set in 0xBEC
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xDCE
tock
expect out 0x15A
set in 0x15B
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x15A
tock
expect out 0x15B
set in 0xE70
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x15B
tock
expect out 0xF71
set in 0x3D7
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xF71
tock
expect out 0x3D7
set in 0x696
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x3D7
tock
expect out 0x3D8
set in 0x0EE
set inc 1
set load 1
set push 1
set pop 0
set reset 0
tick
expect out 0x3D8
tock
expect out 0x0EE
set in 0x478
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x0EE
tock
expect out 0x0EE
set in 0x6E1
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x0EE
tock
expect out 0x3D9
set in 0x525
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x3D9
tock
expect out 0x3DA
set in 0xC63
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x3DA
tock
expect out 0x3DA
set in 0x59F
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x3DA
tock
expect out 0x3DB
set in 0x024
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x3DB
tock
expect out 0xF72
set in 0x7CE
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xF72
tock
expect out 0x7CE
set in 0x10F
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x7CE
tock
expect out 0x7CF
set in 0x28D
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x7CF
tock
expect out 0x28D
set in 0x837
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x28D
tock
expect out 0x837
set in 0x0AB
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x837
tock
expect out 0x838
set in 0x820
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x838
tock
expect out 0x28E
set in 0xBDA
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x28E
tock
expect out 0xF73
set in 0xF77
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xF73
tock
expect out 0x06E
set in 0x2A7
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x06E
tock
expect out 0x2A7
set in 0x795
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x2A7
tock
expect out 0x795
set in 0x013
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x795
tock
expect out 0x013
set in 0xE32
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x013
tock
expect out 0x796
set in 0x322
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x796
tock
expect out 0x322
set in 0x4AC
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x322
tock
expect out 0x4AC
set in 0x6E0
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x4AC
tock
expect out 0x4AC
set in 0x120
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x4AC
tock
expect out 0x4AD
set in 0x99C
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x4AD
tock
expect out 0x4AD
set in 0x9BD
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x4AD
tock
expect out 0x9BD
set in 0x41F
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x9BD
tock
expect out 0x9BD
set in 0x36D
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x9BD
tock
expect out 0x36D
set in 0x1A7
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x36D
tock
expect out 0x1A7
set in 0x685
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x1A7
tock
expect out 0x06F
set in 0xA47
set inc 0
set load 1
set push 1
set pop 0
set reset 0
tick
expect out 0x06F
tock
expect out 0xA47
set in 0x5DC
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xA47
tock
expect out 0xA48
set in 0xAC2
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xA48
tock
expect out 0xA49
set in 0x6DA
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xA49
tock
expect out 0xA4A
set in 0x844
set inc 1
set load 0
set push 0
set pop 1
set reset 1
tick
expect out 0xA4A
tock
expect out 0x000
set in 0x116
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x000
tock
expect out 0x001
set in 0x72A
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x001
tock
expect out 0x002
set in 0xEE4
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x002
tock
expect out 0xEE4
set in 0xB65
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xEE4
tock
expect out 0xEE5
set in 0x2F1
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xEE5
tock
expect out 0x002
set in 0xC21
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x002
tock
expect out 0x838
set in 0x132
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x838
tock
expect out 0x839
set in 0xBAB
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x839
tock
expect out 0x839
set in 0x94E
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x839
tock
expect out 0x83A
set in 0x17C
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x83A
tock
expect out 0x013
set in 0xD1C
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x013
tock
expect out 0xD1C
set in 0x2CD
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xD1C
tock
expect out 0xEE5
set in 0xB9D
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xEE5
tock
expect out 0x002
set in 0x556
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x002
tock
expect out 0x83A
set in 0xB0C
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x83A
tock
expect out 0xB0C
set in 0x9EB
set inc 0
set load 0
set push 0
set pop 0
set reset 1
tick
expect out 0xB0C
tock
expect out 0x000
set in 0x661
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x000
tock
expect out 0x661
set in 0x7E7
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x661
tock
expect out 0x661
set in 0xA8A
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x661
tock
expect out 0x662
set in 0x088
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x662
tock
expect out 0x663
set in 0xD64
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x663
tock
expect out 0x664
set in 0x7A2
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x664
tock
expect out 0x7A2
set in 0x53A
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x7A2
tock
expect out 0x7A3
set in 0xD1B
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x7A3
tock
expect out 0x7A4
set in 0xB94
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x7A4
tock
expect out 0xB94
set in 0xCC3
set inc 1
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xB94
tock
expect out 0x7A5
set in 0x814
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x7A5
tock
expect out 0x7A6
set in 0x9CF
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x7A6
tock
expect out 0x7A7
set in 0xFE7
set inc 0
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x7A7
tock
expect out 0x7A7
set in 0xC66
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x7A7
tock
expect out 0x665
set in 0x338
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x665
tock
expect out 0x666
set in 0x97B
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x666
tock
expect out 0x667
set in 0xFCD
set inc 1
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x667
tock
expect out 0xFCD
set in 0xA1C
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0xFCD
tock
expect out 0xA1C
set in 0x5AF
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xA1C
tock
expect out 0xA1D
set in 0x5CD
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xA1D
tock
expect out 0xA1E
set in 0x779
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0xA1E
tock
expect out 0x83B
set in 0x161
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x83B
tock
expect out 0x83C
set in 0xE84
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x83C
tock
expect out 0x83D
set in 0xFA4
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x83D
tock
expect out 0xFA4
set in 0x6B9
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xFA4
tock
expect out 0x6B9
set in 0xDD1
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x6B9
tock
expect out 0x6BA
set in 0xE44
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0x6BA
tock
expect out 0x6BB
set in 0xD15
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x6BB
tock
expect out 0xFA4
set in 0x714
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0xFA4
tock
expect out 0x714
set in 0x0FC
set inc 0
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x714
tock
expect out 0x0FC
set in 0x0A6
set inc 0
set load 1
set push 0
set pop 0
set reset 0
tick
expect out 0x0FC
tock
expect out 0x0A6
set in 0x89C
set inc 0
set load 0
set push 0
set pop 1
set reset 0
tick
expect out 0x0A6
tock
expect out 0x714
set in 0xE01
set inc 1
set load 0
set push 1
set pop 0
set reset 0
tick
expect out 0x714
tock
expect out 0xE01
set in 0xB8E
set inc 1
set load 0
set push 0
set pop 0
set reset 0
tick
expect out 0xE01
tock
expect out 0xE02
