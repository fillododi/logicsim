// RAM4002: every main character and every status character written and read back,
// status characters named with addr[2..3] set to anything, main and status kept apart,
// then 96 random cycles (seed 4004). Each write checks out after its tick and its tock.
chip RAM4002
// Every main character: register addr[4..5], character addr[0..3]
set in 0x5
set addr 0
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x2
set addr 1
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x4
set addr 2
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xE
set addr 3
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xD
set addr 4
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x3
set addr 5
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0xB
set addr 6
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 7
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xF
set addr 8
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0x9
set addr 9
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xA
set addr 10
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x2
set addr 11
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xB
set addr 12
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 13
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x8
set addr 14
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
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
set in 0x8
set addr 17
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x9
set addr 18
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0x5
set addr 19
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0x1
set addr 20
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xD
set addr 21
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x4
set addr 22
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x2
set addr 23
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x2
set addr 24
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x1
set addr 25
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xE
set addr 26
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x8
set addr 27
set load 1
set status 0
tick
expect out *
tock
expect out 0x8
set in 0x0
set addr 28
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0x1
set addr 29
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x1
set addr 30
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x6
set addr 31
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xA
set addr 32
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x6
set addr 33
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x2
set addr 34
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0x3
set addr 35
set load 1
set status 0
tick
expect out *
tock
expect out 0x3
set in 0x6
set addr 36
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0x6
set addr 37
set load 1
set status 0
tick
expect out *
tock
expect out 0x6
set in 0xE
set addr 38
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0x5
set addr 39
set load 1
set status 0
tick
expect out *
tock
expect out 0x5
set in 0xC
set addr 40
set load 1
set status 0
tick
expect out *
tock
expect out 0xC
set in 0xE
set addr 41
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xA
set addr 42
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x1
set addr 43
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x7
set addr 44
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0xB
set addr 45
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x1
set addr 46
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x4
set addr 47
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0xA
set addr 48
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 49
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x4
set addr 50
set load 1
set status 0
tick
expect out *
tock
expect out 0x4
set in 0x1
set addr 51
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0x9
set addr 52
set load 1
set status 0
tick
expect out *
tock
expect out 0x9
set in 0xB
set addr 53
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
set in 0x0
set addr 54
set load 1
set status 0
tick
expect out *
tock
expect out 0x0
set in 0xD
set addr 55
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0xA
set addr 56
set load 1
set status 0
tick
expect out *
tock
expect out 0xA
set in 0x7
set addr 57
set load 1
set status 0
tick
expect out *
tock
expect out 0x7
set in 0x2
set addr 58
set load 1
set status 0
tick
expect out *
tock
expect out 0x2
set in 0xE
set addr 59
set load 1
set status 0
tick
expect out *
tock
expect out 0xE
set in 0xF
set addr 60
set load 1
set status 0
tick
expect out *
tock
expect out 0xF
set in 0xD
set addr 61
set load 1
set status 0
tick
expect out *
tock
expect out 0xD
set in 0x1
set addr 62
set load 1
set status 0
tick
expect out *
tock
expect out 0x1
set in 0xB
set addr 63
set load 1
set status 0
tick
expect out *
tock
expect out 0xB
// Every status character: register addr[4..5], character addr[0..1]; addr[2..3] don't matter
set in 0xC
set addr 0
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xC
set addr 9
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0x1
set addr 6
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0x3
set addr 7
set load 1
set status 1
tick
expect out *
tock
expect out 0x3
set in 0xB
set addr 24
set load 1
set status 1
tick
expect out *
tock
expect out 0xB
set in 0xD
set addr 25
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x8
set addr 22
set load 1
set status 1
tick
expect out *
tock
expect out 0x8
set in 0xD
set addr 31
set load 1
set status 1
tick
expect out *
tock
expect out 0xD
set in 0x1
set addr 36
set load 1
set status 1
tick
expect out *
tock
expect out 0x1
set in 0xA
set addr 45
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0x4
set addr 38
set load 1
set status 1
tick
expect out *
tock
expect out 0x4
set in 0xC
set addr 39
set load 1
set status 1
tick
expect out *
tock
expect out 0xC
set in 0xA
set addr 60
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
set in 0xE
set addr 49
set load 1
set status 1
tick
expect out *
tock
expect out 0xE
set in 0x6
set addr 50
set load 1
set status 1
tick
expect out *
tock
expect out 0x6
set in 0xA
set addr 63
set load 1
set status 1
tick
expect out *
tock
expect out 0xA
// Read everything back: the status writes left the main characters alone
set in 0x0
set addr 0
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 1
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 2
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 3
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 4
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 5
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 6
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 7
set load 0
set status 0
eval
expect out 0x1
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
expect out 0x9
set in 0x0
set addr 10
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 11
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 12
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 13
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 14
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 15
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 16
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 17
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 18
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 19
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 20
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 21
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 22
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 23
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 24
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 25
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 26
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 27
set load 0
set status 0
eval
expect out 0x8
set in 0x0
set addr 28
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 29
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 30
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 31
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 32
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 33
set load 0
set status 0
eval
expect out 0x6
set in 0x0
set addr 34
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 35
set load 0
set status 0
eval
expect out 0x3
set in 0x0
set addr 36
set load 0
set status 0
eval
expect out 0x6
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
expect out 0xE
set in 0x0
set addr 39
set load 0
set status 0
eval
expect out 0x5
set in 0x0
set addr 40
set load 0
set status 0
eval
expect out 0xC
set in 0x0
set addr 41
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 42
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 43
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 44
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 45
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 46
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 47
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 48
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 49
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 50
set load 0
set status 0
eval
expect out 0x4
set in 0x0
set addr 51
set load 0
set status 0
eval
expect out 0x1
set in 0x0
set addr 52
set load 0
set status 0
eval
expect out 0x9
set in 0x0
set addr 53
set load 0
set status 0
eval
expect out 0xB
set in 0x0
set addr 54
set load 0
set status 0
eval
expect out 0x0
set in 0x0
set addr 55
set load 0
set status 0
eval
expect out 0xD
set in 0x0
set addr 56
set load 0
set status 0
eval
expect out 0xA
set in 0x0
set addr 57
set load 0
set status 0
eval
expect out 0x7
set in 0x0
set addr 58
set load 0
set status 0
eval
expect out 0x2
set in 0x0
set addr 59
set load 0
set status 0
eval
expect out 0xE
set in 0x0
set addr 60
set load 0
set status 0
eval
expect out 0xF
set in 0x0
set addr 61
set load 0
set status 0
eval
expect out 0xD
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
expect out 0xB
set in 0x0
set addr 0
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 1
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 2
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 3
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 4
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 5
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 6
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 7
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 8
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 9
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 10
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 11
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 12
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 13
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 14
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 15
set load 0
set status 1
eval
expect out 0x3
set in 0x0
set addr 16
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 17
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 18
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 19
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 20
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 21
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 22
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 23
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 24
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 25
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 26
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 27
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 28
set load 0
set status 1
eval
expect out 0xB
set in 0x0
set addr 29
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 30
set load 0
set status 1
eval
expect out 0x8
set in 0x0
set addr 31
set load 0
set status 1
eval
expect out 0xD
set in 0x0
set addr 32
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 33
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 34
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 35
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 36
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 37
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 38
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 39
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 40
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 41
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 42
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 43
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 44
set load 0
set status 1
eval
expect out 0x1
set in 0x0
set addr 45
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 46
set load 0
set status 1
eval
expect out 0x4
set in 0x0
set addr 47
set load 0
set status 1
eval
expect out 0xC
set in 0x0
set addr 48
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 49
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 50
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 51
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 52
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 53
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 54
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 55
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 56
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 57
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 58
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 59
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 60
set load 0
set status 1
eval
expect out 0xA
set in 0x0
set addr 61
set load 0
set status 1
eval
expect out 0xE
set in 0x0
set addr 62
set load 0
set status 1
eval
expect out 0x6
set in 0x0
set addr 63
set load 0
set status 1
eval
expect out 0xA
// Random cycles
set in 0xA
set addr 25
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x5
set addr 55
set load 0
set status 0
tick
expect out 0xD
tock
expect out 0xD
set in 0x6
set addr 1
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x6
set in 0x5
set addr 57
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x5
set in 0xE
set addr 40
set load 0
set status 1
tick
expect out 0x1
tock
expect out 0x1
set in 0xF
set addr 13
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x1
set addr 2
set load 0
set status 1
tick
expect out 0x1
tock
expect out 0x1
set in 0xE
set addr 33
set load 0
set status 1
tick
expect out 0xA
tock
expect out 0xA
set in 0x8
set addr 62
set load 0
set status 1
tick
expect out 0x6
tock
expect out 0x6
set in 0xF
set addr 4
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0xF
set in 0xB
set addr 5
set load 1
set status 1
tick
expect out 0xC
tock
expect out 0xB
set in 0x0
set addr 50
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x0
set in 0x8
set addr 29
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x8
set in 0xB
set addr 9
set load 0
set status 0
tick
expect out 0x9
tock
expect out 0x9
set in 0xD
set addr 61
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0xD
set in 0xB
set addr 20
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xB
set in 0xE
set addr 43
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x9
set addr 5
set load 1
set status 0
tick
expect out 0x3
tock
expect out 0x9
set in 0x6
set addr 44
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x6
set in 0xC
set addr 58
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xC
set in 0x1
set addr 15
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x1
set in 0x6
set addr 48
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x6
set in 0x4
set addr 8
set load 1
set status 0
tick
expect out 0xF
tock
expect out 0x4
set in 0xA
set addr 36
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xA
set in 0x4
set addr 32
set load 0
set status 0
tick
expect out 0xA
tock
expect out 0xA
set in 0x0
set addr 7
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x0
set addr 40
set load 1
set status 1
tick
expect out 0x1
tock
expect out 0x0
set in 0x6
set addr 20
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x6
set in 0xC
set addr 61
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0xC
set in 0xD
set addr 23
set load 0
set status 0
tick
expect out 0x2
tock
expect out 0x2
set in 0x0
set addr 34
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x0
set in 0x0
set addr 32
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0x0
set in 0xB
set addr 44
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x2
set addr 4
set load 1
set status 0
tick
expect out 0xD
tock
expect out 0x2
set in 0x3
set addr 10
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x3
set in 0x8
set addr 7
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x9
set addr 44
set load 0
set status 0
tick
expect out 0x6
tock
expect out 0x6
set in 0x8
set addr 2
set load 0
set status 0
tick
expect out 0x4
tock
expect out 0x4
set in 0x2
set addr 62
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0xA
set addr 29
set load 0
set status 0
tick
expect out 0x8
tock
expect out 0x8
set in 0xB
set addr 51
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0xB
set in 0xB
set addr 37
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0xB
set in 0x1
set addr 1
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x1
set in 0x8
set addr 45
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x7
set addr 38
set load 1
set status 1
tick
expect out 0x4
tock
expect out 0x7
set in 0x6
set addr 57
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x6
set in 0xB
set addr 36
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0xB
set in 0x1
set addr 56
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x1
set in 0xD
set addr 12
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x4
set addr 53
set load 0
set status 0
tick
expect out 0xB
tock
expect out 0xB
set in 0x6
set addr 40
set load 0
set status 0
tick
expect out 0xC
tock
expect out 0xC
set in 0x5
set addr 26
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0xC
set addr 4
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xC
set in 0x4
set addr 37
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x4
set in 0x9
set addr 42
set load 1
set status 0
tick
expect out 0xA
tock
expect out 0x9
set in 0xE
set addr 53
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0xE
set in 0xE
set addr 13
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xE
set in 0xF
set addr 50
set load 1
set status 1
tick
expect out 0x0
tock
expect out 0xF
set in 0xB
set addr 28
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0xE
set addr 12
set load 1
set status 1
tick
expect out 0xF
tock
expect out 0xE
set in 0xF
set addr 41
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0xF
set in 0xA
set addr 23
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0xA
set in 0xA
set addr 18
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xA
set in 0x6
set addr 21
set load 1
set status 1
tick
expect out 0xD
tock
expect out 0x6
set in 0x7
set addr 47
set load 1
set status 0
tick
expect out 0x4
tock
expect out 0x7
set in 0x2
set addr 63
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x2
set in 0x6
set addr 4
set load 1
set status 0
tick
expect out 0xC
tock
expect out 0x6
set in 0x8
set addr 53
set load 0
set status 1
tick
expect out 0x6
tock
expect out 0x6
set in 0xB
set addr 19
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xB
set in 0xF
set addr 48
set load 0
set status 1
tick
expect out 0x6
tock
expect out 0x6
set in 0xD
set addr 29
set load 0
set status 1
tick
expect out 0x6
tock
expect out 0x6
set in 0xC
set addr 0
set load 1
set status 0
tick
expect out 0x5
tock
expect out 0xC
set in 0xF
set addr 30
set load 0
set status 0
tick
expect out 0x1
tock
expect out 0x1
set in 0x7
set addr 4
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x7
set in 0x9
set addr 46
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0x9
set in 0x0
set addr 34
set load 1
set status 1
tick
expect out 0x7
tock
expect out 0x0
set in 0xA
set addr 5
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0xA
set in 0x8
set addr 52
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0x8
set in 0x2
set addr 60
set load 1
set status 1
tick
expect out 0x8
tock
expect out 0x2
set in 0x5
set addr 36
set load 1
set status 0
tick
expect out 0xB
tock
expect out 0x5
set in 0x7
set addr 46
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x7
set in 0x4
set addr 1
set load 1
set status 1
tick
expect out 0xB
tock
expect out 0x4
set in 0xB
set addr 17
set load 1
set status 1
tick
expect out 0x6
tock
expect out 0xB
set in 0x8
set addr 12
set load 1
set status 1
tick
expect out 0xE
tock
expect out 0x8
set in 0x9
set addr 41
set load 1
set status 1
tick
expect out 0xA
tock
expect out 0x9
set in 0x4
set addr 17
set load 0
set status 1
tick
expect out 0xB
tock
expect out 0xB
set in 0x7
set addr 11
set load 1
set status 0
tick
expect out 0x2
tock
expect out 0x7
set in 0x5
set addr 20
set load 1
set status 0
tick
expect out 0x6
tock
expect out 0x5
set in 0xB
set addr 17
set load 1
set status 0
tick
expect out 0x8
tock
expect out 0xB
set in 0x3
set addr 27
set load 0
set status 1
tick
expect out 0xD
tock
expect out 0xD
set in 0x4
set addr 53
set load 1
set status 0
tick
expect out 0xE
tock
expect out 0x4
set in 0x7
set addr 49
set load 1
set status 0
tick
expect out 0x7
tock
expect out 0x7
set in 0x5
set addr 59
set load 0
set status 0
tick
expect out 0xE
tock
expect out 0xE
set in 0x8
set addr 54
set load 0
set status 0
tick
expect out 0x0
tock
expect out 0x0
set in 0x8
set addr 52
set load 1
set status 0
tick
expect out 0x9
tock
expect out 0x8
set in 0xB
set addr 51
set load 1
set status 0
tick
expect out 0x1
tock
expect out 0xB
