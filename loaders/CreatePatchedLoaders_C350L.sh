#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x12000040 patch_nor.o ../syms/C350L_RAMDLD_0000.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp C350L_RAMDLD_0000.ldr C350L_RAMDLD_0000_Patched_Dump_NOR.ldr

# Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('C350L_RAMDLD_0000_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x40);o.write(i.read())"

# Add branch patch.
python3 -c "with open('C350L_RAMDLD_0000_Patched_Dump_NOR.ldr','r+b') as f: f.seek(0x18A8);f.write(b'\xF7\xFE\xFB\xCA')"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
