// Timing: period counts 0 (A1) to 7 (X3), one step per clock cycle; reset makes the
// next period A1; sync is 1 during X3. Checked after each tick (still the old period)
// and after each tock (the new one). Generated from a model, seed 4004.
chip Timing
// Before any reset the count is unknown.
set reset 0
tick
expect period *
expect sync *
tock
expect period *
expect sync *
// Reset, then two and a half wraps through A1..X3.
set reset 1
tick
expect period *
expect sync *
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
set reset 0
tick
expect period 7
expect sync 1
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
set reset 0
tick
expect period 7
expect sync 1
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
// A reset in the middle of a cycle (at X2), and one held for three cycles.
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 1
tick
expect period 6
expect sync 0
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 1
tick
expect period 3
expect sync 0
tock
expect period 0
expect sync 0
set reset 1
tick
expect period 0
expect sync 0
tock
expect period 0
expect sync 0
set reset 1
tick
expect period 0
expect sync 0
tock
expect period 0
expect sync 0
// A reset at X3, where the count would wrap anyway.
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
set reset 1
tick
expect period 7
expect sync 1
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
// Random cycles, reset about one time in eight.
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
set reset 1
tick
expect period 7
expect sync 1
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 1
tick
expect period 6
expect sync 0
tock
expect period 0
expect sync 0
set reset 1
tick
expect period 0
expect sync 0
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 1
tick
expect period 3
expect sync 0
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
set reset 1
tick
expect period 7
expect sync 1
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 1
tick
expect period 5
expect sync 0
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
set reset 0
tick
expect period 7
expect sync 1
tock
expect period 0
expect sync 0
set reset 0
tick
expect period 0
expect sync 0
tock
expect period 1
expect sync 0
set reset 0
tick
expect period 1
expect sync 0
tock
expect period 2
expect sync 0
set reset 0
tick
expect period 2
expect sync 0
tock
expect period 3
expect sync 0
set reset 0
tick
expect period 3
expect sync 0
tock
expect period 4
expect sync 0
set reset 0
tick
expect period 4
expect sync 0
tock
expect period 5
expect sync 0
set reset 0
tick
expect period 5
expect sync 0
tock
expect period 6
expect sync 0
set reset 0
tick
expect period 6
expect sync 0
tock
expect period 7
expect sync 1
