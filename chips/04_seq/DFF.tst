// DFF: out(t) = in(t-1). Each cycle checks out after its tick (still the old value,
// which fails a latch open while clock is 1) and after its tock (the new one). Some
// cycles then change in while the clock is low and settle the chip: out must not
// follow, which fails a latch open while clock is 0. Others change in between the
// tick and the tock: the value stored at the tick wins.
chip DFF
set in 0
tick
expect out *
tock
expect out 0
set in 1
eval
expect out 0
set in 1
tick
expect out 0
tock
expect out 1
set in 0
eval
expect out 1
set in 1
tick
expect out 1
tock
expect out 1
set in 0
tick
expect out 1
set in 1
tock
expect out 0
set in 1
eval
expect out 0
set in 1
tick
expect out 0
tock
expect out 1
set in 0
tick
expect out 1
tock
expect out 0
set in 1
eval
expect out 0
set in 0
tick
expect out 0
tock
expect out 0
set in 1
tick
expect out 0
set in 0
tock
expect out 1
set in 0
eval
expect out 1
set in 0
tick
expect out 1
tock
expect out 0
