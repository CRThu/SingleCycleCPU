# SingleCycleCPU

carrot's simple single-cycle CPU -- CRT4004

## Instruction Structure

| Bus     | [31:26] | [25:21]   | [20:16]  | [15:11] | [10:6] | [5:0]  |
| :-----: | :-----: | :-------: | :------: | :-----: | :----: | :----: |
| cu,reg  | op      | addr1     | addr2    |         |        | funct  |
| reg     |         |           | addr3A   | addr3B  |        |        |
| imm     |         |           |          | immH    | immM   | immL   |

| Bus     | [31:26] | [25:21]   | [20:16]  | [15:11] | [10:6] | [5:0]  |
| :-----: | :-----: | :-------: | :------: | :-----: | :----: | :----: |
| R-Type  | 000000  | A_addr    | B_addr   | Y_addr  | x      | funct  |
| lw      | 100011  | *mem_addr | reg_addr | immH    | immM   | immL   |
| sw      | 101011  | *mem_addr | reg_addr | immH    | immM   | immL   |
| beq     | 000100  | A_addr    | B_addr   | immH    | immM   | immL   |
| addi    | 001000  | A_addr    | Y_addr   | immH    | immM   | immL   |

## Instruction Introduce

### when execute R-Type

calculate A and B and store to Y register.

| R-Type | funct  |
| :----: | :----: |
| ADD    | 100000 |
| SUB    | 100010 |
| AND    | 100100 |
| OR     | 100101 |
| SLT    | 101010 |

### when execute lw

read memory data to register, memory address = mem_addr + imm, reg address = reg_addr;

### when execute sw

write register data to memory, memory address = mem_addr + imm, reg address = reg_addr;

### when execute beq

if register A = B, Branch to Address = (imm << 2) + (PC + 4).

### when execute addi

Y = A + imm.

## storage size

ROM : 2K * 8b = 16Kb

REG : 31 * 32b = 992b

RAM : 256 * 32b = 8Kb

RAM(Reserved) : 4G * 32b = 128Gb
