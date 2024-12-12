#Simple asembler for enlec ISA

import sys
import re

BCH = r"^([A-Za-z]+:)?\s*(JMP|JPZ)\s+([A-Za-z][A-Za-z0-9]*)$"
CMD = r"^([A-Za-z]+:)?\s*([A-Za-z]+)\s+(R[0-7]),(R[0-7]),(#[0-9]+|R[0-7])$"
LBL = r"^([A-Za-z]+):$"


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
        
        self.labels = {}

    def assemble(self, instruction):
        func = instruction.split(" ")[0]
        
        #hacky way to remove the func
        parts = instruction.replace(func + " ","").split(",")        
        optype = self.opcodes.get(func)
        opcode = self.functions.get(func)
        if opcode is None:
            raise ValueError(f"Illegal instruction: {func}")

        #Sample instruction: OP Rd,RA,RB
        #select operation type
        if optype == 0:
            reg_D = int(parts[0][1:])
            src_A = int(parts[1][1:])  
            if parts[2].startswith("#"):
                I = 1
                src_B = int(parts[2][1:]) 
                if not (0 <= src_B <= 2**4 - 1):
                    raise ValueError(f"Invalid DP immediate: {src_B}")
            else:
                I = 0
                src_B = int(parts[2][1:])
            return (optype << 14) | (I << 13) | (opcode << 10) | (reg_D << 7) | (src_A << 4) | src_B
        elif optype == 1:
            L = opcode           
            
            if not (parts[1].startswith("[") and parts[2].endswith("]")):
                raise ValueError(f"Invalid use of brackets")
                        
            reg_D = int(parts[0][1:]) 
            src_A = int(parts[1][2:]) 
            if parts[2].startswith("#"):
                I = 1
                src_B = int(parts[2][1:-1]) 
                if not (0 <= src_B <= 2**6 - 1):
                    raise ValueError(f"Invalid MEM immediate: {src_B}")
            else:
                I = 0
                src_B = int(parts[2][1:2])
            return (optype << 14) | (I << 13) | (L << 12) | (reg_D << 9) | (src_A << 6) | src_B
        elif optype == 2:
            Z = opcode
            src_A = self.labels.get(parts[0])
            
            if src_A is None:
                raise ValueError(f"Label not defined: {parts[0]}")
            
            if not (0 <= src_A <= 2**13 - 1):
                raise ValueError(f"Invalid BCH label: {src_B}")
            return (optype << 14) | (Z << 13) | src_A
        else:
            raise ValueError("Illegal optype")


if __name__ == "__main__":
    print("ATML assembler - v1.0 - 2024")
    if len(sys.argv) < 2:
        print("Execute as: python atml.py <input file> [<output file>]")
        sys.exit(1)

    input_file = sys.argv[1]  
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.nlc"  

    assembler = Assembler()


    instructions = []
    addr = 0
    
    #Load file and parse instructions
    with open(input_file, "r") as infile:
        for line in infile:
            l = line.strip()
            if not l:
                continue    
                    
            #check if matchs
            match_lbl = re.match(LBL,l)
            match_cmd = re.match(CMD,l)
            match_bch = re.match(BCH,l)
            if match_lbl:
                assembler.labels[l[:-1]] = addr
            elif match_cmd or match_bch:
                sel = (match_cmd or match_bch)
                if (sel.group(1)):
                    assembler.labels[sel.group(1)] = addr 
                    instr = sel.string.split(":",maxsplit=1)[1].strip()
                else:
                    instr = sel.string
                instructions.append(instr)
                addr += 1
            else:
                raise ValueError(f"Invalid instruction. {l}")
    
    #print(instructions)
    #print(assembler.labels)
    
    with open(output_file, "w") as outfile:
        for idx,instr in enumerate(instructions):
            machine_code = assembler.assemble(instr)
            outfile.write(f"{machine_code:04x}\n")

    print(f"SUCCESS: Machine code saved to {output_file}.")
