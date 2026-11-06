// DMux4Way: every input combination
chip DMux4Way
table in sel  | a b c d
    0  0b00 | 0 0 0 0
    0  0b01 | 0 0 0 0
    0  0b10 | 0 0 0 0
    0  0b11 | 0 0 0 0
    1  0b00 | 1 0 0 0
    1  0b01 | 0 1 0 0
    1  0b10 | 0 0 1 0
    1  0b11 | 0 0 0 1
end
