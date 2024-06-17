#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x110661FC patch_nor.o ../syms/C350_RAMDLD_0372.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp C350_RAMDLD_0372.bin C350_RAMDLD_0372_Patched_Dump_NOR.bin

# Insert patch to 0x61FC offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('C350_RAMDLD_0372_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x61FC);o.write(i.read())"

# Add branch patch.
#python3 -c "with open('C350_RAMDLD_0372_Patched_Dump_NOR.bin','r+b') as f: f.seek(0x183A);f.write(b'\xF0\x08\xF8\x29')"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
