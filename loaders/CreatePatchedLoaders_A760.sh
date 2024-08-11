#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x11073E2C patch_nor.o ../syms/A760_BP_RAMDLD_0372.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp A760_BP_RAMDLD_0372.bin A760_BP_RAMDLD_0372_Patched_Dump_NOR.bin

# Insert patch to 0x13E2C offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('A760_BP_RAMDLD_0372_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x13E2C);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -O2 -DEZX_AP ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0xA020370C patch_nor.o ../syms/A760_AP_RAMDLD_0000.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp A760_AP_RAMDLD_0000.ldr A760_AP_RAMDLD_0000_Patched_Dump_NOR.ldr

# Insert patch to 0x370C offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('A760_AP_RAMDLD_0000_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x370C);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
