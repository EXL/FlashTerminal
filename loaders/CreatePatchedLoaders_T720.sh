#!/usr/bin/bash

MCORE_TOOLCHAIN_BIN_DIR=/opt/mcore-elf-gcc/bin

# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_T720_0370 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M210_T720.ld -o patch_nor.bin

cp T720_RAMDLD_0370.bin T720_RAMDLD_0370_Patched_Dump_NOR.bin

## Insert patch to 0x111EC offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('T720_RAMDLD_0370_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x111EC);o.write(i.read())"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
