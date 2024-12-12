# enlec
**ENLEC** is a simulator of a 16-bit CPU using a fictional ISA inspired by the ARM architecture, designed to create a computing system capable of low-level graphics operations (to-do).



## Building
The source code is written in **C** and is compatible with standard compilers like GCC.
1. Clone the repository:
   ```bash
   git clone https://github.com/marcelochincha/enlec.git
   cd enlec
   ```

2. Compile the emulator:
   ```bash
   gcc -o enlec enlec.c
   ```

## Usage
To use the emulator, you need to compile an assembly source file using the `atml.py` assembler:

1. Assemble the program:
   ```bash
   python3 atml.py <input_file> [<output_file>]
   ```

2. Load the program into the emulator:
   ```bash
   ./enlec <output_file>
   ```

## ISA
The defined architecture supports operations for data processing, memory access, and control flow. Instructions are grouped into three types:
### DP type

| **Instruction** | **Description**                      | **Name**            | **Operation**                |
|------------------|--------------------------------------|-----------------------|------------------------------|
| `ADD`           | Add two registers                   | `ADD rD, rA, srcB` | `rD := rA + srcB`        |
| `SUB`           | Subtract two registers              | `SUB rD, rA, srcB` | `rD := rA - srcB`        |
| `ORR`           | Logical OR between two registers    | `ORR rD, rA, srcB` | `rD := rA or srcB`       |
| `AND`           | Logical AND between two registers   | `AND rD, rA, srcB` | `rD := rA and srcB`      |

### MEM type
| **Instruction** | **Description**                      | **Name**            | **Operation**                |
|------------------|--------------------------------------|-----------------------|------------------------------|
| `LDR`           | Load value from memory to register  | `LDR rD, [rA, srcB]`       | `rD := MEM[rA + srcB]`            |
| `STR`           | Store value from register to memory | `STR rD, [rA, srcB]`       | `MEM[rA + srcB] := rD`            |

### BCH type
| **Instruction** | **Description**                      | **Name**            | **Operation**                |
|------------------|--------------------------------------|-----------------------|------------------------------|
| `JMP`           | Unconditional jump to an address    | `JMP LABEL`           | `PC := [LABEL]`                 |
| `JPZ`           | Jump if zero flag is set            | `JPZ LABEL`           | `if ZF == 1: PC := [LABEL]`     |

### Registers
- **Rn:** General-purpose registers (R0-R6).
- **PC:** Program Counter. (R7)

