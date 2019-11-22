#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# interpreter for crt4004 ROM
# version 1.0 beta

# OP
OP_RTYPE = '000000'
OP_LW = '100011'
OP_SW = '101011'
OP_BEQ = '000100'
OP_ADDI = '001000'

# R-TYPE
R_ADD = '100000'
R_SUB = '100010'
R_AND = '100100'
R_OR = '100101'
R_SLT = '101010'

# DEFINE
_FORMAT_WORD_TO_BYTE_ = False
_FORMAT_BIN_TO_HEX_ = True
_FORMAT_HEX_UPPERCASE_ = True


# Convert '123' to '7b'
def dec_str_to_hex(dec_str):
    return format(int(dec_str, 10), 'x')


# Convert '123' to '01111011' (fill zero)
def dec_str_to_bin(dec_str, bin_len):
    return format(int(dec_str, 10), 'b').zfill(bin_len)


# ASM to BIN
def asm_interpreter(instr_asm):
    instr_bin = ""
    if instr_asm[0] == 'PC':
        instr_bin = '@' + dec_str_to_hex(instr_asm[1])
    elif instr_asm[0] == 'ADD':
        instr_bin = (OP_RTYPE
                     + dec_str_to_bin(instr_asm[1].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[2].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[3].replace('$', ''), 5)
                     + '00000' + R_ADD)
    elif instr_asm[0] == 'SUB':
        instr_bin = (OP_RTYPE
                     + dec_str_to_bin(instr_asm[1].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[2].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[3].replace('$', ''), 5)
                     + '00000' + R_SUB)
    elif instr_asm[0] == 'LW':
        instr_bin = (OP_LW
                     + dec_str_to_bin(instr_asm[1].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[2].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[3], 16))
    elif instr_asm[0] == 'SW':
        instr_bin = (OP_SW
                     + dec_str_to_bin(instr_asm[1].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[2].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[3], 16))
    elif instr_asm[0] == 'BEQ':
        instr_bin = (OP_BEQ
                     + dec_str_to_bin(instr_asm[1].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[2].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[3], 16))
    elif instr_asm[0] == 'ADDI':
        instr_bin = (OP_ADDI
                     + dec_str_to_bin(instr_asm[1].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[2].replace('$', ''), 5)
                     + dec_str_to_bin(instr_asm[3], 16))
    else:
        instr_bin = '{undefined instruction:' + str(instr_asm) + '}'

    return instr_bin


# split word for bin instructions
def format_bin(instr_str):
    if instr_str[0] == '{' and instr_str[-1] == '}':
        return '*ERROR: ' + instr_str + '*'
    if not _FORMAT_WORD_TO_BYTE_:
        return instr_str
    else:
        if instr_str[0] == '@':
            return instr_str
        elif len(instr_str) == 32:
            return instr_str[0:8] + ' ' + instr_str[8:16] + ' ' + instr_str[16:24] + ' ' + instr_str[24:32]
        else:
            return '*ERROR: {unknown}*'


# convert bin to hex
def format_bin_to_hex(bin_instr):
    if bin_instr[0] == '{' and bin_instr[-1] == '}':
        return bin_instr
    elif bin_instr[0] == '@':
        return bin_instr
    elif len(bin_instr) == 32:
        return format(int(bin_instr, 2), 'X' if _FORMAT_HEX_UPPERCASE_ else 'x').zfill(8)
    else:
        return '*ERROR: {unknown}*'


# split word for hex instructions
def format_hex(instr_str):
    if instr_str[0] == '{' and instr_str[-1] == '}':
        return '*ERROR: ' + instr_str + '*'
    if not _FORMAT_WORD_TO_BYTE_:
        return instr_str
    else:
        if instr_str[0] == '@':
            return instr_str
        if len(instr_str) == 8:
            return instr_str[0:2] + ' ' + instr_str[2:4] + ' ' + instr_str[4:6] + ' ' + instr_str[6:8]
        else:
            return '*ERROR: {unknown}*'


# convert bin to hex & format bin/hex
def format_bin_to_out(instr_bin_str):
    if not _FORMAT_BIN_TO_HEX_:
        return format_bin(instr_bin_str)
    else:
        return format_hex(format_bin_to_hex(instr_bin_str))


def main():
    f = open('rom_raw.txt')

    # preprocess
    asm_instr_list = [i.replace('\r', '').replace('\n', '').replace('\t', ' ') for i in f.readlines()]

    for asm_instr in asm_instr_list:
        if asm_instr == '':
            asm_instr_list.remove(asm_instr)

    print('file instruction list:\t', end='')
    print(asm_instr_list)

    # split instruction
    asm_instr_element_list = [i.split() for i in asm_instr_list]

    print('asm instruction list:\t', end='')
    print(asm_instr_element_list)

    # interpreter to asm
    bin_instr_list = [asm_interpreter(asm_instr) for asm_instr in asm_instr_element_list]
    # output format
    out_instr_list = [format_bin_to_out(bin_instr) for bin_instr in bin_instr_list]

    print('%s instruction list:\t' % ('bin' if not _FORMAT_BIN_TO_HEX_ else 'hex'), end='')
    print(out_instr_list)

    f.close()


if __name__ == '__main__':
    main()
