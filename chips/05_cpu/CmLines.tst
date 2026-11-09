// CmLines: every bank and on (16 rows). Bank 0 raises CM-RAM0 alone; banks 1-7 are
// their number on CM-RAM1..3, as in the DCL table of Intel's MCS-4 manual.
chip CmLines
table bank on | cmram
    0 0 | 0b0000
    1 0 | 0b0000
    2 0 | 0b0000
    3 0 | 0b0000
    4 0 | 0b0000
    5 0 | 0b0000
    6 0 | 0b0000
    7 0 | 0b0000
    0 1 | 0b0001
    1 1 | 0b0010
    2 1 | 0b0100
    3 1 | 0b0110
    4 1 | 0b1000
    5 1 | 0b1010
    6 1 | 0b1100
    7 1 | 0b1110
end
