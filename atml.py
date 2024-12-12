import sys

class Assembler:
    def __init__(self):
        
        #data
        self.functions = {
            "ADD": 0b000,
            "SUB": 0b001,
            "AND": 0b010,
            "ORR": 0b011,
            "LDR": 0b1,
            "STR": 0b0,
            "JMP": 0b0,
            "JPZ": 0b1
        }
        
        self.opcodes = {
            "ADD": 0b00,
            "SUB": 0b00,
            "AND": 0b00,
            "ORR": 0b00,
            "LDR": 0b01,
            "STR": 0b01,
            "JMP": 0b10,
            "JPZ": 0b10
        }

    def assemble(self, instruction):
        parts = instruction.split()
        func = parts[0]
        optype = self.opcodes.get(func)
        opcode = self.functions.get(func)
        if opcode is None:
            raise ValueError(f"Illegal instruction: {func}")

        #Sample instruction: OP Rd,RA,RB
        if optype == 0:
            reg_D = int(parts[1][1:])
            src_A = int(parts[2][1:])  
            if parts[3].startswith("#"):
                I = 1
                src_B = int(parts[3][1:]) 
                if not (0 <= src_B <= 2**4 - 1):
                    raise ValueError(f"Invalid DP immediate: {src_B}")
            else:
                I = 0
                src_B = int(parts[3][1:])
            return (optype << 14) | (I << 13) | (opcode << 10) | (reg_D << 7) | (src_A << 4) | src_B
        elif optype == 1:
            L = opcode           
            reg_D = int(parts[1][1:]) 
            src_A = int(parts[2][1:]) 
            if parts[3].startswith("#"):
                I = 1
                src_B = int(parts[3][1:]) 
                if not (0 <= src_B <= 2**6 - 1):
                    raise ValueError(f"Invalid MEM immediate: {src_B}")
            else:
                I = 0
                src_B = int(parts[3][1:])
            return (optype << 14) | (I << 13) | (L << 12) | (reg_D << 9) | (src_A << 6) | src_B
        elif optype == 2:
            Z = opcode
            src_A = int(parts[1][1:]) 
            if not (0 <= src_B <= 2**13 - 1):
                raise ValueError(f"Invalid BCH immediate: {src_B}")
            return (optype << 14) | (Z << 13) | src_A
        else:
            raise ValueError("Instrucción no soportada")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Execute as: python atml.py <input file> [<output file>]")
        sys.exit(1)

    input_file = sys.argv[1]  
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.nlc"  

    assembler = Assembler()


    with open(input_file, "r") as infile:
        instructions = infile.readlines()

    with open(output_file, "w") as outfile:
        for instr in instructions:
            instr = instr.strip() 
            if instr:
                machine_code = assembler.assemble(instr)
                outfile.write(f"{machine_code:04x}\n")

    print(f"El código máquina se ha guardado en {output_file}.")
