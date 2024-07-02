#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -apcs /interwork -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x01016800 patch_nor.o ../syms/V120e_RAMDLD_0713.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp V120e_RAMDLD_0713.ldr V120e_RAMDLD_0713_Patched_Dump_NOR.ldr

# Insert patch to 0x6800 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V120e_RAMDLD_0713_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x6800);o.write(i.read())"

# Add branch patch.
python3 -c "with open('V120e_RAMDLD_0713_Patched_Dump_NOR.ldr','r+b') as f: f.seek(0x1306);f.write(b'\x05\xF0\x7B\xFA')"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
