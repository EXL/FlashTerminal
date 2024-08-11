#!/usr/bin/bash

ADS_TOOLCHAIN_BIN_DIR=/opt/arm/bin/

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/tcc -bigend -apcs /interwork -O2 ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0x1200BC44 patch_nor.o ../syms/A768i_BP_RAMDLD_0731.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp A768i_BP_RAMDLD_0731.bin A768i_BP_RAMDLD_0731_Patched_Dump_NOR.bin

# Insert patch to 0xBC44 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('A768i_BP_RAMDLD_0731_Patched_Dump_NOR.bin','r+b') as o: o.seek(0xBC44);o.write(i.read())"

# Add branch patch.
python3 -c "with open('A768i_BP_RAMDLD_0731_Patched_Dump_NOR.bin','r+b') as f: f.seek(0xA8CC);f.write(b'\xF0\x01\xF9\xBA')"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin

# Compile dump SRAM patch.
${ADS_TOOLCHAIN_BIN_DIR}/armcc -apcs /interwork -O2 -DEZX_AP ../Injection_RQRC_Dump_SRAM.c -c -o patch_nor.o
${ADS_TOOLCHAIN_BIN_DIR}/armlink -ro-base 0xA0203708 patch_nor.o ../syms/A768i_AP_RAMDLD_0000.sym -o patch_nor.elf
${ADS_TOOLCHAIN_BIN_DIR}/fromelf patch_nor.elf -bin -output patch_nor.bin

cp A768i_AP_RAMDLD_0000.ldr A768i_AP_RAMDLD_0000_Patched_Dump_NOR.ldr

# Insert patch to 0x3708 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('A768i_AP_RAMDLD_0000_Patched_Dump_NOR.ldr','r+b') as o: o.seek(0x3708);o.write(i.read())"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
