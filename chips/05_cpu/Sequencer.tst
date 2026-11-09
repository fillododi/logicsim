// Sequencer: `second` is 1 in the second instruction cycle of JCN FIM FIN JUN JMS ISZ;
// it changes at X3 (period 7) and clears on reset. `finfetch` is `second` and FIN.
// Instruction cycles in period order, with the instruction kept over both cycles as
// InstrReg keeps it, then random periods. Generated from a model, seed 4004.
chip Sequencer
// Before any reset, `second` is unknown.
set opr 4
set opa 0
set period 7
set reset 0
tick
expect second *
expect finfetch *
tock
expect second *
expect finfetch *
// Reset, then instruction cycles as Timing and InstrReg run them.
set opr 0
set opa 0
set period 0
set reset 1
tick
expect second *
expect finfetch *
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 4
set opa 1
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
// Random periods and instructions, reset now and then.
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 2
set opa 5
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 15
set opa 2
set period 0
set reset 1
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 6
set opa 1
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 5
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 11
set opa 4
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 5
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 11
set opa 4
set period 4
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 4
set period 0
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 3
set opa 3
set period 1
set reset 1
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 5
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x1
set opr 4
set opa 1
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 5
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 5
set period 7
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 2
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 0
set opa 0
set period 6
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 6
set opa 1
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 14
set opa 9
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 5
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 14
set opa 9
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 3
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 15
set opa 2
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 2
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 11
set opa 4
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 5
set period 7
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 5
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 14
set opa 9
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 5
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 0
set opa 0
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 15
set opa 2
set period 7
set reset 1
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 13
set opa 3
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 4
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 6
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 5
set opa 2
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 7
set opa 9
set period 0
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 6
set opa 1
set period 4
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 1
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 4
set opa 1
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 1
set opa 6
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 3
set opa 2
set period 3
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 2
set opa 4
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x1
expect finfetch 0x1
tock
expect second 0x1
expect finfetch 0x1
set opr 5
set opa 2
set period 5
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 3
set opa 3
set period 7
set reset 0
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 5
set period 0
set reset 1
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 1
set opa 6
set period 7
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x1
expect finfetch 0x0
set opr 2
set opa 5
set period 2
set reset 1
tick
expect second 0x1
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 2
set opa 4
set period 3
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
set opr 3
set opa 2
set period 2
set reset 0
tick
expect second 0x0
expect finfetch 0x0
tock
expect second 0x0
expect finfetch 0x0
