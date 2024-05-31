#!/usr/bin/bash

MCORE_TOOLCHAIN_BIN_DIR=/opt/mcore-elf-gcc/bin

# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_V60_0355 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M340_A830.ld -o patch_nor.bin

cp V60_RAMDLD_0355.bin V60_RAMDLD_0355_Patched_Dump_NOR.bin

## Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V60_RAMDLD_0355_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x40);o.write(i.read())"

## Add branch patch.
python3 -c "with open('V60_RAMDLD_0355_Patched_Dump_NOR.bin','r+b') as f: f.seek(0xD54);f.write(b'\x11\x01\x00\x40')"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin


# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_V60_0371 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M340_A830.ld -o patch_nor.bin

cp V60_RAMDLD_0371.bin V60_RAMDLD_0371_Patched_Dump_NOR.bin

## Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V60_RAMDLD_0371_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x40);o.write(i.read())"

## Add branch patch.
python3 -c "with open('V60_RAMDLD_0371_Patched_Dump_NOR.bin','r+b') as f: f.seek(0xD938);f.write(b'\x11\x01\x00\x40')"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin


# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_V66I_1001 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M340_A830.ld -o patch_nor.bin

cp V66i_RAMDLD_1001.bin V66i_RAMDLD_1001_Patched_Dump_NOR.bin

## Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V66i_RAMDLD_1001_Patched_Dump_NOR.bin','r+b') as o: o.seek(0x40);o.write(i.read())"

## Add branch patch.
python3 -c "with open('V66i_RAMDLD_1001_Patched_Dump_NOR.bin','r+b') as f: f.seek(0xE358);f.write(b'\x00\x0f\x34\x34')"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin


# Compile dump NOR patch.
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-gcc -nostdinc -nostdlib -fshort-wchar -funsigned-char -fpic -fpie -mbig-endian \
	-m210 -DM_CORE_MOTOROLA_V66I_1001_2 -O2 -c ../Injection_RQRC_Dump_SRAM.c -o patch_nor.o
${MCORE_TOOLCHAIN_BIN_DIR}/mcore-elf-ld -nostdinc -nostdlib -Bstatic patch_nor.o \
	-T../lds/Injection_MCORE_M340_A830.ld -o patch_nor.bin

cp V66i_RAMDLD_1001.bin V66i_RAMDLD_1001_Patched_Dump_NOR_2.bin

## Insert patch to 0x40 offset.
python3 -c "with open('patch_nor.bin','rb') as i,open('V66i_RAMDLD_1001_Patched_Dump_NOR_2.bin','r+b') as o: o.seek(0x40);o.write(i.read())"

## Add branch patch.
python3 -c "with open('V66i_RAMDLD_1001_Patched_Dump_NOR_2.bin','r+b') as f: f.seek(0xE358);f.write(b'\x11\x01\x00\x40')"

## Clean intermedianes.
rm -f *.o *.elf patch_nor.bin
