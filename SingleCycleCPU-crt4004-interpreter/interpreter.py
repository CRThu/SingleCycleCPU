#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# interpreter for crt4004 ROM
# version 1.2

import sys
import math

# OP
OP_RTYPE = '000000'
OP_LW = '100011'
OP_SW = '101011'
OP_BEQ = '000100'
OP_ADDI = '001000'
OP_NOP = '111111'

# R-TYPE
R_ADD = '100000'
R_SUB = '100010'
R_AND = '100100'
R_OR = '100101'
R_SLT = '101010'

# DEFINE
#_FORMAT_WORD_TO_BYTE_ = False
_FORMAT_BIN_TO_HEX_ = True
_FORMAT_HEX_UPPERCASE_ = True


# Convert '123' to '7b'
def dec_str_to_hex_div4(dec_str):
    return format(math.floor(int(dec_str, 10)/4), 'x')


# Convert '123' to '01111011' (fill zero)
def dec_str_to_bin(dec_str, bin_len):
    return format(int(dec_str, 10), 'b').zfill(bin_len)


# ASM to BIN
def asm_interpreter(asm_instr):
    bin_instr = ""
    if asm_instr[0] == 'PC':
        bin_instr = '@' + dec_str_to_hex_div4(asm_instr[1])
    elif asm_instr[0] == 'ADD':
        bin_instr = (OP_RTYPE
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3].replace('$', ''), 5)
                     + '00000' + R_ADD)
    elif asm_instr[0] == 'SUB':
        bin_instr = (OP_RTYPE
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3].replace('$', ''), 5)
                     + '00000' + R_SUB)
    elif asm_instr[0] == 'LW':
        bin_instr = (OP_LW
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'SW':
        bin_instr = (OP_SW
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'BEQ':
        bin_instr = (OP_BEQ
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'ADDI':
        bin_instr = (OP_ADDI
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'NOP':
        bin_instr = (OP_NOP
                     + '11111'
                     + '11111'
                     + '1111111111111111')
    else:
        bin_instr = '{undefined instruction:' + str(asm_instr) + '}'

    return bin_instr


# split word for bin instructions
def format_bin(instr_str):
    if instr_str[0] == '{' and instr_str[-1] == '}':
        return '*ERROR: ' + instr_str + '*'
    else:
        return instr_str

    # if not _FORMAT_WORD_TO_BYTE_:
    #     return instr_str
    # else:
    #     if instr_str[0] == '@':
    #         return instr_str
    #     elif len(instr_str) == 32:
    #         return instr_str[0:8] + ' ' + instr_str[8:16] + ' ' + instr_str[16:24] + ' ' + instr_str[24:32]
    #     else:
    #         return '*ERROR: {unknown}*'


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
    else:
        return instr_str
    # if not _FORMAT_WORD_TO_BYTE_:
    #     return instr_str
    # else:
    #     if instr_str[0] == '@':
    #         return instr_str
    #     if len(instr_str) == 8:
    #         return instr_str[0:2] + ' ' + instr_str[2:4] + ' ' + instr_str[4:6] + ' ' + instr_str[6:8]
    #     else:
    #         return '*ERROR: {unknown}*'


# convert bin to hex & format bin/hex
def format_bin_to_out(instr_bin_str):
    if not _FORMAT_BIN_TO_HEX_:
        return format_bin(instr_bin_str)
    else:
        return format_hex(format_bin_to_hex(instr_bin_str))


class mif_file_gen_class(object):
    # TODO : changing parameters is not supported yet
    def __init__(self, mif_path, mif_width=32, mif_depth=256, addr_radix='HEX', data_radix='HEX'):
        # parameter
        self.mif_path = mif_path
        self.mif_width = mif_width
        self.mif_depth = mif_depth
        self.addr_radix = addr_radix
        self.data_radix = data_radix
        # value
        self.write_mif_file = None
        self.mif_lines = []
        self.rom_addr = 0
        self.append_header()
        self.append_ender()

    def read_lines(self):
        return self.mif_lines

    # write mif file header
    def append_header(self):
        self.mif_lines.append('WIDTH=' + str(self.mif_width) + ';')
        self.mif_lines.append('DEPTH=' + str(self.mif_depth) + ';')
        self.mif_lines.append('')
        self.mif_lines.append('ADDRESS_RADIX=' + self.addr_radix + ';')
        self.mif_lines.append('DATA_RADIX=' + self.data_radix + ';')
        self.mif_lines.append('')
        self.mif_lines.append('CONTENT BEGIN')

    # write instructions
    # '00:FFFFFFFF;'
    def append_instructions(self, bin_instr):
        if bin_instr[0] == '{' and bin_instr[-1] == '}':
            self.mif_lines.insert(-1, bin_instr)
            self.rom_addr += 1
        elif bin_instr[0] == '@':
            self.rom_addr = int(bin_instr[1:], 16)
        elif len(bin_instr) == 32:
            self.mif_lines.insert(-1, format(self.rom_addr, 'x').zfill(math.ceil(math.log(self.mif_depth, 16))) + ':'
                                  + format(int(bin_instr, 2), 'X' if _FORMAT_HEX_UPPERCASE_ else 'x').zfill(
                math.ceil(self.mif_width / 8 * 2)) + ';')
            self.rom_addr += 1
        else:
            self.mif_lines.insert(-1, '*ERROR: {unknown}*')
            self.rom_addr += 1

    # write mif file end
    def append_ender(self):
        self.mif_lines.append('END;')

    def open(self):
        self.write_mif_file = open(self.mif_path, 'w')

    def close(self):
        self.write_mif_file.close()

    def write_lines(self):
        self.open()
        for mif_line in self.mif_lines:
            self.write_mif_file.write(mif_line + '\n')
        self.close()


def main():
    # read input file name
    try:
        asm_path = sys.argv[1]
    except IndexError:
        asm_path = 'rom_raw.txt'

    # read output dat file name
    dat_path = asm_path.replace('.txt', '.dat')
    if dat_path.rfind('.dat') == -1:
        dat_path += '.dat'

    # read output mif file name
    mif_path = asm_path.replace('.txt', '.mif')
    if mif_path.rfind('.mif') == -1:
        mif_path += '.mif'

    print('input txt file path:\t' + asm_path)
    print('output dat file path:\t' + dat_path)
    print('output mif file path:\t' + mif_path)

    # read asm file
    read_asm_file = open(asm_path)

    # preprocess
    asm_instr_list = [i.replace('\r', '').replace('\n', '').replace('\t', ' ') for i in read_asm_file.readlines()]

    read_asm_file.close()

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

    # write dat file
    write_dat_file = open(dat_path, 'w')
    for i in out_instr_list:
        write_dat_file.write(i + '\n')
    write_dat_file.close()

    # write mif file
    mif_file_gen = mif_file_gen_class(mif_path)

    for bin_instr in bin_instr_list:
        mif_file_gen.append_instructions(bin_instr)

    print('mif file list:\t\t\t', end='')
    print(mif_file_gen.read_lines())

    mif_file_gen.write_lines()


if __name__ == '__main__':
    main()
