#!/usr/bin/bash

MCORE_TOOLCHAIN_BIN_DIR=/opt/mcore-elf-gcc/bin

# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_V60I_1007 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M210_V60i.ld -o patch_nor.bin

cp V60i_RAMDLD_1007.bin V60i_RAMDLD_1007_Patched_Dump_NOR.bin

## Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V60i_RAMDLD_1007_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x40);o.write(i.read())"

## Add branch patch.
python3 -c "with open('V60i_RAMDLD_1007_Patched_Dump_NOR.bin','r+b') as f: f.seek(0x6944);f.write(b'\x11\x01\x00\x40')"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin

# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_V60I_1007 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M210_V60i_2.ld -o patch_nor.bin

cp V60i_RAMDLD_1007.bin V60i_RAMDLD_1007_Patched_Dump_NOR_2.bin

## Insert patch to 0x9A10 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V60i_RAMDLD_1007_Patched_Dump_NOR_2.bin','r+b') as o: o.seek(0x9A10);o.write(i.read())"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
