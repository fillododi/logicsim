// SRLatch: each row follows the one before, so a row with neither input checks
// that the latch keeps what the row before set or reset. set and reset are never 1
// together.
chip SRLatch
table set reset | out
    0 0 | *
    1 0 | 1
    0 0 | 1
    1 0 | 1
    0 0 | 1
    0 1 | 0
    0 0 | 0
    0 1 | 0
    0 0 | 0
    1 0 | 1
    0 1 | 0
    1 0 | 1
    0 0 | 1
end
