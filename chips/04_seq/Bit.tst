// Bit: load each value, then hold or replace it with every in and load
chip Bit
set in 0
set load 1
tick
tock
expect out 0
set in 0
set load 0
tick
expect out 0
tock
expect out 0
set in 0
set load 1
tick
expect out 0
tock
expect out 0
set in 1
set load 0
tick
expect out 0
tock
expect out 0
set in 1
set load 1
tick
expect out 0
tock
expect out 1
set in 0
set load 1
tick
expect out 1
tock
expect out 0
set in 1
set load 1
tick
expect out 0
tock
expect out 1
set in 0
set load 0
tick
expect out 1
tock
expect out 1
set in 0
set load 1
tick
expect out 1
tock
expect out 0
set in 1
set load 1
tick
expect out 0
tock
expect out 1
set in 1
set load 0
tick
expect out 1
tock
expect out 1
set in 1
set load 1
tick
expect out 1
tock
expect out 1
