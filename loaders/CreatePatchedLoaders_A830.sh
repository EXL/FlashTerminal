#!/usr/bin/bash

MCORE_TOOLCHAIN_BIN_DIR=/opt/mcore-elf-gcc/bin

# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m340 -DM_CORE_MOTOROLA_A830_SIEMENS_U10 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M340_A830.ld -o patch_nor.bin

cp A830_RAMDLD_0520.bin A830_RAMDLD_0520_Patched_Dump_NOR.bin

# Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('A830_RAMDLD_0520_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x40);o.write(i.read())"

# Add branch patch.
python3 -c "with open('A830_RAMDLD_0520_Patched_Dump_NOR.bin','r+b') as f: f.seek(0x1030);f.write(b'\x07\x80\x00\x40')"

# Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
