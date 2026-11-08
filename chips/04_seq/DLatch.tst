// DLatch: each row follows the one before. While load is 1, out follows in through
// both changes; while load is 0, out keeps its value whichever way in goes.
chip DLatch
table in load | out
    0 0 | *
    1 1 | 1
    0 1 | 0
    1 1 | 1
    1 0 | 1
    0 0 | 1
    1 0 | 1
    0 1 | 0
    0 0 | 0
    1 0 | 0
    0 0 | 0
    0 1 | 0
    1 1 | 1
    0 0 | 1
end
