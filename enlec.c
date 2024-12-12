// ENLEC16 - CPU EMULATOR - V1.0 : 12-11-2024
// 16BIT - ISA FORMAT
//  3 TYPES
//  DATA
//  MEMORY
//  JUMP

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned short WORD;

#define MEM_M_SIZE 4

// SIZE IN WORDS
#define MEM_SIZE MEM_M_SIZE *MEM_M_SIZE
#define NREGS 8
#define REG_PC 7

// Utilities
#define GET_BITS(value, shift, mask) (((value) >> (shift)) & (mask))
#define GET_TYPE(instr) GET_BITS(instr, 14, 0b11)
#define GET_I(instr) GET_BITS(instr, 13, 0b1)
#define GET_L(instr) GET_BITS(instr, 12, 0b1)
#define GET_Z(instr) GET_BITS(instr, 12, 0b1)

// For DP DECODING
#define GET_DP_FUNC(instr) GET_BITS(instr, 10, 0b111)
#define GET_DP_SRC_D(instr) GET_BITS(instr, 7, 0b111)
#define GET_DP_SRC_A(instr) GET_BITS(instr, 4, 0b111)
#define GET_DP_SRC_B_IMM(instr) GET_BITS(instr, 0, 0b1111)
#define GET_DP_SRC_B_REG(instr) GET_BITS(instr, 0, 0b111)

// For MEM DECODING
// 01 IL XXX XXX ABCDEF
// 2  2  3   3   6
#define GET_MEM_SRC_D(instr) GET_BITS(instr, 9, 0b111)
#define GET_MEM_SRC_A(instr) GET_BITS(instr, 6, 0b111)
#define GET_MEM_SRC_B_IMM(instr) GET_BITS(instr, 0, 0b111111)
#define GET_MEM_SRC_B_REG(instr) GET_BITS(instr, 0, 0b111)

// For BCH DECODING
#define GET_JMP_IMM(instr) GET_BITS(instr, 0, 0b1111111111111)

// MACHINE CODE

// FUNCS
#define ADD 0b000
#define SUB 0b001
#define AND 0b010
#define ORR 0b011
#define LDR 0b100
#define STR 0b101
#define JMP 0b110
#define JPZ 0b111

// OP TYPES
#define DP 0b00
#define MEM 0b01
#define BCH 0b10
#define SPC 0b11

// ALU-OP
// 0 +
// 1 -
// 2 |
// 3 &

// Global variables
int END_ROM = 0;

// MEM
WORD RAM[MEM_SIZE], ROM[MEM_SIZE];
WORD R[NREGS] = {0};
WORD PC = 0, FLAG_Z = 0;
WORD INSTR;

//
// INITIALIZER
//
void init()
{
    PC = 0;
    FLAG_Z = 0;
    for (int i = 0; i < NREGS; i++)
    {
        R[i] = 0;
    }
}

//
// CPU
//

void fetch()
{
    INSTR = ROM[PC];
}

// THIS IS GOING TO BE USED BY THE EXECUTE ROUTINE
unsigned char reg_D, src_A, src_B, alu_op, type, I, Z, L;
void decode()
{
    // start decoding
    type = GET_TYPE(INSTR);
    I = GET_I(INSTR);

    // DP && MEM
    if (type == DP)
    {
        reg_D = GET_DP_SRC_D(INSTR);
        src_A = GET_DP_SRC_A(INSTR);
        src_B = I ? GET_DP_SRC_B_IMM(INSTR) : GET_DP_SRC_B_REG(INSTR);

        switch (GET_DP_FUNC(INSTR))
        {
        case ADD:
            alu_op = 0;
            break;
        case SUB:
            alu_op = 1;
            break;
        case ORR:
            alu_op = 2;
            break;
        case AND:
            alu_op = 3;
            break;
        };
    }
    else if (type == MEM)
    {
        reg_D = GET_MEM_SRC_D(INSTR);
        src_A = GET_MEM_SRC_A(INSTR);
        src_B = I ? GET_MEM_SRC_B_IMM(INSTR) : GET_MEM_SRC_B_REG(INSTR);
        L = GET_L(INSTR);
        alu_op = 0;
    }
    // JMP
    else if (type == BCH)
    {
        src_A = GET_JMP_IMM(INSTR);
        Z = GET_Z(INSTR);
        alu_op = 0;
    }
    else
    {
        printf("Unsuported operation. \n");
    }
}

WORD alu(WORD A, WORD B, unsigned char op)
{
    switch (op)
    {
    case 0:
        return A + B;
        break;
    case 1:
        return A - B;
        break;
    case 2:
        return A | B;
        break;
    case 3:
        return A & B;
        break;
    default:
        return 0;
        break;
    }
}

void execute()
{
    // UPDATE VALUE r[REG_PC]
    R[REG_PC] = PC;

    // LOAD from register file
    WORD A = R[src_A], B;
    if (I)
        B = src_B;
    else
        B = R[src_B];

    // Now exec using the alu
    WORD result = alu(A, B, alu_op);
    // set flags
    if (type == DP)
        FLAG_Z = (result == 0);

    // Check the type
    if (type == DP)
    {
        // JUST STORE IT
        R[reg_D] = result;
        PC += 1;
    }
    else if (type == MEM)
    {
        if (L)
            // LOAD FROM MEM
            R[reg_D] = RAM[result];
        else
            // STORE TO MEM
            RAM[result] = reg_D;
        PC += 1;
    }
    else if (type == BCH)
    {
        if (Z)
        {
            if (FLAG_Z)
                PC = src_A;
        }
        else
            PC = src_A;
    }
}

void run()
{
    while (PC < END_ROM)
    {
        fetch();
        decode();
        execute();
    }
}

//
// ROM LOADER
//
void load_rom(FILE *rom_data)
{
    WORD index = 0;
    char instr[4];
    while (fgets(instr, 5, rom_data))
    {
        fgetc(rom_data);
        // CONVERT STRING TO HEX
        WORD r = strtol(instr, NULL, 16);
        ROM[index] = r;
        index++;
    }
    END_ROM = index;
    printf("loaded %d instruction(s)\n", index);
}

int main(int argc, char **argv)
{
    printf("Enlec16 v1.0 - CPU EMULATOR\n");

    // INIT CPU
    printf("ANLEC - 2024\n");
    init();

    if (argc < 2)
    {
        printf("ROM file required.\n");
        return 1;
    }

    // LOAD CONTENTS INTO ROM
    FILE *rom_data;
    rom_data = fopen(argv[1], "r");

    // checking if the file is opened successfully
    if (rom_data == NULL)
    {
        printf("Cannot find the rom file. Exiting now...\n");
        return 1;
    }

    printf("\nLoading rom...\n");
    load_rom(rom_data);
    printf("Done loading.\n");
    fclose(rom_data);

    // START EXECUTING
    run();
    printf("Final RAM status: \n");

    // print RAM
    for (int i = 0; i < MEM_SIZE; i++)
    {
        printf("%04x ", RAM[i]);
        if (i % MEM_M_SIZE == 3)
        {
            printf("\n");
        }
    }

    printf("Final REG status: \n");
    // print REGS
    for (int i = 0; i < NREGS; i++)
    {
        if (i == REG_PC)
            printf("R%d (PC): %04x \n", i, R[i]);
        else
            printf("R%d: %04x \n", i, R[i]);
    }

    // EXIT
    return 0;
}