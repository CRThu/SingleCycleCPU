# SingleCycleCPU

carrot's simple single-cycle CPU -- CRT4004

## Instruction Structure

|  Bus   | [31:26] | [25:21] | [20:16] | [15:11] | [10:6] | [5:0] |
| :----: | :-----: | :-----: | :-----: | :-----: | :----: | :---: |
|cu,reg|op|addr1|addr2|||funct|
|reg|||addr3A|addr3B|||
|imm||||immH|immM|immL|